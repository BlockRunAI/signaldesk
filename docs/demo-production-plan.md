# SignalDesk demo: data sourcing and final short video

Updated: 2026-09-22. Production plan; official X retrieval and classification now
work with real posts. No finished video or validated priority-lead dataset yet.

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

Target: a 25–35 second MP4, based on actual SignalDesk UI and verified posts,
plus an optional 6–8 second loop for X. HyperFrames product-showcase workflow.
Proposed 16:9 main cut for readable desktop UI, with concise English captions for
X; these are production defaults, subject to the user's later direction.

1. 0–4s: “Someone is asking for what you sell.” Enter a real company URL.
2. 4–10s: Show the actual collected posts, source and date window.
3. 10–18s: Jev labels and filters; reveal measured count and classification time.
4. 18–27s: Expand a genuine request, its product match and original-post evidence.
5. 27–32s: Show the reply draft, acquisition cost separately from analysis cost,
   and SignalDesk / BlockRun branding. No automatic outreach.

Do not film the current two promotional negative controls as a successful
customer-discovery example. Positive model fixtures are explicitly synthetic
tests and are not eligible for the marketing lead count. Production of the final
customer demo depends on obtaining and validating the real source dataset.
