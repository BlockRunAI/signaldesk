# Contributing

Python 3.11+; the app needs no third-party Python dependencies.

1. Fork and clone the repository.
2. Run `python3 -m unittest discover -s tests -v`.
3. Run `python3 -m signaldesk serve` and open http://127.0.0.1:8787.
4. Use `/demo` without keys, or enter your own keys in **Connect your APIs**.
5. Make a focused change and include validation in your pull request.

Keep credentials, raw provider responses and bulk post datasets out of commits.
Use synthetic data in tests; keep live validation opt-in. Do not send outreach
from tests or automatically retry paid requests. Preserve source provenance,
exact quote checks and the distinction between a candidate and a customer.

The no-key walkthrough lives in `web/demo.html`, `web/flow.css`, `web/flow.js`
and `web/flow-player.js`. Keep its attribution and replay labeling intact.
Launch-film production and rendering are outside this repository's scope.

Read [architecture](docs/architecture.md) for module boundaries and supported deployment.
CI pins its Actions, checks Python/JavaScript and scans full Git history with Gitleaks. Report vulnerabilities privately using [SECURITY.md](SECURITY.md).
