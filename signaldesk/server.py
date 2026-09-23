import csv
import io
import json
import os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import re
import secrets
import threading
from urllib.parse import urlparse
from .core import safe_csv
from .workflow import ROOT,execute

def serve(port=8787):
    state={'run':None,'busy':False};lock=threading.Lock();token=secrets.token_urlsafe(24)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def valid_host(self):
            return self.headers.get('Host') in (f'127.0.0.1:{port}',f'localhost:{port}')
        def send(self,status,data,ctype='application/json'):
            if not isinstance(data,bytes):data=json.dumps(data,ensure_ascii=False).encode()
            self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(data)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers();self.wfile.write(data)
        def do_GET(self):
            if not self.valid_host():return self.send(403,{'error':'Invalid host'})
            path=urlparse(self.path).path
            files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8')}
            files.update({key:(name,ctype) for key,name,ctype in [('/demo','demo.html','text/html; charset=utf-8'),('/flow.css','flow.css','text/css; charset=utf-8'),('/flow.js','flow.js','text/javascript; charset=utf-8'),('/flow-player.js','flow-player.js','text/javascript; charset=utf-8'),('/vendor/gsap.min.js','vendor/gsap.min.js','text/javascript; charset=utf-8')]})
            if path in files:
                name,ctype=files[path];return self.send(200,(ROOT/'web'/name).read_bytes(),ctype)
            if path=='/api/config':return self.send(200,{'token':token,'configured':{k:bool(os.getenv(k)) for k in ['BLOCKRUN_API_KEY','TYPESAFE_API_KEY','TWITTERAPI_KEY','X_BEARER_TOKEN']}})
            if path=='/api/status':
                with lock:snapshot=json.loads(json.dumps(state))
                return self.send(200,snapshot)
            if path=='/api/runs':
                runs=[]
                for p in sorted((ROOT/'runs').glob('*.json'),key=lambda p:p.stat().st_mtime,reverse=True)[:30]:
                    d=json.loads(p.read_text());runs.append({k:d.get(k) for k in ['id','status','started_at','provider','valid_count']}|{'company':d.get('company',{}).get('name','Incomplete run')})
                return self.send(200,runs)
            m=re.fullmatch(r'/api/runs/([a-f0-9-]{36})(\.csv)?',path)
            if m:
                p=ROOT/'runs'/f'{m[1]}.json'
                if not p.exists():return self.send(404,{'error':'Run not found'})
                d=json.loads(p.read_text())
                if not m[2]:return self.send(200,d)
                stream=io.StringIO();w=csv.writer(stream);fields=['url','created_at','text','category','priority','score','fit','intent','confidence'];w.writerow(fields)
                for row in d.get('posts',[]):w.writerow([safe_csv(row.get(k,'')) for k in fields])
                return self.send(200,stream.getvalue().encode('utf-8-sig'),'text/csv; charset=utf-8')
            return self.send(404,{'error':'Not found'})
        def do_POST(self):
            if not self.valid_host() or self.headers.get('X-SignalDesk-Token')!=token:return self.send(403,{'error':'Refresh the local page'})
            if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{port}',f'http://localhost:{port}'):return self.send(403,{'error':'Invalid origin'})
            if self.path!='/api/run':return self.send(404,{'error':'Not found'})
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=2_000_000:raise ValueError('Request too large or empty')
                options=json.loads(self.rfile.read(length))
                if not isinstance(options,dict):raise ValueError('Expected JSON object')
            except (ValueError,json.JSONDecodeError):return self.send(400,{'error':'Invalid input JSON'})
            with lock:
                if state['busy']:return self.send(409,{'error':'A run is already in progress'})
                state.update(busy=True,run=None)
            def update(run):
                with lock:state['run']=run
            def work():
                try:execute(options,update)
                except Exception as e:update({'status':'failed','stage':'error','error':str(e) if isinstance(e,(ValueError,RuntimeError)) else 'Run failed','posts':[],'events':[]})
                finally:
                    with lock:state['busy']=False
            threading.Thread(target=work,daemon=True).start();self.send(202,{'accepted':True})
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'SignalDesk → http://127.0.0.1:{port}',flush=True)
    server.serve_forever()
