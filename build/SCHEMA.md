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
