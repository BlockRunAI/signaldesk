# Live integration findings — 2026-09-22

## Confirmed

- TypeSafe `POST /v1/systemone`, pinned `jev-1.13.0`: HTTP 200. A small
  recommendation-intent probe returned a typed `noul` result and token usage.
- BlockRun `GET /v1/surf/search/social/posts`: HTTP 410, endpoint retired
  September 6. Do not build a workflow against stale MCP descriptions.
- BlockRun `POST /v1/exa/search` with `category: tweet`: HTTP 400, upstream says
  that category is no longer supported. No charge indicated for this rejection.
- Exa's supported domain filter / ordinary search returned HTTP 200 but zero
  posts for both tested travel-eSIM queries. BlockRun reported $0.010 per call.
  Empty search results still have a cost; success status does not imply usable data.
- The currently available browser X search redirects to login.

## Dedicated X provider

The repository supports TwitterAPI.io and the official X Recent Search API.
The official X adapter was live validated after the user configured and funded
their developer account. TwitterAPI.io remains unverified against a live account.
The app fails before any paid company calls when the selected search credential
is missing.

### Official X live runs

On September 22, three Airalo/eSIM queries returned 20, 40 and 29 valid posts
respectively. These are 89 records across batches (88 unique post IDs), not 89
customers. Company-site extraction and official Jev classification completed in
all three runs. Jev wall times were 0.836 s, 1.083 s and 0.791 s respectively.
The second and third runs requested long-post content (`note_tweet`), avoiding
classification of truncated previews. A regression test covers that behavior.

No post met the existing priority-review rule. Manual inspection found promotions,
carrier support requests, phone-hardware requests and some travel-related needs
requiring further research. Thresholds were not relaxed. Consequently the live
positive draft path and a successful customer-discovery marketing example remain
unverified; the synthetic contract check below is separate evidence only.

After these calls, the X console showed $0.45 current spend and $4.55 remaining
from the initial $5 credit purchase. This is an account-level UI observation,
rounded to cents, not per-run API billing metadata or a total workflow cost.
Three Exa page reads reported $0.006 combined; Jev costs are estimates and chat
costs still lack the header consumed by this app. Do not advertise a full cost.

The local server now loads its ignored, owner-readable `.env` with X configured.
No credentials or collected post datasets are committed to this repository.

## Acceptance criteria for a publishable demo

- Retrieve original posts using a working dedicated data provider.
- Preserve per-post IDs, text, timestamps and direct source links.
- Inspect the priority results manually for actual business relevance.
- Display real counts and timings; do not fill empty lists with invented leads.
- Separate retrieval cost, Jev estimate and text-generation cost.
- Record the source date window and label cached/imported runs accurately.

The empty index-search probes do not establish that no matching X posts exist.
They establish that these search routes did not supply usable posts in these calls.

## Completed end-to-end import run

The two public Jasper Li posts previously inspected in the browser were imported
as a negative-control dataset. Creation timestamps were derived from their X
snowflake IDs and matched the observed page times. No customer posts were invented.

- Company: Monid, website extraction via BlockRun/Exa succeeded.
- Company-profile extraction via BlockRun chat succeeded.
- Official Jev model: `jev-1.13.0`.
- Two valid posts, six typed questions; Jev request wall time **381.2 ms**.
- Both posts were categorized as promotional/noise and excluded. **Zero leads**
  is the expected result for this dataset, not proof of lead-discovery quality.
- Exa company-content cost reported by BlockRun: $0.002.
- Jev: 2,322 input tokens; estimated cost $0.000097524.
- The chat response did not provide the cost header consumed by the adapter, so
  chat cost remains **unknown**. No total-cost marketing claim is warranted.
- The run is available locally in the UI's history, but raw runs are not committed.

## Positive-path model contract check

`scripts/live_contract.py` runs an opt-in paid test using three **synthetic**
fixtures, stored separately from real runs. All five checks passed:

1. Explicit Japan eSIM recommendation request selected for review.
2. A customer explicitly requiring a physical SIM excluded (product mismatch).
3. Affiliate promotion excluded.
4. Generated evidence was an exact substring of the supplied fixture.
5. A reply draft was produced.

The three-post Jev call took 294.6 ms. These are integration tests, not discovered
customers, and must never be included in a marketing lead count.

## Local verification

- 14 offline tests cover normalization, stale/future data, deduplication, paging,
  provider errors, malformed model answers, source-quote validation, exclusions,
  missing credentials, CSV formula handling and redirect behavior.
- Python compilation and JavaScript syntax checks pass.
- Browser verification: startup, configured/missing credentials, real-run replay,
  exclusion filtering, source-link targets and visual layout.
