# SignalDesk demo: data sourcing and final short video

Updated: 2026-09-22 Pacific. The selected demo is Tally / form builders.
Official X retrieval, Jev classification and the positive reply-draft path are
validated with a real public post. See `live-validation.md` for measured results.

## Reference demo

Inspected the original Jasper Li post, its tutorial reply, the linked Monid blog
and public SKILL.md. None supplied a source repository for this particular demo.
This is a bounded observation, not a claim that Monid has no public repositories.
The tutorial supplies prompts and reports TikHub as the TikTok search/data source.

- https://x.com/Jasperli0122/status/2102140451763749077
- https://monid.ai/blog/jev-viral-ugc
- https://monid.ai/SKILL.md

## Data acquisition

Use the official X provider, now configured and live validated, for this demo.
TwitterAPI.io remains an alternative adapter with keyword search and cursor
paging. Its public rate on the date above is $0.15/1K tweets,
with per-call minimums. 100 returned tweets correspond to $0.015 at the item rate,
not a quote for the whole workflow or a guarantee about unique usable posts.
X official is the alternative: $0.005/read post, about $0.50 for 100 post resources;
user expansions and other resources can incur additional charges.

- https://twitterapi.io/pricing
- https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search
- https://docs.x.com/x-api/getting-started/pricing

Initial sampling plan: one real business, three query families (recommendation
requests, explicit alternatives, concrete product-category complaints), a recorded
date window, and up to 100 unique original posts. Preserve irrelevant posts in the
audit so the demo can visibly show meaningful filtering. Do not pad counts.

Record source provider, exact query, retrieval time, original post ID/URL/text and
creation time. For the top candidates, inspect the original post and any required
thread context before calling them relevant. Fetching thread context is a planned
follow-up; it is not implemented in the initial adapter. Do not infer author
details from handles or assume a complaint implies a purchase.

For filming, freeze the verified collection snapshot. Label its acquisition date;
run Jev on it and show separately measured classification time. If showing a saved
run, label it as a replay. Do not pass a sped-up recording off as actual latency.
Company facts come from the company website, not from a text model's memory.

## Final video deliverable

A 30-second, 1920×1080 MP4 with Chinese on-screen text and no audio. Editable
HyperFrames sources live in `videos/signaldesk-forms`; local output is
`videos/signaldesk-forms/renders/signaldesk-demo.mp4` (ignored delivery artifact).

1. 0–8s: Enter tally.so; ask who is looking for a form-tool alternative.
2. 8–18s: Show 25 returned records → 23 unique posts → 1 priority candidate.
   Separate 1.691-second Jev classification from the 8.08-second full workflow.
3. 18–30s: Show the actual Google Forms alternative request, supporting evidence
   and generated draft. Identify it as a candidate, with human review and no autosend.

All product UI is a capture of the actual saved run, labeled as a real-data replay.
The original post URL and timestamp remain available in the app. The MP4 is a
presentation of the result, not a real-time screen recording. The synthetic
positive fixtures and earlier negative controls are excluded from the video.

Replaying the saved run or rendering this project causes no paid discovery calls.
A fresh live run needs configured keys and may return different recent posts.
