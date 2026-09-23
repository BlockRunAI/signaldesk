# SignalDesk · English continuous workflow

The current social demo: 32 seconds, 1920×1080, 60 fps, with instrumental background music. Supersedes the
three-scene Chinese first cut in `../signaldesk-forms`.

Open `http://127.0.0.1:8787/demo` after `python3 -m signaldesk serve`.
The browser player supports play/pause, replay, seeking, soundtrack controls and reduced-motion mode.
All source links point to actual public posts. Playback makes no provider calls.

```sh
npm run check
npm run render -- --fps 60 --quality delivery --output renders/signaldesk-launch.mp4
```

`index.html` is generated from the shared web replay assets. To rebuild after an
edit, from the repository root (requires the owner's ignored verified run):

```sh
python3 scripts/build_flow_demo.py runs/21db965b-a824-4121-bb35-8df2972ffee0.json
```

Canonical files: `web/flow.css`, `web/flow.js`, `web/flow-player.js`, and
`scripts/build_flow_demo.py`. The checked-in HTML includes six literal, attributed
post excerpts, one source quote and the original generated draft. Bulk collected
posts and credentials stay ignored. The selected request was verified in X.

Numbers: 25 returned records, 23 unique posts, 21 noise, one further-research
item, one priority candidate. Jev 1.691 seconds; full run 8.08 seconds. The video
is a paced replay, not a real-time recording. Scores are not conversion rates.
Tally is an example product, not a partner. Free usage has fair-use conditions;
a complete Sheets replacement is not established. No outreach was sent.

Reference: https://x.com/Jasperli0122/status/2102140451763749077
We inspected the original clip's persistent three-column progression and built
our own layout and animation using SignalDesk's real run data.

GSAP 3.14.2 is vendored with its copyright/license header intact:
https://gsap.com/standard-license . No runtime CDN is required by the demo page.
The optional HyperFrames CLI is pinned to 0.8.62 for reproducible rendering.

Opening: BlockRun × Jev → SignalDesk. Closing: bring your own X, TypeSafe Jev and BlockRun keys. The 24-second main sequence is retained between four-second brand bookends. See ../../THIRD_PARTY.md for music provenance.
