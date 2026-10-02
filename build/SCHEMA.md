# Strata YAML schema, draft v0.1 (proposal, not yet agreed)

Source of truth: `build/subjects/<subject>/{claims,tests,threads,log}.yaml`. Pages, headlines, meta descriptions and JSON-LD are generated from these files. Everything below is taken from `CONTRIBUTING.md` unless marked **PROPOSED**.

## Files
| File | Holds |
|---|---|
| `claims.yaml` | headline block, `divergence_note`, `claims[]` |
| `tests.yaml` | `discriminating_tests[]` (question, retires, predicts, result, resolves, note) |
| `threads.yaml` | reception overlays; `confers_weight: false` is required |
| `log.yaml` | append-only `log[]`; entries are never edited |

## Claim fields (required unless noted)
`id`, `state`, `statement`, `evidence_class`, `confidence`, `evidential_weight` (1-5), `anchor_checked`, `adoption_weight` (1-5), `adoption_note`, `would_change_if`, `anchor{type,description,accessible}`, `basis`.
Conditional: `refutes_target` (when refuted); `next_step` (when searched_gap); `refutation_class` (only when refuted; classes undefined, see COORDINATION.md).

| Field | Allowed values |
|---|---|
| `state` | established, proposed, contested, refuted, searched_gap |
| `evidence_class` | material, primary_text, interpretive, synthetic |
| `confidence` | high, moderate, low |
| `anchor_checked` | **PROPOSED:** `no` (not checked) / `secondary` (agreed across 2+ secondary sources) / `primary` (document read). Current files use `no` for both of the first two. |

## Mechanical rules a validator should enforce
1. Rule 9: `refuted` needs `refutes_target` and `evidence_class` in {material, primary_text}.
2. Rule 12: `refutation_class` only on `refuted`.
3. `searched_gap` needs `next_step`.
4. Absence anchors are capped at provisional confidence.
5. `proposed` is capped at provisional confidence.
6. Every claim has `would_change_if`, both weights, and `anchor_checked`.
7. Evidential weight and adoption weight are never merged into one field.
8. Threads and lineages have `confers_weight: false`.
9. IDs are unique and never reused (checked against git history).
10. `log.yaml` entries only ever grow (checked against git history).
11. **PROPOSED:** `evidential_weight` is at most 4 unless `anchor_checked: primary`.
12. **PROPOSED:** `established` requires `anchor_checked: primary`, or an explicit `exception:` line explaining why not.
13. **PROPOSED:** a published headline must name (`headline_claim`) a claim that is established or refuted at `evidential_weight` >= 4 with `anchor_checked: primary`. `headline_status` is `draft | published | parked`.
14. **PROPOSED:** a convergence claim needs at least two anchors marked `independence: independent`.

## Open items
- ID scheme: `C-01` numbering (CONTRIBUTING) or slugs (PIE, Apollo, Tonkin). Suggested: numeric `id` plus a human `slug`.
- `refutation_class` definitions and their evidential bars.
- A validator. README-deploy.md refers to `build/conformance.py` and a 21-test suite; neither is in this repository.

---
## Reconciliation, 2026-10-02 (added after seeing the live corpus)

v0.1 above was drafted from CONTRIBUTING.md and the HTML bounty pages **before** the owner's Mesopotamian corpus was available. That corpus is the established YAML standard, so v0.1 should yield to it where they differ. Differences found (see `build/imports/mesopotamia-corpus/`):

| Topic | Live corpus | My Apollo/Tonkin files (v0.1) |
|---|---|---|
| Subject header | `subject:{id,title,incipit,provenance_note,primary_edition}` | flat `subject:`, plus headline block |
| Claim IDs | slugs with a subject prefix (`ah-structure`); cross-references written `subject:claim` | slugs (`apollo-staged-hoax`); bounty HTML pages use `C-01` |
| Evidence class | per anchor: `anchors:[{class, ref}]`, one claim can carry several classes | one `evidence_class` per claim plus one `anchor{}` |
| Class spelling | `primary-text` | `primary_text` (changed to follow CONTRIBUTING.md) |
| Contested claims | `positions:[{label, holder, ground}]` with named holders | one `anchor` of type `live-dispute` |
| Weights | none in the claim files | `confidence`, `evidential_weight`, `adoption_weight`, `anchor_checked` |
| Threads | `type: morphology` or `reception-overlay`; `members:[{claim, attestation}]`; rules T1-T4 | `type: reception-overlay` with `overlay_notes` and `firewall`; no `members` |
| Attestation | per member: preserved, reconstructed, inferred, interpretive | none |

**Consequence:** the ID question is largely answered by the live corpus: slugs with `subject:claim` references. Only the bounty pages use `C-01`.
**Recommended v0.2 (needs the owner's main eight-rule validator and live schema to finish):** adopt the live corpus structure as the base; carry my extra fields (`confidence`, weights, `anchor_checked`, `would_change_if`, `next_step`, `divergence_note`, headline block) as additions only if the main validator accepts them; convert my threads to `members` with `attestation`; fold `positions` into my contested claims.

---
## Timelines (added 2026-10-02)

`build/subjects/<subject>/timeline.yaml` holds events, people and sources for a subject where *who did what, and when* matters (live events, intelligence chains). `build/tools/render_timeline.py <path>` generates `timeline.html` beside it. The YAML is the source of truth.

- `panels[]`: a time window with its own scale and `lanes` (one lane per actor or group).
- `events[]`: `id`, `panel`, `lane`, `time` (UTC ISO), `precision` (exact | approx | range | day), optional `end`, `kind` (data | official | witness | media), `status` (reported | single | disputed | inferred), `sources[]`, `label`, `detail`; optional `alt_time` and `alt_note` to draw a second source's time for the same event.
- `people[]` and `sources[]` list everyone and everything cited. Rules for people: name only officials and people the cited reports name who spoke publicly; never name an unidentified suspect.
- Every `sources` reference must resolve; every event's lane must exist in its panel. A validator should check both.


---
## Sources and authenticity (added 2026-10-02; draft v0.2, pending review)

Method and cases: `docs/AUTHENTICITY.md`. Authenticity is its own axis. It is never merged into `evidential_weight`; it limits what a claim may say about its anchor.

### Where it lives
Each subject lists its sources in `sources/MANIFEST.yaml` (or `sources.yaml`). Every source carries an `authenticity` block:

| Field | Meaning |
|---|---|
| `status` | `authenticated` \| `disputed` \| `forged` \| `unchecked` \| `not_applicable` |
| `strength` | `strong` \| `moderate` \| `weak` (required when status is authenticated, disputed or forged) |
| `provenance` | Where the item has been, in words, with who holds it now |
| `tests` | Named tests run, each one that could have failed |
| `tested_by` | Who ran them, and whether they are independent of the claimant |
| `gaps` | What was not checked |
| `next_step` | The one action that would close the largest gap |
| `checked` | Date |
| `decisive_anachronism` | For `forged`: `{what, first_possible_date, claimed_date}` |
| `copy_of`, `sha256`, `compared_with_holder_copy` | For mirrors and copies |
| `derived_from` | For transcriptions, OCR and translations, which carry their own entry |
| `capture` | For digital items: archive or platform records, with dates |

### Rules a validator should enforce
- **A1** Every source has an `authenticity` block with a valid `status`.
- **A2** `authenticated` needs at least one named test that could have failed, and a `provenance` statement.
- **A3** `forged` needs a `decisive_anachronism`, or at least two tests by different testers.
- **A4** A claim may carry `anchor_checked: primary` only if every anchor it relies on is a source whose status is `authenticated` with strength `moderate` or `strong`. Otherwise the cap is `secondary`.
- **A5** A claim that rests only on an `unchecked` source has `evidential_weight` at most 3 and `anchor_checked` at most `secondary`.
- **A6** A claim cannot be `established` on a `disputed` source alone.
- **A7** A copy or mirror records `copy_of`, `sha256` and `compared_with_holder_copy` (yes | no).
- **A8** A digital item (a post, a screenshot, a file) needs at least one `capture` by a party independent of the person who produced it, or a platform record. A screenshot alone is `unchecked`.
- **A9** Transcriptions, OCR and translations are separate source entries with `derived_from`; authenticity of the original does not cover them.
- **A10** Authenticity is never folded into `evidential_weight` or `confidence`.

## Timelines: when one is required (added 2026-10-02)
- **T1** A subject with five or more dated events, or any live event, carries a `timeline.yaml`.
- **T2** Every event has at least one source with a URL; the diagram's dot opens it (PDFs open at the page where practical). A `link` field overrides the first source.
- **T3** Times are UTC. A source's own clock convention is stated, and an ambiguous clock is drawn as a range with a note.
- **T4** `precision` is stated for every event (exact, approx, range, day, month, year); events without a reported time are drawn hollow or as bars.
- **T5** `timeline.html` is generated by `build/tools/render_timeline.py` and never edited by hand.
- **T6** Every event's `kind` (data, document, official, witness, analysis, media) and `status` (reported, single, disputed, inferred) is stated; the diagram shows both.
- **T7** Where two sources give different times for the same event, one dot is drawn at the better-supported time and a ghost marker at the other (`alt_time`, `alt_note`).
