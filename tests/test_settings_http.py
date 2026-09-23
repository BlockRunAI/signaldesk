import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from signaldesk.settings import KEYS

class SettingsHTTPTests(unittest.TestCase):
    def test_settings_are_local_authenticated_and_never_echo_secrets(self):
        with tempfile.TemporaryDirectory() as folder:
            envfile=Path(folder)/'.env'
            with socket.socket() as sock:
                sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
            env={k:v for k,v in os.environ.items() if k not in KEYS}
            proc=subprocess.Popen([sys.executable,'-m','signaldesk','--env',str(envfile),'serve','--port',str(port)],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            base=f'http://127.0.0.1:{port}'
            def request(path,body=None,headers=None):
                req=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers or {})
                try:
                    with urllib.request.urlopen(req,timeout=3) as response:return response.status,response.read()
                except urllib.error.HTTPError as error:
                    with error:return error.code,error.read()
            try:
                for _ in range(60):
                    try:code,raw=request('/api/config');break
                    except urllib.error.URLError:time.sleep(.05)
                else:self.fail('Local test server did not start')
                token=json.loads(raw)['token'];secret='synthetic-test-secret-123'
                payload={'keys':{'X_BEARER_TOKEN':secret},'persist':True}
                self.assertEqual(request('/api/settings',payload)[0],403)
                headers={'X-SignalDesk-Token':token,'Content-Type':'application/json','Origin':'https://untrusted.example'}
                self.assertEqual(request('/api/settings',payload,headers)[0],403)
                headers['Origin']=base
                code,raw=request('/api/settings',payload,headers)
                self.assertEqual(code,200);self.assertNotIn(secret.encode(),raw)
                self.assertIn(secret,envfile.read_text());self.assertEqual(envfile.stat().st_mode&0o777,0o600)
                code,raw=request('/api/config');self.assertEqual(code,200);self.assertNotIn(secret.encode(),raw)
                self.assertTrue(json.loads(raw)['configured']['X_BEARER_TOKEN'])
                self.assertEqual(request('/.env')[0],404)
                self.assertEqual(request('/api/config',headers={'Host':'untrusted.example'})[0],403)
            finally:
                proc.terminate();proc.wait(timeout=5)
