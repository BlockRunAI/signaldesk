"""Opt-in PAID integration check with explicitly synthetic fixtures, never customer data."""
import argparse
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from signaldesk.providers import API,load_env
from signaldesk.core import questions,rank,now

p=argparse.ArgumentParser();p.add_argument('--env',default='.env');args=p.parse_args();load_env(args.env)
api=API(max_calls=2)
company={'name':'SYNTHETIC TEST COMPANY','capabilities':['Prepaid mobile data eSIMs for Japan'],'limitations':['Requires an unlocked, eSIM-compatible phone; cannot supply physical SIM cards']}
posts=[{'id':'fixture-seeking','text':'Heading to Japan next week. My unlocked iPhone supports eSIM. Can anyone recommend a prepaid data eSIM?'},
       {'id':'fixture-incompatible','text':'My phone does not support eSIM. Need a physical SIM card for Japan. Where can I buy one?'},
       {'id':'fixture-promotion','text':'Get our amazing travel eSIM today! Use my affiliate code for 20% off.'}]
payload=questions(company,posts);payload['model']=os.getenv('JEV_MODEL','jev-1.13.0')
response=api.call('jev','/v1/systemone',payload,'synthetic-contract-test')
ranked=rank(posts,response)
byid={v['id']:v for v in ranked}
checks={'seeking_selected':byid['fixture-seeking']['priority']=='review',
        'incompatible_excluded':byid['fixture-incompatible']['priority']=='excluded',
        'promotion_excluded':byid['fixture-promotion']['priority']=='excluded'}
draft=api.chat('This is a SYNTHETIC integration test. Return {"evidence":"an exact substring of the provided post, 10-200 characters","draft":"short reply asking a relevant clarifying question"}. Do not invent company capabilities.',{'company':company,'post':posts[0]},'synthetic-draft-test')
checks['exact_quote']=isinstance(draft.get('evidence'),str) and 10<=len(draft['evidence'])<=200 and draft['evidence'] in posts[0]['text']
checks['draft_present']=isinstance(draft.get('draft'),str) and bool(draft['draft'].strip())
out={'label':'SYNTHETIC CONTRACT TEST — NOT CUSTOMER LEADS','at':now().isoformat(),'model':response.get('model'),'checks':checks,'calls':api.calls,'classifications':[{k:v[k] for k in ['id','category','priority','fit','intent','confidence']} for v in ranked]}
dest=Path('data')/'synthetic-contract-test.json';dest.parent.mkdir(exist_ok=True);dest.write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2));sys.exit(0 if all(checks.values()) else 1)
