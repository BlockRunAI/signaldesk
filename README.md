# SignalDesk

**People are asking for what you sell. Find the conversations worth having.**

A local customer-discovery demo: company website → public X posts → Jev intent
classification → evidence-linked opportunities and reply drafts. No messages are
sent. Works with any business whose product facts and relevant public posts are
available, not just AI companies.

## Selected real demo

**Form builders: find someone asking for a Google Forms alternative.** A live
Tally run returned 25 records, classified 23 unique posts, and selected one
candidate for review. Jev took 1.691 s; the complete workflow took 8.08 s.
[Original request](https://x.com/MisWiredKE/status/2101589197890977975),
[validation notes](docs/live-validation.md), and
[English continuous video project](videos/signaldesk-flow-en/README.md).

Open [the animated workflow](http://127.0.0.1:8787/demo) for a 32-second,
three-column replay with a BlockRun × Jev opening, scrolling posts, Jev scores, an evidence-linked
reply draft, and instrumental background music. The app UI is English. Replay never starts a paid run.

## Run locally

Python 3.11+, no third-party Python packages required.

```sh
git clone https://github.com/BlockRunAI/signaldesk.git
cd signaldesk
python3 -m signaldesk serve
# Open the page and choose Connect your APIs.
# Or copy .env.example to .env and set keys there.
# http://127.0.0.1:8787
```

Choose a text model: **BlockRun** (recommended) or **your own OpenAI-compatible API**.
The custom option uses `LLM_API_KEY`, `LLM_BASE_URL` and `LLM_MODEL` with
`CHAT_PROVIDER=custom`. Models must support Chat Completions, `max_tokens`,
`temperature=0`, and JSON-object output. Native APIs with a different request
format are not interchangeable. Compatible-provider support is tested offline;
a particular provider/model needs its own live validation.

`TYPESAFE_API_KEY` is still required for **official TypeSafe Jev**. X search uses
its own provider credential. BlockRun is optional: without its website extraction,
enter a factual **Product context** and use X, TwitterAPI.io or imported posts.
This version does not relabel BlockRun's separate OpenJev implementation as official Jev.
The UI shows the actual Jev model and per-stage request records.

Choose an X provider:

| Provider | Key | Coverage / status |
|---|---|---|
| TwitterAPI.io | `TWITTERAPI_KEY` | Dedicated original-post search, Latest order, cursor paging; adapter implemented, requires credential for live validation |
| X official | `X_BEARER_TOKEN` | Live validated September 22: Recent Search, author expansion, timestamps and long-post text; recent seven-day coverage |
| Exa through BlockRun | Existing BlockRun key | Web-index fallback only; may return zero X posts. Not a substitute for a dedicated X feed |
| Import | No search key | JSON from an existing supplier/export; explicitly labeled as imported evidence |

The app reads keys from `.env` or an explicitly supplied local file:
`python3 -m signaldesk --env /path/to/local.env serve`.
Keys stay on the backend. The custom model key is sent only to its explicitly
configured HTTPS Base URL; BlockRun, Jev and X credentials retain their fixed
provider origins. HTTP redirects are disabled, and no cross-provider fallback occurs. It never reads browser cookies or X account passwords.

## First-run setup

**No keys needed to watch:** open `/demo`, then click **Play with sound**.

**For live discovery:** expand **Connect your APIs** on the home page and enter:

| Credential | Used for | Where to obtain it |
|---|---|---|
| Model API key + Base URL + Model ID | Product understanding and reply drafting; select My own API | Your chosen OpenAI-compatible provider |
| BlockRun API key | Recommended model option; optional website extraction / Exa search | https://user.blockrun.ai |
| TypeSafe Jev API key | Official Jev classification | https://typesafe.ai |
| X API Bearer Token | Original public posts, recent seven days | https://console.x.com |
| TwitterAPI.io key | Optional alternative X provider | https://twitterapi.io |

Keep **Save locally in .env** unchecked for a session-only setup, or check it to
persist in an owner-readable file (0600). Blank fields preserve existing keys;
changing a saved custom Base URL requires entering the destination's model API key again;
existing secrets are never sent back to the browser. Settings cannot change during
a run. The server must remain local. Saving validates input and configuration;
provider credentials/access are checked when a live request is made.

The public BlockRun catalog currently distinguishes **OpenJev** from official
**TypeSafe Jev**. This demo uses the latter directly and requires its separate
key. The BlockRun × Jev opening describes this combined workflow, not a claim
that official Jev is available through BlockRun's gateway.

Start with a small live run. Search needs a funded provider account; replay is
free of API calls. Provider failures appear as actionable errors with no automatic
paid retry. Data and run history stay on this machine.

## Command line

Example custom model configuration (the Base URL includes the API prefix):

```dotenv
CHAT_PROVIDER=custom
LLM_API_KEY=your-provider-key
LLM_BASE_URL=https://api.your-provider.com/v1
LLM_MODEL=your-model-id
TYPESAFE_API_KEY=your-jev-key
X_BEARER_TOKEN=your-x-token
```

With this setup, supply `--brief` (or Product context in the UI). No BlockRun
key is needed. Exa website extraction and Exa search remain optional BlockRun services.

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
2. Your selected text model extracts capabilities, limitations and search phrases.
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

## License and contributions

SignalDesk's original code is MIT licensed. See [LICENSE](LICENSE),
[third-party notices](THIRD_PARTY.md), and [contribution guide](CONTRIBUTING.md).
Offline CI uses no API keys and performs no paid calls.
