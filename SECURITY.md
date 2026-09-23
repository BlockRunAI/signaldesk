# Security

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for this repository:
https://github.com/BlockRunAI/signaldesk/security/advisories/new

Include the affected commit, reproduction steps using synthetic credentials,
impact and any proposed fix. Do not put live keys, private posts or exploit
credentials in public issues or pull requests. If a credential is exposed,
revoke it at its provider; removing the text from a commit is not revocation.

## Supported scope

Security fixes target the current `main` branch. SignalDesk is a local,
single-user demo, not an authenticated hosted service. Keep it bound to loopback.
See [architecture](docs/architecture.md) for supported deployment and storage.

Stored keys stay on the backend; UI configuration responses expose presence
flags only. Explicit non-secret model settings are returned for editing. Keys
are sent to their selected service endpoints with redirects disabled. Changing
a saved custom model destination requires entering its key again.

`.env`, run histories and bulk data are ignored. Optional dotenv persistence uses
an owner-readable file; files are not encrypted at rest. Run snapshots contain
public-post text and drafts. Protect the local machine and remove old runs when
no longer needed. Do not upload your workspace wholesale in a bug report.

Offline CI uses synthetic credentials, makes no paid requests, and scans Git
history with Gitleaks. Passing a scan is a useful check, not proof that every
possible secret or vulnerability has been detected.
