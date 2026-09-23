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

## Current English video deliverable

User revision: English for X, with a more fluid end-to-end workflow similar to
the reference. The current cut is `videos/signaldesk-flow-en`: 32 seconds,
1920×1080, 60 fps, with instrumental background music. Local artifact:
`videos/signaldesk-flow-en/renders/signaldesk-launch-blue.mp4`.

One persistent three-column canvas replaces the first cut's separate slides:
rolling original-post excerpts → Jev API intent/fit/confidence → source evidence
and generated reply draft. The full UI and controls are English. The shared
web player at `/demo` supports pause, replay and seeking without paid requests.
The original 30-second Chinese first cut remains in `videos/signaldesk-forms`
for history and is no longer the preferred social demo.

All visible posts are attributed literal excerpts from the verified run. Six
selected excerpts illustrate the feed; the measured run counts are 25 returned,
23 unique and one priority candidate. The original quote, measured 1.691-second
classification and 8.08-second total remain accurate. The animation is explicitly
a paced replay. It does not represent real-time API execution or a conversion.

The editable video and browser page are generated from the same source files;
see the current video README for build/render instructions. No social post or
outreach was sent as part of this revision.

Current review status: repository remains private at the owner's request until the branded video is approved. The MIT license and open-source onboarding are prepared; no public release has occurred.
