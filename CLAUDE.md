# Instructions for agents working in this repository

Stratah is an evidence-weighted encyclopedia. Read `CONTRIBUTING.md` (the rules) and
`build/SCHEMA.md` (the file formats) before changing content.

## Never push to `main`

All changes go through `docs/REVIEW.md`:

1. Work on a branch (`dig/<subject>`, `fix/<subject>`, `bounty/<id>`, `process/<topic>`).
2. Run `python3 build/conformance.py --base origin/main`. Zero errors.
3. Open a pull request into `main`.
4. Hand the PR to a **separate** review agent that has not seen your work, with only the PR number,
   the repository and `docs/REVIEW.md`. Do not review your own PR.
5. The review agent posts its verdict on the PR and merges only on APPROVE. Changes to the gate
   itself (the "What only the owner merges" list in `docs/REVIEW.md`) are escalated to the owner,
   never merged by an agent.

## Content rules that are easy to get wrong

- Wikipedia is never an anchor. Summaries and search snippets are not primary reads.
- `anchor_checked: primary` means the document itself was opened and read. Say what was blocked.
- Absence of a record is capped at provisional (`absence_anchor: true`).
- How a myth spread goes in `transmission.yaml`; it never supports a claim.
- Logs are append-only. Corrections are new entries.
- Surface lines (headline, summaries) are plain and true. No hype.
