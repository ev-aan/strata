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
5. The review agent posts its verdict on the PR and merges only on APPROVE. Changes to rules,
   `CONTRIBUTING.md`, `SCHEMA.md`, `conformance.py` or `docs/REVIEW.md` are escalated to the owner,
   never merged by an agent. "Rules" means everything on the owner-only list in `docs/REVIEW.md`
   ("What only the owner merges"), which matches `.github/CODEOWNERS`: all of `docs/`, the schema,
   validator and tools, `build/site.yaml`, `build/news.yaml`, `build/taxonomy.yaml`, `.github/` and every `review.yaml`.

## Content rules that are easy to get wrong

- Wikipedia is never an anchor. Summaries and search snippets are not primary reads.
- `anchor_checked: primary` means the document itself was opened and read. Say what was blocked.
- Anchor format (SCHEMA N25): every claim has ONE `anchor:` mapping with `type` and `description`, optional `sources: [manifest ids]` and `nodes`. Never `anchors:` or `ref:`. Searched gaps use `type: search-record`. Conformance fails otherwise.
- Absence of a record is capped at provisional (`absence_anchor: true`).
- How a myth spread goes in `transmission.yaml`; it never supports a claim.
- Logs are append-only. Corrections are new entries.
- Surface lines (headline, summaries) are plain and true. No hype.

- Never change `build/SCHEMA.md`, `build/conformance.py` or the rules to get a result someone prefers. A change needs a proposal that meets `docs/SCHEMA_PROPOSALS.md`, even if the owner asks in conversation; draft the proposal instead.

## Other gates (reconciled 2026-10-02)

- A subject only goes on the site if `build/subjects/<subject>/review.yaml` has status `passed` or `passed_with_open_items`
  (`docs/PUBLISH_GATE.md`). The independent review agent writes it; the author never does.
- Public challenges and submitted evidence are admitted only if they pass S1 to S5 (`docs/CHALLENGES.md`). Counts, reactions and
  repeats carry no weight; an automated step never admits or declines one.
- Nodes, windows, statement kinds, reasons behind confidence and the assessment block follow `build/SCHEMA.md` (N1 to N24).

