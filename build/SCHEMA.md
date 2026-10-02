# Stratah YAML schema, draft v0.1 (proposal, not yet agreed)

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

## Actors, statements and votes (draft v0.3, 2026-10-02)

Applies to ANY subject that names decision-makers: Tonkin (Johnson, McNamara, Bundy, Congress),
the politics pilot (`congress-promise-vote`), and later digs. One method, one presentation.

### Actor record (`actors.yaml`, one entry per named person or body)
```yaml
actors:
  - id: mcnamara            # slug, never reused
    name: "Robert S. McNamara"
    role_at_event: "Secretary of Defense"      # role at the time, with dates
    roles: [{title: "...", from: "1961-01-21", to: "1968-02-29", source: <src id>}]
    affiliation: "Democratic administration"   # party/body where relevant, dated and sourced
    # What the record shows, in four fixed buckets. Every item has a date and a source link.
    statements: [{date, text_quote, venue, private|public, source, anchor_checked}]
    commitments: [{date, text_quote, specific: true|false, source}]   # 'specific' per rule P2
    actions: [{date, kind: vote|order|signature|testimony|filing, what, source}]
    alignment: []             # see P4; links a commitment to an action
    motive_map: {possible: [...], acted_on_evidence: [], weight: "none (rule P6)"}
```

### Timeline event kinds added (render in the same shapes as existing kinds)
`vote` (official; square), `statement` (witness; diamond), `commitment` (document; hexagon),
`filing` (official; square, e.g. a donation or disclosure). Every dot still links to its source (T1).

### Rules P1 to P8 (politicians and officials)
- **P1 Same dig for everyone.** Each actor gets the same four buckets (statements, commitments, actions,
  alignment). If a bucket is empty it says "searched, none found" with the places searched (a searched_gap).
- **P2 Commitment is specific.** A dated, attributable statement of what they would do on this matter.
  Values language ("I support a strong defense") is a statement, not a commitment.
- **P3 Anchor the action to the official record.** A vote is anchored to the roll call (House Clerk XML,
  Senate.gov XML, or the Congressional Record). A dataset such as Voteview is a cross-check and is
  marked `anchor_checked: secondary` until the official roll call is read.
- **P4 Alignment labels only:** `kept`, `broke`, `changed_with_stated_reason`, `no_specific_commitment`,
  `not_determinable`. No scores, rankings or grades. Public and private statements are shown separately
  (Tonkin: McNamara's private call and his Senate testimony are different events with different weight).
- **P5 Money is context.** A dated filing beside a vote shows timing only. The page states that timing
  does not show causation unless a source documents the link.
- **P6 Motive carries no evidential weight.** It is listed in `motive_map` and labelled so.
- **P8 Information available at the time.** For every action, record what the actor could have known on that date, from the sources, or `not_determined`. A mismatch between a statement and later facts is not a broken commitment unless the information was available to them then. (Added after the Tonkin test; the vote is the clearest case.)
- **P7 Same neutrality for all parties and sides.** Selection rules are written before records are read
  (see `build/subjects/congress-promise-vote/protocol.yaml`). Subjects are never swapped to find a result.

### Politics-only additions (draft, 2026-10-02): apply ONLY to digs about officials and votes
Scope note: these rules are not part of the general schema. They are used only where the subject is what a
public official did and why it might have happened. Other subjects (documents, events, natural questions) do not use them.
- **P9 Inducement claims (pressure or payment) are their own claims**, filed per actor, default `searched_gap`
  (never "clean"). Evidence tiers:
  - `decisive`: conviction or plea, official ethics or inspector-general finding, a recorded communication, or an
    admission by a participant. One is enough to establish the claim.
  - `supporting`: documented contacts, or a donation followed by a vote with a source linking them. Never enough alone.
  - `context`: timing or money alone. Shown beside the vote, carries no weight toward the claim.
  - Absence of a decisive item is recorded as "not found, searched: <places>", not as evidence of independence.
- **P10 Consistency over time (analysis, class `synthetic`)** is computed the same way for every actor in a dig:
  position stability on the matter across dated events, with a published baseline for how often members change
  or break with their party. It describes behaviour, not belief, and is capped at weight 3.
- **P11 Sincerity and motive are not assessed.** Every actor page carries the fixed line:
  "Motive and sincerity are not assessed." Authorship questions (who wrote a speech or statement) are handled by the
  authenticity rules A1 to A10, not by P-rules.

### Applied so far
- Tonkin: `actors.yaml` built for Johnson, McNamara, Bundy, Morse, Gruening (2026-10-02); vote links to the roll-call data.
- Politics pilot: protocol conforms to P1 to P7.

## Nodes: shared dated artifacts (draft v0.4, 2026-10-02)

A node is one dated artifact (an event, a document, an image, a recording, a dataset) kept once in `build/nodes/<id>.yaml`. Digs refer to nodes; they do not copy them.

**Fields.** `id` (permanent, equals the file name), `rev` (whole number from 1), `type` (event, document, image, recording, dataset), `label`, `time` (ISO; negative years are BCE as written), optional `end`, `precision`, `kind` (the source kind that sets the marker shape: data, document, official, witness, analysis, media), `status` (single, reported, disputed, inferred), `what` (what the sources show, nothing about what it means), `sources` (title, url, authenticity), `link`, `related`, `created`, `history`. Images and recordings add `media: {file, sha256}` and `evidences: [node ids]`. A node whose source is already filed in a dig's sources manifest points to it with `manifest: {subject, source}` instead of repeating the authenticity record.

**Rules.**
- N1. A node says what a source shows, with its date. It does not say the thing is true. That judgement lives in the claims, which cite nodes as anchors.
- N2. Digs reference a node by `node: <id>` (and `rev:` for the revision they read) in `timeline.yaml`. A dig's own reading goes in the event's `note`, never into the node.
- N3. Append-only. A change is a new `rev` plus a `history` entry that says what changed and why. Nothing is overwritten or deleted.
- N4. A dig that disagrees with a node (a different date, a different reading of the source) makes a variant: a new node with `derived_from: <id>` and `variant_reason`. The original stays and both can be shown.
- N5. Two descriptions are merged into one node only when they are the same event. Overlaps that are not identical stay separate and are linked with `related`. Merges are logged in the node's `history`.
- N6. A node needs at least one source or a stated `source_gap`. A media file carries its sha256, and the file is stored only where its licence allows.
- N7. Conformance checks that every `node:` resolves, that hashes match, that history is in step with `rev`, and warns when a dig's pinned `rev` is behind the node's current `rev`.
- N8. A dataset (for example a set of roll calls) is one node that points at its records. Individual records become nodes only when a dig cites them.

Tools: `build/tools/nodes.py` expands references in memory for the timeline renderer and the Atlas. `build/tools/migrate_tonkin_nodes.py` was the one-off pilot move of the Tonkin family.

### Places and objects on nodes (added 2026-10-02)
- N9. Any node may carry `place: {name, lat, lon, precision (exact | site | city | region), uncertainty_km (optional), source, note}`. A place needs a `source` for its coordinates (a gazetteer such as OpenStreetMap Nominatim counts as orientation, not as evidence that the event happened there). Give a place only where a source read names it; otherwise leave it out. Never guess a find-spot: say it is unknown.
- N10. An object (a tablet, a manuscript, a casket) is a node of `type: object` with ordinary descriptive fields (`object: {class, material, museum, accession, held_now: {status, as_of, note}}`). Its life is told by ordinary event nodes (made, found, acquired, moved, held, published), each with its own date and place, and each pointing at the object with `about: [object id]`. There is no separate custody structure. `held_now` always carries an `as_of` date and a source, or says `not established`.
- N11. Published coordinates follow the precision the source gives (owner decision 2026-10-02), and the `precision` field says which it is.
The Atlas has a Map view (Leaflet and OpenStreetMap tiles, loaded only when the Map button is pressed) that shows nodes with coordinates, filtered like the timeline, with a time slider and dashed custody routes between events about the same object.

### Terminology: open questions (2026-10-02)
A narrowed, testable question inside a dig, with a stated test and an append-only record, is an **open question** (formerly "bounty"). Pages live under `/questions/`; `/bounties/` redirects. New items use the prefix `Q-`. The two existing ones keep their legacy IDs B-001 and B-002 in YAML (`bounty_id`) and in logs, and are shown as Q-001 and Q-002 on the site. Claim-level IDs (C-, F-) are unchanged.

### Grouping the excavations (2026-10-02)
`build/taxonomy.yaml` holds the areas (History, Politics and Government, Current Events, Science and Nature, Medicine and Health, Technology and Engineering, Archaeology and Ancient Texts, Language and Linguistics, Religion and Mythology, Law and Justice, Media and Misinformation, Economics and Business), the question types (Did it happen? Who wrote or made it? Is it genuine? What caused it? What did people know, and when? Is a widely shared claim true? Where and when did it begin? What does it say or mean?) and each subject's assignment: one primary `area`, optional extra `areas`, `types`, and `popular_claims`. Conformance checks every value and warns when a subject has no entry. The site builds the filters on /digs/ and a page per area under /areas/. Areas with no excavation get no page.

### Many kinds of source, graded links and dates (schema v0.5, 2026-10-02)
Learned from a review of another node-based archive (docs/research/archivegenocide-node-map.md). The system must take in many kinds of source, so each source on a node says what it is and where it comes from.
- N12. **Source fields.** Each source on a node has `origin` (a short id for the underlying record or work), optional `derives_from` (the origin it repeats or draws on), `source_type`, and `access` (`read` = opened and read here, `cited_only` = known only from another source). Source types: primary_document, official_record, official_history, dataset, scholarly, secondary_report, news, social_media, testimony, ai_generated, unknown. An `ai_generated` source can never be a node's only source and never an anchor.
- N13. **Independence.** Sources that trace to the same origin count once. `build/tools/nodes.py` computes, for each node, the number of independent origins, how many were read, and a label: `single_origin`, `independent` (2+ declared), `multiple_unverified` (some origins not declared) or `no_source`. Repeats, reposts, datasets built from an official record, and summaries of a primary document are not corroboration; they are adoption. Conformance warns when a node's `status` disagrees with the count.
- N14. **Date basis.** Every node says how its date was arrived at: `stated` (given in the source), `derived` (worked out, for example a time-zone conversion or "after X"), `publication_proxy` (the date a source was published, used because no event date is given), `inferred` (our inference) or `dataset_field` (a date column of a dataset). Precision (day, month, year) is separate from basis.
- N15. **Graded links.** `related` links are mappings: `{node, kind (same_event | part_of | summarises | overlaps | responds_to), grade (established | possible), why}`. `established` follows from a stated signal (the same record, an explicit reference, the same event); `possible` is a lead and is never treated as a finding. Nodes are merged only on an `established` same_event link, and only by a person approving it.
- N16. **Migration.** All 62 existing nodes were given these fields by rule in one pass (build/tools/migrate_nodes_v05.py); each has a new `rev` and a history line saying the values were assigned by rule and are to be reviewed. Two nodes had their `status` corrected because their two sources repeat one record.
Still to do from the review: gazetteer ids for places, a build id with signed checksums and exports, a public list of rejected findings, and Atlas query and share links.

### Schema v0.6 (2026-10-02): windows, definitions, kinds of statement, reasons for confidence, disputes
From the standards survey (docs/research/open-data-standards-survey.md).
- N17. **Authority-scoped definitions.** `build/definitions/<id>.yaml` holds one authority's definition of a period, kept as printed: `label`, `authority` (title, creators, year, locator), `quoted` (start and stop text exactly as printed), `from_bce` and `to_bce` (our reading, BCE years counting down), `via` (how we reached it), `authority_read_directly`, and a `note` for any discrepancy. A definition is never edited, only superseded. Two authorities' versions of one period coexist. Years in nodes follow the same convention: a negative year is BCE as written, so -2700 is 2700 BCE. (PeriodO's structured years are astronomical, so -2669 there is 2670 BCE; the definitions record the conversion.) Six definitions of the Egyptian Old Kingdom were taken from the PeriodO dataset.
- N18. **Time window.** A node may carry `window: {earliest, latest (or open), certainly_covers: {from, to}, begin_note, end_note, defined_by}`. `time` stays the best single date and must lie inside the window. `begin_note` and `end_note` are required: the reason for each boundary. With `defined_by`, conformance recomputes the window from the definitions (outer bounds = earliest start to latest end; certainly covers = latest start to earliest end). The Atlas draws the window as a pale bar around the node and the span all authorities agree on as the solid bar.
- N19. **Kind of statement** (from ICD 203). Every claim has `statement_kind`: `reported` (what a source says or shows), `judgment` (a conclusion about what happened or is true), `assumption`, or `search_result` (what a search did and did not find). The values on the existing claims were assigned by rule and are marked to be reviewed. A claim may list `assumptions: [{text, if_wrong}]` and `alternatives: [{text, why_not_preferred}]`. An optional `likelihood` (almost no chance, very unlikely, unlikely, roughly even chance, likely, very likely, almost certain) says how probable the event is; it is a separate thing from `confidence`, which says how sure we are of the basis. The words are conventions and carry no stated percentages. Never put a likelihood and a confidence word in the same sentence.
- N20. **Reasons behind confidence** (from GRADE). A claim may give `confidence_reasons: {start, start_because, steps: [{domain, effect, reason}], reviewed}`. `start` follows the anchor (primary read: high; secondary: moderate; not checked: low). Domains that lower: risk_of_bias, inconsistency, indirectness, imprecision, unreported_negative_results. Domains that raise: independent_corroboration, primary_anchor_read, convergent_material_evidence. Effects: down1, down2, up1, none (a domain considered and not applied still gets its reason). Conformance rejects a confidence higher than its steps give. This is a checklist with written reasons, not a calculator, and a rating below `provisional` is not possible.
- N21. **Attributable disputes** (from Wikidata's "statement disputed by"). A contested claim lists `disputed_by: [{who, kind (person | institution | group | work | unnamed), position, source_read, via}]`. A disputant we cannot name is recorded as `unnamed` and the claim says so. Rank and agreement are never evidence.
- N22. **What an evidence node does** (from CiTO). Each entry of `anchor.nodes` is `{node, verb}` with verb supports, disputes, refutes, qualifies, confirms, corrects or extends, said about the claim's statement. For a refuted claim the evidence disputes the statement.
Applied: the four published excavations (statement kinds on all 128 claims' siblings in those digs; assumptions, alternatives and confidence reasons on their four headline claims; disputants on three contested claims; verbs on the 16 Tonkin anchors); windows on four Casket and one Old Kingdom node. Everything assigned by rule or drafted by the project says so and is marked to be reviewed.

### Where it stands: the assessment (2026-10-02)
- N23. Every excavation page opens with the question and its answer in words, from `assessment:` in claims.yaml (shown on the page under the heading 'Where it stands', labelled 'Current assessment'): `question`, `answer` (yes | no | leans_yes | leans_no | unsettled | partly), `headline`, `text`, `basis` (claim ids), `would_settle`, and an optional `lean: {toward, strength, because, caveats}`. The page also generates the same box on the matching open-question page. **No percentages**: an assessment must not state a probability (conformance rejects `%` and "percent"), because no source supplies a calibrated number and an invented one would be false precision. Confidence words describe how sure we are of the basis. `leans_yes` / `leans_no` need at least one basis claim at moderate or high confidence; below that the answer is `unsettled`, and the direction the data points is shown in `lean` with its caveats and the line that it is not a finding. Casket Letters and the King's Book are `unsettled` with a stated slight lean; Gulf of Tonkin and Surfside are `no`.

N23 addendum: the assessment is laid out as an executive summary. Order on the page: the question as the page title; then 'Where it stands' with the answer in one sentence (`headline`), three `key_points`, the lean if any, the evidential and adoption ratings of the central claim (`rated_claim`, default the first `basis` claim), and `would_settle`; the longer `text`, the lean's caveats and the basis claims fold under 'The full reasoning'. The `<title>` of the page keeps the search headline that states the finding.

### Challenges and submitted evidence (2026-10-02)
- N24. Public challenges and submitted evidence follow docs/CHALLENGES.md (rules C1 to C9): a challenge is evidence that must pass an admission test (S1 specific, S2 evidential, S3 checkable, S4 relevant, S5 not opinion); counts, reactions and repeats carry no weight; admission is decided by a reviewer, never by automation or the submitter. A ledger entry that came from a public submission carries `intake: {issue, decided, criteria: {S1..S5: pass|fail}}`; a ledger `result` may also be `declined` (the entry then states the criterion failed and no name). Conformance rejects an admitted result on a challenge that failed a criterion.

## Transmission records and thread membership (added 2026-10-02, enforced by conformance.py)

`build/subjects/<subject>/transmission.yaml` traces how a claim spread, step by dated step. It is the
standing rule's "transmission chain": a myth is documented as seriously as the history, and its spread
never counts as evidence. First used in `incandescent-lamp`; the format is in that file's header.

- **X1** every chain sets `confers_weight: false`.
- **X2** every event names a source listed in `sources/MANIFEST.yaml` and says `read: yes | no`.
- **X3** no claim may cite a chain id in its anchors (same firewall as threads, T2).
- **X4** `about` resolves to a claim in the subject.

Thread rules now enforced in the validator:
- **T1** members resolve to a claim; write them as `subject:claim-id` (bare ids warn).
- **T2** no claim cites a thread id in its anchors.
- **T4** reception-overlay members are only `contested` or `interpretive` claims. Settled myths go in
  `transmission.yaml`, pointed to with `see_transmission`.
- Claims marked `absence_anchor: true` are capped at provisional confidence.
