import argparse
import json
from pathlib import Path
from .providers import load_env
from .workflow import execute
from .server import serve

def main():
    p=argparse.ArgumentParser(description='SignalDesk · source-backed customer discovery')
    p.add_argument('--env',default='.env',help='Local dotenv path (never uploaded)')
    sub=p.add_subparsers(dest='command',required=True)
    s=sub.add_parser('serve');s.add_argument('--port',type=int,default=8787)
    r=sub.add_parser('run');r.add_argument('--url',required=True);r.add_argument('--brief',default='')
    r.add_argument('--provider',choices=['twitterapi','x','exa','import'],default='twitterapi')
    r.add_argument('--posts',help='Path to JSON array for import mode');r.add_argument('--query',action='append')
    r.add_argument('--days',type=int,default=30);r.add_argument('--limit',type=int,default=60)
    args=p.parse_args();load_env(args.env)
    if args.command=='serve':serve(args.port);return
    options={'url':args.url,'brief':args.brief,'provider':args.provider,'queries':args.query,'days':args.days,'limit':args.limit}
    if args.posts:options['posts']=json.loads(Path(args.posts).read_text())
    try:
        run=execute(options,lambda v:print(v.get('events',[{}])[-1].get('message',''),flush=True))
        print(json.dumps({'id':run['id'],'status':run['status'],'valid_posts':run.get('valid_count',0),'cost':run['cost']},ensure_ascii=False))
        if run['status']!='complete':raise SystemExit(2)
    except (ValueError,RuntimeError) as e:p.exit(2,str(e)+'\n')

if __name__=='__main__':main()
