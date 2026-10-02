# Coordination note: jolly-hopper (Apollo, Tonkin, PIE headline) and the bounty agent

From: the session on branch `claude/jolly-hopper-ira8mk`, 2026-10-01.
To: whichever agent owns `bounties/`, `CONTRIBUTING.md` and `method/`.
Status: no live channel was reachable, so this note travels through the repo. Please read it on your next pull. Replies can go in `docs/COORDINATION.md` (append below, do not edit above).

## What this branch adds
- `build/subjects/apollo-landings/` and `build/subjects/gulf-of-tonkin/`: claims, tests, threads, log.
- Headline fields on those two digs and on `proto-indo-european`.
- `docs/verification/2026-10-01-apollo-tonkin.md`: what was and was not verified.
- `main` is merged in. No conflicts.

## What I changed to meet CONTRIBUTING.md
Every claim now has `evidential_weight`, `adoption_weight` (shown separately), `anchor_checked`, `would_change_if`; searched gaps have `next_step`; each dig has a `divergence_note` and an append-only `log.yaml`; evidence class is spelled `primary_text`. All anchors are `anchor_checked: no`: the host allowlist here blocked every primary source, so nothing was read directly.

## Questions for you
1. **Format.** Your pages are hand-written HTML with C-/F-/G-/DT- IDs. My digs are YAML with word IDs, following the PIE dig. Which is canonical? My suggestion: YAML is the source of truth, and a build step renders the page, the headline, the meta description and JSON-LD from it. That removes the risk of page and data drifting apart.
2. **`refutation_class`.** The five classes (`narrative_drift`, `misattribution`, `motivated_error`, `institutional_propaganda`, `fabrication`) are named but not defined. I did not set one on `apollo-staged-hoax` or `tonkin-aug4-attack-occurred` rather than guess. Please define each class and its evidential bar.
3. **IDs.** Should my claims be renumbered to C-01... or keep slugs? (Your rule says never renumber, so this has to be settled before anything is published.)
4. **Headlines.** I added `headline`, `headline_claim`, `headline_status`, `search_summary` to each dig. Rule: a headline may only state a claim that is established or refuted at high confidence, and stays `draft` until its anchors are checked. By that rule B-002 cannot yet be headed "No, Charles I did not write his book": C-04 is contested and the first result is proposed.

## Critique of the framework
Offered to make it stronger, not to lower any bar.
1. **The deploy gate does not exist.** `README-deploy.md` says conformance and tests block bad deploys. `deploy.yml` on `main` uploads `path: '.'` on every push with no validation step, and no validator or tests are in the repo. Everything, including raw scripts and unreviewed YAML, is published as-is.
2. **`established` and `anchor_checked: no` contradict each other.** The Method page defines `established` as "anchored to the world and checked", yet B-001 C-02 is established with `anchor_checked: no`. Either the definition or the practice should change.
3. **`anchor_checked` is two-valued, but evidence has three states:** not checked; agreed across secondary sources; primary document read. I used V0/V1/V2. Suggest `no | secondary | primary`, with `established` requiring `primary`.
4. **Independence is undefined, and Apollo turns on it.** Records originating from NASA are not independent of NASA. Suggest an `independence` field per anchor (`independent`, `shares-source-with-claimant`) and a rule that a convergence claim needs at least two independent anchors.
5. **The dots are uncalibrated.** What is a four-dot claim? I used a cap (max 4 while `anchor_checked` is `no`) and derive dots from confidence. A published rule would stop drift between authors.
6. **Adoption weight has no measurement rule.** I used published polls where I found them and wrote "not measured" otherwise. Suggest requiring a source or "not measured" for every adoption figure.
7. **Section 4 covers computed tests. Documentary digs have no equivalent checklist.** Suggest one: quantities ledger, verification level per figure, independence check, list of what could not be accessed.
8. **Page titles do not state findings.** `<title>Eikon Basilike Bounty</title>` helps nobody searching for the answer.

## Critique of my own work (so you can hold me to it)
- Slug IDs instead of C-/F-/G-/DT-.
- No sources list labelled by evidence class yet (sources are in header comments).
- No `.html` pages; YAML only.
- My first draft misstated the NSA Hanyok finding on intent (corrected, log L-03 in the Tonkin dig). The finding is still known only from secondary reports.
- Several quantities rest on search summaries (see the verification ledger).

## Reply space (append below)

### Decision from the owner, 2026-10-01 (jolly-hopper session)
1. **Format: YAML is the standard.** `build/subjects/<subject>/{claims,tests,threads,log}.yaml` is the source of truth. Pages, headlines, meta descriptions and JSON-LD are to be generated from it, not hand-written. The existing HTML bounty pages (B-001, B-002) should be migrated to YAML subjects; their data and run files stay as they are. Open items that follow: ID scheme (C-01 vs slugs), `refutation_class` definitions, and a validator, which does not exist yet.
2. **Verification:** the owner is unblocking primary-source hosts so every `anchor_checked: no` can be re-anchored to the document itself. The verification ledger in `docs/verification/` lists the V2 targets.

### From jolly-hopper, 2026-10-01 (second post): YAML approach
- Draft schema: `build/SCHEMA.md` (v0.1). It lists the fields, the enumerations from CONTRIBUTING.md, and 14 mechanical rules a validator should enforce. Rules marked PROPOSED are new; the rest come from the framework as written. Please review and amend.
- **Validator:** `README-deploy.md` says `build/conformance.py` and a 21-test suite exist, and that deploys are blocked on them. Neither is in this repository, and `deploy.yml` has no validation step. If they live on the owner's machine they should be committed; if not, SCHEMA.md rules 1-14 are a starting spec. I will not write a competing validator without agreement.
- **IDs:** proposal is numeric `id` (C-01...) plus a human `slug`. Existing slugs in my digs would become `slug`. Not migrated yet; awaiting your answer.
- **Status of my digs:** Apollo is **parked** (owner request) until primary sources are reachable. Tonkin is unchanged and also awaits primary-source verification. A new dig, `dyatlov-pass`, is in scoping: feasibility log only, no claims.
- **Migration offer:** once the schema is agreed I can convert B-001 and B-002 into YAML subjects. Their run files stay in `bounties/*/data*`.

### From jolly-hopper, 2026-10-02: proposed framework rule on Wikipedia, and new digs
- **Proposed rule:** Wikipedia may be linked for orientation but is never an anchor. A claim's `anchor` and any `sources` entry may not be a Wikipedia page; the page is a pointer to primary or scholarly sources, which must be read. (Owner decision, 2026-10-02.)
- **New scoping digs** (log only, no claims): `dyatlov-pass`, `mcafee-and-surfside`, `chemtrails`, `flood-myths-worldwide`. Apollo is parked.

### From jolly-hopper, 2026-10-02 (third post): the live corpus has been supplied
The owner uploaded the earlier Mesopotamian dig; it is imported verbatim at `build/imports/mesopotamia-corpus/` with an `IMPORT_NOTE.md`. `validate_threads.py` passes (26 claims, 1 expected warning).
- **The live YAML schema differs from `build/SCHEMA.md` v0.1** (reconciliation table appended there). Where they differ, the live corpus wins; v0.1 was drafted before it was seen.
- **IDs are settled in practice:** slugs with a subject prefix, referenced as `subject:claim`. `C-01` appears only on the HTML bounty pages.
- **Needed from the owner:** the main eight-rule validator, the live schema document, the Gilgamesh subject file and the retranslation.
- **Found in the import:** one Wikipedia anchor (`atra-hasis:ah-date-colophon`) that breaks the new no-Wikipedia rule. Left unedited; to be corrected by a new entry.
- **Evidence-class spelling:** `primary-text` (live corpus) vs `primary_text` (CONTRIBUTING.md). Needs one answer.
