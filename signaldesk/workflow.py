import json
import os
from pathlib import Path
import time
import uuid
from .core import normalize,now,questions,rank,public_url
from .providers import API,profile,search

ROOT=Path(__file__).resolve().parent.parent

def execute(options, callback=lambda r:None, api=None):
    api=api or API()
    provider=options.get('provider','twitterapi')
    url=public_url(options.get('url',''))
    limit=options.get('limit',60);days=options.get('days',30)
    if type(limit)!=int or not 1<=limit<=100 or type(days)!=int or not 1<=days<=365:
        raise ValueError('Post limit must be 1–100; date window must be 1–365 days')
    if provider not in ['twitterapi','x','exa','import']:raise ValueError('Invalid data provider')
    rows=options.get('posts',[])
    if provider=='import' and (not isinstance(rows,list) or not 1<=len(rows)<=500):raise ValueError('Import 1–500 posts as a JSON array')
    required=['BLOCKRUN_API_KEY','TYPESAFE_API_KEY']+({'twitterapi':['TWITTERAPI_KEY'],'x':['X_BEARER_TOKEN']}.get(provider,[]))
    missing=[key for key in required if not os.getenv(key)]
    if missing:raise ValueError('Missing configuration: '+', '.join(missing))
    run={'id':str(uuid.uuid4()),'started_at':now().isoformat(),'status':'running','stage':'company','provider':provider,
         'mode':'imported posts' if provider=='import' else 'live search','days':days,'limit':limit,'posts':[],
         'events':[],'calls':api.calls,'warnings':[],'schema_version':1}
    path=ROOT/'runs'/f"{run['id']}.json";path.parent.mkdir(exist_ok=True)
    start=time.monotonic()
    def save(stage,message):
        run['stage']=stage;run['events'].append({'at':now().isoformat(),'stage':stage,'message':message})
        run['elapsed_seconds']=round(time.monotonic()-start,2)
        run['cost']={'reported_usd':round(sum(c['cost_usd'] for c in api.calls if c.get('cost_usd') is not None and c['cost_basis']=='provider-reported'),6),
                     'estimated_usd':round(sum(c['cost_usd'] for c in api.calls if c.get('cost_usd') is not None and c['cost_basis'].startswith('estimate')),6),
                     'unknown_calls':sum(c.get('cost_usd') is None for c in api.calls)}
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(run,ensure_ascii=False,indent=2));temp.replace(path)
        callback(json.loads(json.dumps(run)))
    try:
        save('company','Reading the product and its documented capabilities')
        company=profile(api,url,options.get('brief',''));run['company']=company
        save('search','Collecting source posts')
        if provider!='import':rows,traces=search(api,provider,company,days,limit,options.get('queries'));run['searches']=traces
        else:run['searches']=[];run['warnings'].append('Imported text is supplied evidence, not independently verified by SignalDesk. Review the original links.')
        if provider=='exa':run['warnings'].append('Exa is a web index: X coverage and original-text completeness are not guaranteed. Indexed results require source verification.')
        if provider=='x' and days>7:run['warnings'].append('X Recent Search searches only the last 7 days; use a full-archive provider for a longer window.')
        posts,rejected=normalize(rows,provider,days=days,max_posts=limit)
        run.update(raw_count=len(rows),rejected=rejected,valid_count=len(posts))
        if not posts:
            run.update(status='empty',posts=[])
            save('done','No eligible source posts returned. Change the query or configure a dedicated X provider.');return run
        save('classify',f'Jev is evaluating {len(posts)} posts')
        classified=[];jev_start=time.monotonic();models=set()
        for offset in range(0,len(posts),15):
            batch=posts[offset:offset+15];payload=questions(company,batch)
            payload['model']=os.getenv('JEV_MODEL','jev-1.13.0')
            response=api.call('jev','/v1/systemone',payload,'classify')
            if payload['model']!='jev-latest' and response.get('model')!=payload['model']:raise ValueError('Jev returned an unexpected model')
            models.add(response.get('model'));classified.extend(rank(batch,response))
            run['posts']=sorted(classified,key=lambda p:(p['priority']=='review',p['score']),reverse=True)
            save('classify',f'{len(classified)} / {len(posts)} posts classified')
        run['jev_seconds']=round(time.monotonic()-jev_start,3);run['models']=sorted(models)
        top=[p for p in run['posts'] if p['priority']=='review'][:5]
        if top:
            save('draft','Preparing evidence-linked suggestions for human review')
            r=api.chat('Given company facts and selected posts, return {"leads":[{"id":"exact post id","reason":"brief evidence-based fit explanation","evidence":"an EXACT verbatim substring of that post, 10-200 characters","check":"one important unknown to confirm","draft":"a short helpful public reply DRAFT, same language as post"}]}. Do not promise features absent from company facts, infer sensitive traits, add discounts, fabricate experience or claim affiliation. Only these IDs; do not send anything.',{'company':company,'posts':top},'draft')
            annotations=r.get('leads',[])
            byid={p['id']:p for p in top};seen=set()
            if not isinstance(annotations,list):raise ValueError('Invalid draft response')
            for a in annotations:
                if not isinstance(a,dict) or a.get('id') not in byid or a['id'] in seen:raise ValueError('Invalid draft post ID')
                if not all(isinstance(a.get(k),str) and a[k].strip() for k in ['reason','evidence','check','draft']):raise ValueError('Incomplete draft')
                if not 10<=len(a['evidence'])<=200 or a['evidence'] not in byid[a['id']]['text']:raise ValueError('Draft evidence is not an exact source quote')
                seen.add(a['id']);byid[a['id']]['suggestion']={k:a[k] for k in ['reason','evidence','check','draft']}
            if seen!=set(byid):raise ValueError('Missing a requested lead suggestion')
        run['status']='complete';run['ended_at']=now().isoformat()
        save('done',f"Ready: {sum(p['priority']=='review' for p in run['posts'])} posts merit review. No messages sent.")
    except Exception as e:
        run['status']='failed';run['error']=str(e) if isinstance(e,(ValueError,RuntimeError)) else f'{type(e).__name__}: workflow failed'
        save('error',run['error'])
    return run
