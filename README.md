# SignalDesk

**People are asking for what you sell. Find the conversations worth having.**

A local customer-discovery demo: company website → public X posts → Jev intent
classification → evidence-linked opportunities and reply drafts. No messages are
sent. Works with any business whose product facts and relevant public posts are
available, not just AI companies.

## Run locally

Python 3.11+, no third-party Python packages required.

```sh
cp .env.example .env
# Set your keys in .env, then:
python3 -m signaldesk serve
# http://127.0.0.1:8787
```

Required: `BLOCKRUN_API_KEY` for company extraction and short text generation,
`TYPESAFE_API_KEY` for **official TypeSafe Jev**. This version intentionally does
not relabel BlockRun's separate OpenJev implementation as official Jev.
The UI shows the actual returned model and per-stage request records.

Choose an X provider:

| Provider | Key | Coverage / status |
|---|---|---|
| TwitterAPI.io | `TWITTERAPI_KEY` | Dedicated original-post search, Latest order, cursor paging; adapter implemented, requires credential for live validation |
| X official | `X_BEARER_TOKEN` | Recent Search; last seven days, author expansion and timestamps; adapter implemented, requires credential for live validation |
| Exa through BlockRun | Existing BlockRun key | Web-index fallback only; may return zero X posts. Not a substitute for a dedicated X feed |
| Import | No search key | JSON from an existing supplier/export; explicitly labeled as imported evidence |

The app reads keys from `.env` or an explicitly supplied local file:
`python3 -m signaldesk --env /path/to/local.env serve`.
Keys stay on the backend and are only sent to fixed provider origins, with HTTP
redirects disabled. It never reads browser cookies or X account passwords.

## Command line

```sh
python3 -m signaldesk run --url https://www.airalo.com --provider twitterapi \
  --query '"esim" (recommend OR alternative OR "looking for")' --days 30 --limit 60

python3 -m signaldesk run --url https://your-company.com --provider import \
  --posts /path/to/posts.json --brief 'Documented product capabilities and limits'

python3 -m unittest discover -s tests -v
```

Optional paid model integration check (synthetic test data, not real leads):
`python3 scripts/live_contract.py --env .env`.

Imported JSON is an array. Every row requires an original post URL, text and a
timezone-qualified timestamp: `url`, `text`, `created_at` (or `createdAt`).
TwitterAPI.io's exported `url`, `text`, `createdAt` shape is accepted directly.
Imports are not independently authenticated. Review source links before outreach.

## Pipeline

1. Extract company website text through Exa, or use the supplied product brief.
2. A BlockRun text model extracts capabilities, limitations and search phrases.
3. Search up to four queries, two pages each, with a maximum of 100 eligible
   posts. Explicit query overrides are supported. Search collection can stop
   short of the requested count; the UI always displays actual counts.
4. Reject malformed links, missing dates, duplicates, reposts and stale posts.
5. Official Jev evaluates three independent questions per post: category,
   documented product fit, and explicitly expressed action intent. Batches of 15
   posts share state; each question explicitly references its post index.
6. A transparent rule ranks posts. Only seeking/switching + fit ≥ .75 + intent ≥
   .75 + category confidence ≥ .5 enters the priority queue. These thresholds are
   initial demo choices, not validated conversion predictors.
7. A text model drafts suggestions for the first five priority posts. Source
   quotes must be exact substrings of the original post or the run fails.
8. View results, filter categories, replay a saved run without spending, or export
   CSV. Reply suggestions are drafts only.

## Evidence and costs

Every run saves `runs/<uuid>.json` with original public text, canonical URLs,
timestamps, text hashes, search queries, rejected-row counts, model outputs,
stage timings and cost records. Runs and data are gitignored. Failed runs retain
partial evidence and are visibly marked failed; an empty search is not success.

BlockRun's `X-BlockRun-Cost-USD` header is recorded as **provider-reported cost**.
Official Jev currently returns token usage without a settlement receipt, so its
cost is labeled an **estimate** using $0.042/M input tokens (verify your account's
pricing). Dedicated X suppliers without a cost header remain **unknown**, never
silently zero. The board's known subtotal is not necessarily the final bill.

Requests are bounded by 20 calls/run, 100 posts and response/input size limits;
these are workload limits, not a dollar-budget guarantee. There are no automatic
paid retries. A timeout may still incur a charge. Set account spending limits at
your providers before large or repeated runs.

## Local security and scope

The server binds to loopback only. It restricts Host, checks a per-process token
and Origin for paid mutations, disallows cross-origin framing, escapes displayed
source text, and serves only UI files and selected run JSON/CSV—not `.env`.
CSV exports neutralize spreadsheet formulas. No analytics, external fonts or
remote assets are loaded by the frontend.

This is a local demo, not an internet-facing multi-tenant service. Before hosting,
add user authentication, per-user storage, rate/spend limits and a data-retention
policy. No deployment or social posting is part of this repository.

## References

- [TypeSafe request / response schema](https://docs.typesafe.ai/api)
- [TwitterAPI.io Advanced Search](https://docs.twitterapi.io/api-reference/endpoint/tweet_advanced_search)
- [X Recent Search](https://docs.x.com/x-api/posts/search/introduction)
- [Exa Search](https://exa.ai/docs/reference/search)
- [Live integration findings](docs/live-validation.md)
