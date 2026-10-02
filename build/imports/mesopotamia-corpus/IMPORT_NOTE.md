# Import note: Mesopotamian flood corpus

Provenance: uploaded by the owner on 2026-10-02 from the earlier Strata dig on the tablets. Copied here **verbatim and unedited**. Original files are the record; corrections go in new log entries, not edits.

Files: `sumerian_flood_story.yaml`, `atra_hasis.yaml`, `enuma_elish.yaml`, `threads.yaml`, `validate_threads.py`, `flood_narrative.md`.
Not yet received: the Gilgamesh subject file (`gilgamesh:tablet-xi-flood` is referenced by `thread-flood-transmission`), the full retranslation, the main eight-rule validator, and the live schema document.

## Mechanical check run here (2026-10-02)
- `validate_threads.py`: **pass, 1 warning.** 26 claims, 3 subjects, 4 threads. Warning: `gilgamesh:tablet-xi-flood` does not resolve (expected; the file is missing). Firewall (T2): 33 anchors, 0 threads cited as evidence.
- All three subject files parse. Claim states: 15 established, 8 contested, 3 proposed. No `refuted` or `searched_gap` claims.

## Issues found (not fixed here)
1. **Wikipedia cited as an anchor.** `atra-hasis:ah-date-colophon`, anchor 2: "Wikipedia/CDLI summaries concur on the Ammi-saduqa colophon". Under the owner's 2026-10-02 rule (Wikipedia is never an anchor) this needs re-anchoring to CDLI or the Lambert and Millard edition. Not edited, to keep the import verbatim; correct in a new entry once the main validator is available.
2. **Evidence-class spelling:** these files use `primary-text` (hyphen); CONTRIBUTING.md uses `primary_text` (underscore). One must be chosen and the validator must enforce it.
3. **Schema differs from build/SCHEMA.md v0.1** (see the Reconciliation section there).
4. **Fields CONTRIBUTING.md requires but these files do not carry:** separate evidential and adoption weights, `anchor_checked`, `would_change_if`, `next_step` on gaps. They may live in the main validator or live schema, which we have not seen.
