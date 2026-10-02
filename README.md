# Stratah

**What do we actually know?** Stratah is an evidence-weighted record. Each excavation takes one question, often one surrounded by myth or dispute, and files every claim with its sources, how confident we are, and what would change our mind. Evidence and popularity are kept apart. Publishing is not the end: findings stay open to challenge, new evidence and correction.

Site: https://stratah.org

## How it works
- **YAML is the source of truth.** Claims, sources, timelines, logs and shared nodes live in `build/`. The website is generated from them (`python3 build/tools/build_site.py`).
- **Every claim** states its evidence class, confidence, whether its source was read directly, and what would change it. Evidential weight and adoption weight are never combined.
- **Nothing goes live unreviewed.** An independent reviewer, never the author, checks each dig and sends specific requests back before it is published (`docs/PUBLISH_GATE.md`).
- **The validator** (`python3 build/conformance.py`) enforces the mechanical rules; it must report 0 errors.

## Take part
- Challenge a finding or submit evidence: use the button on any claim, or the "Challenge a finding" issue form. Rules: `docs/CHALLENGES.md`.
- Suggest a topic or a News Review: use the issue forms.
- Run your own dig with your own AI: copy the rules from https://stratah.org/start/ (`docs/AGENT_RULES.md`) and submit a draft pull request from a branch `dig/<subject>`.
- Read first: `CONTRIBUTING.md` (the rules), `docs/GOVERNANCE.md` (who decides what), `build/SCHEMA.md` (file formats).

Rules, the schema and the validator change only through a proposal that meets `docs/SCHEMA_PROPOSALS.md`.

## Licences
Written content (pages, claims, findings, logs, timelines): **CC BY 4.0** (`LICENSE-CONTENT.md`). Reuse with credit to "Stratah (stratah.org)", a link to the page and to the licence, and a note of any changes. Code: MIT (`LICENSE`). Historical sources keep their own status.
