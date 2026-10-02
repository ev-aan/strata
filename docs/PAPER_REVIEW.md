# Reviewing an academic paper (process v0.1, 2026-10-02) — PARKED, see docs/FUTURE.md

Owner decisions: the paper itself stays private; only the review is published; no finding changes a dig by itself. Every finding is a proposal that must pass the project's criteria and then be approved by the owner.

## Where things live
- `private/papers/<paper-id>.pdf`: the uploaded paper. `private/` is git-ignored and never published.
- `build/nodes/paper-<paper-id>.yaml`: a `document` node for the paper (citation, date, sha256 of the file, `rights: unknown` until checked, `source_gap` if the paper's own sources are not open). It carries no copy of the text.
- `reviews/<paper-id>.yaml`: the review (below). This is public.

## Steps
1. **Record.** Create the paper's node. Quote it only in short passages, each with a page number.
2. **Extract.** List what the paper asserts: dated facts, quotations it reports from other sources, numbers, and its conclusions, each with a page reference.
3. **Compare** with the named dig's claims and nodes. Each assertion gets one result: `new`, `confirms`, `conflicts`, or `not_in_dig`.
4. **Check the paper.** Quotations against sources we hold (page images, OCR), dates against our nodes, arithmetic, and citations that cannot be found. Findings are `error`, `unsupported`, `gap_in_paper`, or `gap_in_dig`.
5. **Propose.** Each finding that would change the dig is written as a proposal: a new node, a new revision of a node, a new or changed claim, or a note.

## Review file
```
paper: <paper-id>            # node id
dig: <subject>
reviewed: <date>
reviewer: <who ran it>
findings:
  - id: f-01
    kind: new | confirms | conflicts | error | unsupported | gap_in_paper | gap_in_dig
    page: <page in the paper>
    quote: <short passage, at most about 25 words>
    touches: [claim or node ids]
    checked_against: <the source read, and how>
    result: <what was found>
    proposal: {type: new_node | node_rev | new_claim | claim_change | note | none, detail: ...}
    criteria: {anchor_read: yes|no, authenticity: pass|fail|untested, evidence_class: ..., would_change_if: ...}
    decision: pending | accepted | rejected | deferred      # set by the owner only
```

## The criteria a proposal must meet before it can be accepted
A proposal is only offered for approval if it passes these; otherwise it stays `pending` with the reason.
- C1. It rests on a source that was read directly (`anchor_read: yes`), not on the paper's own summary of that source. A paper is a secondary source for what it cites.
- C2. Authenticity of that source is tested (A-rules in `build/SCHEMA.md`).
- C3. A new claim states its evidence class, its confidence, what would change it, and keeps evidential and adoption weight separate.
- C4. A paper's conclusion is filed as the paper's claim (interpretive, attributed to its authors), never as a finding of the dig by itself.
- C5. It passes `python3 build/conformance.py` after the change.
- C6. Nothing is overwritten: changes are new node revisions and new log entries.
