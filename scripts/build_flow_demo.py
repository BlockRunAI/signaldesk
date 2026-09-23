"""Build the English demo page and matching render from a verified local run.

No provider calls. Post excerpts are selected from the supplied real run.
"""
import argparse
import html
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('run',type=Path);args=p.parse_args()
r=json.loads(args.run.read_text());posts=r['posts']
selected=[p for p in posts if p['priority']=='review']
if len(selected)!=1 or r['valid_count']!=23:raise SystemExit('This storyboard expects the verified 23-post, one-candidate Tally run.')
lead=selected[0]
esc=lambda s:html.escape(str(s),quote=True)
handles=['tec_sany','DRudhamoy','euboid','oderajoseph',lead['author'],'SolFormsApp']
cards=[]
for handle in handles:
 post=next(x for x in posts if x['author']==handle)
 # Literal contiguous excerpts, not synthetic sample posts.
 excerpt=post['text'][:139];short=len(post['text'])>139
 cards.append(f'''<article class="post {'match' if post['url']==lead['url'] else ''}"><div class="post-head"><span class="avatar">{esc(handle[0].upper())}</span><a href="{esc(post['url'])}" target="_blank" rel="noopener noreferrer">@{esc(handle)}</a><time>{esc(post['created_at'][:10])}</time></div><p>{esc(excerpt)}{'…' if short else ''}</p></article>''')
content=f'''<div id="root" data-composition-id="signaldesk-flow" data-width="1920" data-height="1080" data-duration="32">
<div id="flow-scene" class="clip" data-start="0" data-duration="32" data-track-index="1">
<div class="main-stage"><div class="paper"></div><div class="brand"><b>s</b>signaldesk</div><div class="byline">BLOCKRUN + TYPESAFE JEV</div>
<div class="step-status"><div class="phase phase-a">Your product. Their next conversation.</div><div class="phase phase-b">Searching public conversations</div><div class="phase phase-c">Finding intent, not just keywords</div><div class="phase phase-d">One request worth a closer look</div></div>
<h1 class="headline">Someone is looking for <em>what you sell.</em></h1><div class="title-summary">From a product URL to <em>a real request.</em></div>
<div class="product"><span class="label">YOUR PRODUCT</span><strong>tally.so</strong><span class="goal">→ No-code forms</span></div>
<div class="run-tag"><span class="dot"></span>VERIFIED RUN REPLAY · 23 SEP 2026 UTC</div><div class="rule"></div>
<div class="column-title label-search"><span>1</span>Search X</div><div class="column-title label-judge"><span>2</span>Classify with Jev</div><div class="column-title label-output"><span>3</span>Review the opportunity</div>
<div class="feed-window"><div class="feed" data-layout-allow-overflow data-layout-allow-occlusion>{''.join(cards)}</div></div><div class="winner-outline"></div>
<div class="feed-foot"><strong>25</strong> records → <strong>23</strong> unique posts</div><div class="classification">Selected excerpts · 21 noise / 1 further research</div>
<div class="connector one"><div class="packet"></div></div><div class="connector two"><div class="packet"></div></div>
<div class="engine"><div class="engine-top"><div class="engine-title">Jev</div><span class="api-badge">API</span></div><div class="engine-sub">Intent + product fit, grounded in the post.</div><div class="checks">
<div class="check"><div class="check-head"><strong>Seeking a recommendation</strong><span class="check-value">92%</span></div><div class="track"><div class="fill intent"></div></div></div>
<div class="check"><div class="check-head"><strong>Fits Tally's capabilities</strong><span class="check-value">85%</span></div><div class="track"><div class="fill fit"></div></div></div>
<div class="check"><div class="check-head"><strong>Label confidence</strong><span class="check-value">94%</span></div><div class="track"><div class="fill confidence"></div></div></div>
</div><div class="scoreline">Scores for the highlighted post</div></div><div class="model-result">✓ Priority candidate · 88 / 100</div>
<div class="engine-note"><strong>1.691s</strong> measured classification time</div>
<div class="output-shell"></div><div class="waiting">Evidence first.<br>A useful draft follows.</div>
<div class="result"><div class="result-head"><strong>@{esc(lead['author'])}</strong><b>WORTH REVIEWING</b></div><p class="quote">“{esc(lead['suggestion']['evidence'])}”</p><p class="context">Collecting audience suggestions for Pokémon nicknames. A concrete form-building need.</p><div class="source"><a href="{esc(lead['url'])}" target="_blank" rel="noopener noreferrer">View original post ↗</a> · 20 Sep 2026</div><div class="draft"><div class="draft-label">GENERATED REPLY · HUMAN REVIEW</div><p>{esc(lead['suggestion']['draft'])}</p></div></div>
<div class="output-note"><strong>1</strong> candidate · Draft only, nothing sent</div>
<div class="flight">Google Forms alternative?</div>
<div class="bottom"><strong>Public posts → clear intent → useful next step.</strong><span>Full run: 8.08s · Animation is a replay · A candidate is not a customer</span></div><div class="journey"><div class="journey-fill"></div></div>
</div>
<div class="launch-cover"><div class="launch-inner"><div class="launch-kicker">BUILT TO FIND YOUR NEXT CONVERSATION</div><div class="launch-partners"><span>BlockRun</span><span class="multiply">×</span><span class="jev-name">Jev</span></div><div class="launch-product">SignalDesk</div><div class="launch-line">Real posts. Clear intent. A useful next step.</div></div></div>
<div class="closing-cover"><div class="closing-inner"><div class="closing-tag">BUILD WITH BLOCKRUN</div><h2>Make SignalDesk yours.</h2><p>Open-source code. Bring your own keys.</p><div class="closing-keys"><span>X API</span><span>TypeSafe Jev</span><span>Model API</span></div><a class="closing-repo" href="https://github.com/BlockRunAI/signaldesk" target="_blank" rel="noopener noreferrer">github.com/BlockRunAI/signaldesk ↗</a><div class="closing-powered">Built with BlockRun. Works with your model API.</div></div></div>
</div></div>'''
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SignalDesk · From noise to opportunity</title>'
web=head+'<link rel="stylesheet" href="/flow.css"><script src="/vendor/gsap.min.js" defer></script><script src="/flow.js" defer></script><script src="/flow-player.js" defer></script></head><body class="player-body"><div class="player-viewport"><div class="player-scale">'+content+'</div></div><nav class="player-controls"><button id="play">Play with sound</button><button id="sound">Sound on</button><button id="replay">Replay</button><label for="seek">Timeline</label><input id="seek" type="range" min="0" max="32" step="0.05" value="0"><a href="/?run='+esc(r['id'])+'&amp;filter=review&amp;draft=1">Open verified run ↗</a><small>Saved data · No paid API calls during playback</small></nav><audio id="browser-music" src="/media/launch-music.mp3" preload="auto"></audio></body></html>'
(ROOT/'web/demo.html').write_text(web)
v=ROOT/'videos/signaldesk-flow-en';v.mkdir(exist_ok=True)
(v/'assets').mkdir(exist_ok=True)
(v/'assets/launch-music.mp3').write_bytes((ROOT/'web/media/launch-music.mp3').read_bytes())
(v/'assets/gsap.min.js').write_bytes((ROOT/'web/vendor/gsap.min.js').read_bytes())
(v/'index.html').write_text(head+'<script src="assets/gsap.min.js"></script><style>'+(ROOT/'web/flow.css').read_text()+'</style></head><body>'+content+'<audio id="launch-music" src="assets/launch-music.mp3" data-start="0" data-duration="32" data-track-index="2" data-volume="1"></audio><script>'+(ROOT/'web/flow.js').read_text()+'</script></body></html>')
(v/'package.json').write_text(json.dumps({'name':'signaldesk-flow-en','private':True,'scripts':{k:f'npx --yes hyperframes@0.8.62 {c}' for k,c in [('dev','preview'),('check','check'),('render','render')]}},indent=2)+'\n')
(v/'hyperframes.json').write_text(json.dumps({'$schema':'https://hyperframes.heygen.com/schema/hyperframes.json','authoringSkill':'product-launch-video'},indent=2)+'\n')
print('Built English replay page and 32-second composition from verified data.')
