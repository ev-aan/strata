# Proposal: publication status for sources (rules PS1 to PS4)

Status: PROPOSAL under `docs/SCHEMA_PROPOSALS.md`, on branch `schema/publication-status` (PR #6). Not in force until the owner decides after an independent assessment. This revision answers the independent assessment in `docs/reviews/assessment-topic-proposal-pr4-pr6.md`, section (2). Agents do not merge it.

All commands were run in a clean checkout of this branch merged with `origin/main` (035a82d), on 2026-10-02. "The dig" below means `dig/vaccines-autism` at commit 035bb40, read only; nothing on that branch was changed.

## 1. The failure case

A retracted paper can be cited as an ordinary source and nothing in the repository notices.

The real case is `build/subjects/vaccines-autism` on `dig/vaccines-autism`. Its manifest records two retracted sources (`sources/MANIFEST.yaml`):
- `src-wakefield-1998`, the 1998 Lancet paper, retracted 2010-02-02 (notice recorded as Lancet 2010;375:445). Cited in `claims.yaml` by `va-mmr-causes-autism` and `va-timing-shows-cause`, and in `timeline.yaml` by event `a01`.
- `src-hooker-2014`, Transl Neurodegener 2014;3:16, retracted 2014-10-03 (notice recorded as 2014;3:22). Cited by `va-thompson-subgroup-real`.

On `main` there is no field, rule or rendering for publication status. The dig records the status in `publication:`, `source_notices` and `flagged_sources`, but to the validator on `main` these are unknown keys. Result of running `main`'s `conformance.py` over the tree with the dig added:

```
A. dig as filed (it has publication blocks, source_notices, 3 flagged_sources lines)
   16 subjects and 107 shared nodes checked: 0 errors, 104 warnings
B. same, with every `flagged_sources` line and the whole `source_notices` block deleted
   16 subjects and 107 shared nodes checked: 0 errors, 104 warnings
```
A and B are the same result. The validator on `main` cannot tell a dig that tells its readers about the retraction from one that does not. The page generator (`build/tools/build_site.py`) on `main` prints each source's `authenticity` status and nothing about publication, so a retracted paper in the Sources list reads like any other authenticated source ("authenticity: authenticated"). Wakefield 1998 carries `authenticity: authenticated` in the manifest because the record of the paper was authenticated, not because the paper is sound: authenticity and soundness are different axes (docs/AUTHENTICITY.md), and today only the first is shown.

Limit of this evidence: the retractions are as recorded in the dig's manifest (the dig agent's work; Wakefield read at abstract level, per its `read:` field). I did not open the two retraction notices for this proposal. The proposal does not depend on them: the synthetic injections in section 7 use no real retraction.

## 2. Evidence

Commands and outputs are in sections 1, 5 and 7. Summary of what was checked:
- `main` validator on the dig, with and without its flags: 0 errors both ways (section 1).
- Where a manifest source id can appear in a subject folder, over all 15 digs on `main`: scripted walk of every `*.yaml` in each subject folder for strings equal to a manifest id. Ids occur in `claims.yaml` (`anchor.sources`, `reception_records`), `transmission.yaml` (`chains.events.source`), `actors.yaml` (`statements`, `actions`, `commitments` `.source`) and `timeline.yaml` (event `sources`; the dig only). Shared nodes reach manifest ids by a different route (corrected after the second assessment, which found my earlier statement wrong): a node's `sources` are inline entries, but 48 of the 107 nodes (41 for `incandescent-lamp`, 7 for `gulf-of-tonkin`) carry `manifest: {subject, source}` (SCHEMA, Nodes), and claims reach those nodes through `anchor.nodes` (58 references in `incandescent-lamp`, 9 in `gulf-of-tonkin`).
- The previous version of PS3 (this branch before this revision) read only `anchor.sources`. Injection of a retracted status into each source in turn showed it missed 30 of 121 citation sites in `incandescent-lamp` and 14 of 25 in `gulf-of-tonkin` (section 7).

## 3. The proposed change, exactly

Text: `build/SCHEMA.md`, section "Publication status" (the whole section is the rule text; it is not repeated here except for the points the assessment raised). Validator: `check_publication` in `build/conformance.py`. Page: `build/tools/pubstatus.py` used by `build/tools/build_site.py`. Tests: `build/tools/test_publication_status.py`.

The rules:
- **PS1** `publication.status` is one of `published | unpublished | corrected | expression_of_concern | withdrawn | retracted`.
- **PS2** `expression_of_concern`, `withdrawn` and `retracted` need `date` and `notice`.
- **PS3** A retracted or withdrawn source may be cited only by an item that lists it in `flagged_sources` (error); for an expression of concern, a warning. A `flagged_sources` id must resolve to a manifest source with a valid `publication` status (error).
- **PS4** Every retracted or withdrawn source has an entry in `source_notices` (error). Every `source_notices` entry names a source with a recorded status and carries a `notice` sentence (error).

Answers to the five required changes in the assessment follow.

### 3.1 Silence versus clean (assessment required change 2)
`publication` is optional, so a dig is flagged only if its author looked a source up. Two options:
- (a) Require `checked: <date>` for every journal-article source, with a validator check, so absence means "checked, clean".
- (b) State that silence means unchecked, and make the page say so.

Chosen: **(b)**, the smaller change. Reasons:
1. (a) needs the validator to know which sources are journal articles. The manifest has no such field (`document_class` is `primary_text | secondary | synthetic ...`; Wakefield is `primary_text`, Hooker is `synthetic`). Adding one means a new required field in every manifest, and a judgment per source of what counts. A heuristic on the title or URL would be a guess that the validator cannot defend.
2. (a) as a warning would add a warning to every existing manifest that lists a paper; the owner required the warning list to stay as `main`'s. As an error it would fail digs that pass today.
3. (a) still would not detect an unflagged retraction: a `checked` date proves a lookup was claimed, not that it was done. It trades "silent" for "asserted". The real remedy for selective checking is a tool that does the lookup (alternatives, section 6), which is a separate proposal.

What (b) changes: `build/SCHEMA.md` now says, under "What silence means", that a source with no `publication` block has not been looked up and that this is not "not retracted"; `checked: <date>` is an optional field on the block that says when. The page shows, under its Sources heading, for any dig that records at least one status: "Publication status is recorded only for sources someone looked up. A source with no status shown has not been checked for a retraction or correction; that is not the same as clean." Digs that record none show nothing about publication status at all (they do not imply a check, and their pages are unchanged, section 5). A dig with no manifest cannot record any status (7 of the 15 digs, section 5); the SCHEMA text says so.

### 3.2 Scope of PS3 (assessment required change 3)
PS3 is extended (the node route and the claim-only acknowledgement were added after the second assessment) and its scope is stated exactly in `build/SCHEMA.md` ("Scope of PS3, exactly"). It now looks for a manifest source id as a string in every `*.yaml` file directly in the subject folder (`claims.yaml`, `timeline.yaml`, `tests.yaml`, `transmission.yaml`, `actors.yaml`, `threads.yaml`, `challenges.yaml`), not just `anchor.sources`. Excluded: `log.yaml` and `review.yaml` (they record work and review, and the log is append-only), the manifest, and the `flagged_sources` and `source_notices` keys themselves. The citing item acknowledges with `flagged_sources` on itself or on an enclosing item (claim, timeline event, test, chain, statement); a `flagged_sources` at the top level of a file does not count, so one line cannot silence a whole file.

PS3 also follows a claim's `anchor.nodes` to each node whose `manifest` names this subject and treats that `source` as cited by the claim (acknowledged by the claim's `flagged_sources`). On the 15 digs this changes nothing in the validator output (every such source is also cited directly, and no `publication` block exists); in the injection test it adds the node sites (gulf-of-tonkin 25 to 34, incandescent-lamp 121 to 179 PS3 errors summed over injections). In `claims.yaml` only the claim itself can acknowledge: a `flagged_sources` placed inside the claim, for example in `anchor`, is an error, because the page renders only the claim's own list.

Not covered, stated in SCHEMA.md: a node source that is an inline entry with no `manifest` pointer (no `publication`, so not detected); a node whose `manifest.subject` is another subject; a source named only in prose, a title, a URL or a YAML key; a dig with no manifest or whose claims cite no manifest id, directly or through a node (`mcafee-and-surfside` and `teti-pyramid-texts` have manifests but cite none of their 17 ids from claims, so PS3 cannot apply to them).

Real effect: on the dig as it stood at 035bb40, the extended PS3 found one site the previous PS3 missed, `timeline.yaml` event `a01` (Lancet paper published, 1998-02-28), which cited the retracted paper without a flag (section 5). The dig's author has since flagged it (8efc00d).

Malformed values are errors, not crashes: a non-string `publication.status` is PS1, a `source_notices` entry without a string `source` is PS4, and a non-string manifest id is ignored (tests in `test_publication_status.py`).

### 3.3 Page rendering (assessment required change 4)
SCHEMA.md said the page shows the status; `build_site.py` did not. Now implemented, minimal:
- A claim that lists `flagged_sources` shows, above its statement, a box per source: "Retracted source." (or "Withdrawn source.", "Source with an expression of concern.", "Corrected source.", "Unpublished source.") followed by "This claim cites <source title>", the notice date, the stated reason and the notice (a link if it is a URL).
- `source_notices` render first on the dig page, directly under the title and before the assessment, as a "Source notices" list with a link to each source.
- The Sources list tags each source that has a status ("publication: retracted 2010-02-02") and gives it an id so the links land on it.
- One more sentence under Sources for digs that record any status (3.1).

Tested two ways. (1) `python3 build/tools/test_publication_status.py`: 16 tests, 4 on rendering (notice shown, escaped, absent when no flag, list, tag, note only when a status exists). (2) A scratch copy of the tree with the dig added and a stand-in `review.yaml` (status passed, scratch only, not in the repository) so the build script would publish it: the page showed the 3-item source-notices list before "The short answer", a notice on each of the three claims, and the tagged Sources list. Not done: the timeline page does not show an event's `flagged_sources`; only the claim page and the top list do (stated in SCHEMA.md).

### 3.4 `corrected` (assessment required change 5)
`corrected` is **intentionally** exempt from needing `date` and `notice`, from PS3, and from `source_notices`. Reason: whether a correction changes what a source can support is a judgment about its content (an erratum to an affiliation is not an erratum to Table 2), and the validator can only see the status, not its weight. Forcing a flag on every claim that cites a paper with a correction would put a warning-like notice on sound claims and teach authors to ignore notices. What it does: a `corrected` status is shown in the Sources list when recorded, and an author may list it in `flagged_sources` to show a notice beside a claim; `date` and `notice` are recommended. SCHEMA.md says all of this. The dig has three `corrected` sources, recorded without a date. **Owner decision (section 9):** whether to raise `corrected` to a PS3 warning instead.

`unpublished` is exempt on the same reasoning (a draft is not a retraction); the dig handles its `unpublished` source with a `source_notices` entry, which the schema allows but does not require.

## 4. What it does not change
- It changes no claim, state, confidence, weight, anchor or log entry of any dig. No file in `build/subjects/` is touched.
- The pages of the six published digs are identical apart from one added CSS rule (checked by diff of two full builds, section 5).
- It does not decide whether a retracted source may be cited: citing one (to record the claim it made, or the retraction) is allowed and expected; the rule only requires that the citation shows the status.
- It does not detect a retraction nobody recorded (3.1). It does not look anything up on the network.
- It is blind to what a claim says (section 7).
- It does not edit `docs/REVIEW.md`, `docs/PUBLISH_GATE.md`, `CONTRIBUTING.md`, or the dig branches.

## 5. Impact: every existing dig, before and after

Before = `origin/main`'s `conformance.py`. After = this branch's. The two warning lists are identical (`diff` of the full output: empty); errors 0 and 0.

```
$ python3 build/conformance.py --base origin/main      (this branch, merged with main 035a82d)
15 subjects and 107 shared nodes checked: 0 errors, 93 warnings
$ python3 build/tools/build_site.py
site built: 6 excavation(s), 16 correction note(s)
$ python3 build/tools/test_publication_status.py
Ran 16 tests ... OK
```

| Dig (on main) | Manifest | Manifest ids cited anywhere | `publication` blocks | Before: err / warn | After: err / warn | Migration |
|---|---|---|---|---|---|---|
| apollo-landings | none | n/a | none | 0 / 5 | 0 / 5 | none |
| casket-letters | yes (7) | 6 | none | 0 / 4 | 0 / 4 | none |
| chemtrails | none | n/a | none | 0 / 0 | 0 / 0 | none |
| congress-promise-vote | yes (5) | 5 | none | 0 / 0 | 0 / 0 | none |
| dyatlov-pass | none | n/a | none | 0 / 0 | 0 / 0 | none |
| eikon-basilike | yes (9) | 6 | none | 0 / 2 | 0 / 2 | none |
| flood-myths-worldwide | none | n/a | none | 0 / 0 | 0 / 0 | none |
| flydubai-fz1073 | yes (33) | 26 | none | 0 / 8 | 0 / 8 | none |
| gulf-of-tonkin | yes (11) | 8 | none | 0 / 2 | 0 / 2 | none |
| incandescent-lamp | yes (44) | 43 | none | 0 / 3 | 0 / 3 | none |
| mcafee-and-surfside | yes (10) | 0 | none | 0 / 3 | 0 / 3 | none |
| proto-indo-european | none | n/a | none | 0 / 42 | 0 / 42 | none |
| teti-pyramid-texts | yes (7) | 0 | none | 0 / 23 | 0 / 23 | none |
| votes-2009-present | none | n/a | none | 0 / 0 | 0 / 0 | none |
| votes-johnson-tonkin | none | n/a | none | 0 / 0 | 0 / 0 | none |

(The 93 is these plus one warning on a shared node.) No dig has a `publication` block on `main`, so no rule fires on any of them. Two things this table shows that the previous proposal text did not say: 7 of the 15 digs have no manifest and cannot record a status at all, and 2 more cite none of their manifest ids from claims, so for 9 of 15 the rules cannot apply. That is the real extent of "silence means unchecked" today.

Pages: `build_site.py` was run before and after on the same tree and the two outputs compared file by file. The only difference in any file is the added `.pubnote` CSS rule on the shared stylesheet line; every body is byte-identical (no `publication` block exists in the six published digs, so none of the new markup appears).

Dig not on main, for the record (`dig/vaccines-autism` at 035bb40 overlaid on this tree; read only). The warning figure is 104 here (93 on main plus 11 for the dig), re-run on main 035a82d for this revision; the second assessor reported 105 and I could not reproduce that figure, with the same 104 at the dig's later head 8efc00d. At 8efc00d, where the dig has flagged `a01` itself, this branch gives 0 errors, 104 warnings.

| Validator | Result |
|---|---|
| `main` | 0 errors, 104 warnings |
| this branch before this revision (PS3 on `anchor.sources` only) | 0 errors, 104 warnings |
| this branch now | 1 error, 104 warnings: `vaccines-autism:timeline.yaml:a01: PS3: cites src-wakefield-1998, which is retracted; list it in flagged_sources on that item` |
| this branch now, with `flagged_sources: [src-wakefield-1998]` added to event `a01` | 0 errors, 104 warnings (warning list identical to `main`'s) |
| this branch now, with the dig's three claim-level `flagged_sources` and its `source_notices` removed | 6 errors: 3 PS3 on the claims, 1 PS3 on `a01`, 2 PS4 (against 0 errors on `main`, section 1) |

Migration for that dig, owned by its author and not made here: one flag on event `a01` (since made by the author on its branch). Rendering on that dig (scratch publish, section 3.3): notices list first, a notice on each flagged claim, tagged Sources list.

## 6. Alternatives considered

1. **Do nothing.** Rejected. Section 1: `main` accepts a retracted source cited without any notice and prints it as "authenticity: authenticated". The cost lands on readers, who cannot tell a sound study from a withdrawn one on the page.
2. **A purely manual review step** (a line in `docs/PUBLISH_GATE.md` or the review checklist: "reviewer checks every cited paper for retractions"). Considered seriously: it needs no schema change and catches a retraction in a dig the author never looked up, which no rule here can. Rejected as the only control, kept as a complement: it is applied once at review time and leaves no record on the page or in the file; a later edit that adds a citation is not re-checked; its thoroughness varies by reviewer, and the review gate (`docs/PUBLISH_GATE.md`) is the same mechanism that already relies on one reviewer's attention. The rules here make the result of a check visible and re-checked on every run. They do not replace the reviewer. Nothing in this proposal edits the review documents; the owner may add the line separately.
3. **Require `checked: <date>` on every journal-article source.** Rejected, section 3.1.
4. **An automated lookup (Retraction Watch database or Crossref) run by a tool that writes `publication` blocks.** The best answer to selective checking, and not proposed here: it needs a network dependency, a data licence and a source of truth the owner has not chosen; the validator must stay deterministic and offline. It would work with this schema (it fills `publication`) and is the follow-up I recommend.
5. **A plain `retracted: true` flag.** Rejected: no date, notice or reason; no expression of concern; nothing for a reader to check.
6. **Check only `anchor.sources` (the previous version).** Rejected: it misses sites in other files (section 7).

## 7. Neutrality test

The rules key on `publication.status`, which is a property of a source, never on a claim's state, direction or topic. Checked three ways.

**(a) Unit test.** `test_neutrality_state_and_direction_do_not_matter` runs the same retracted source against claims in each of the five states, once stating a thing and once its opposite: the ten error sets are identical.

**(b) Real digs pointing different directions.** In a copy of each dig, one manifest source at a time was marked retracted (synthetic: date 2000-01-01, notice "synthetic"), with no flag and no notice, and `check_publication` was run. Result per dig, summed over the injections (one per manifest source, so the PS4 column is the number of sources in the manifest, cited or not):

| Dig (its own assessment answer) | Manifest sources cited by id | PS3 errors found (by where) | PS4 errors |
|---|---|---|---|
| gulf-of-tonkin (answer: no) | 8 | 25: 9 on established claims, 2 on searched-gap claims, 14 in `actors.yaml` | 11 |
| incandescent-lamp (partly) | 43 | 121: 32 established, 22 contested, 19 refuted, 14 searched gap, 7 proposed, 27 in `transmission.yaml` | 44 |
| casket-letters (unsettled) | 6 | 12: 6 established, 5 proposed, 1 contested | 7 |
| eikon-basilike (unsettled) | 6 | 9: 3 established, 6 proposed | 9 |
| flydubai-fz1073 (unsettled) | 26 | 135: 54 established, 61 searched gap, 16 proposed, 4 in `transmission.yaml` | 33 |
| congress-promise-vote | 5 | 13: 6 established, 7 in `actors.yaml` | 5 |

Every claim that cites a retracted source is hit, whatever its state (established, contested, refuted, proposed, searched gap), and each cited site gives exactly one error. A source cited only by established claims and one cited only by non-established claims behave the same: for example `casket-letters` `src-nsa-to-catch-a-queen` (cited by one established claim) and `src-labanoff-1844` (cited by one proposed claim) each give 1 PS3 and 1 PS4; `eikon-basilike` `src-tcp-a50898` (established) and `src-tcp-a12229` (proposed) the same; in `gulf-of-tonkin` and `incandescent-lamp` the counts differ only by how many sites cite the source. With the claim-level flag added, the claim errors go to 0 and PS4 to 0 in each case, and what remains is only sites in other files, again independent of direction.

Before this revision the same injection found 91 of the 121 sites in `incandescent-lamp` and 11 of the 25 in `gulf-of-tonkin`; the 30 and 14 missed were in `transmission.yaml`, `reception_records` and `actors.yaml`. The missed sites were not tied to any direction; the extension closes them without regard to it.

**(c) What is not neutral, stated plainly.** The rules enforce what was recorded. A dig on a topic that draws scrutiny gets its sources looked up; another that does not may never be. Nothing in the validator can see an unrecorded retraction. That asymmetry belongs to whoever looks, not to the rules, and it is why 3.1 says silence means unchecked, why the page says so, and why an automated lookup is the recommended follow-up (section 6.4).

## 8. Files changed by this revision (second revision, after the second independent assessment)

`docs/proposals/publication-status.md` (new), `build/SCHEMA.md` (section rewritten), `build/conformance.py` (PS3 and PS4 extended, node route, claim-only acknowledgement, malformed-value guards), `build/tools/pubstatus.py` (new), `build/tools/build_site.py` (renders the above), `build/tools/test_publication_status.py` (new, 19 tests). Also added: `build/SCHEMA.md` now states that a status recorded or changed after publication is a correction under `docs/PUBLISH_GATE.md` with a new log entry (the manifest block is not itself a history), and its "Why" sentence says only what is enforced and shown. `build/SCHEMA.md` and `build/conformance.py` are owner-only changes under `CLAUDE.md`; they are made on this branch only so the owner can judge the proposal, and no agent merges them.

## 9. Independent assessment and decision

Assessment of the revised proposal by an independent reviewer against the seven standards of `docs/SCHEMA_PROPOSALS.md`: pending.

Decisions left to the owner:
1. Adopt (b), "silence means unchecked", or require `checked` dates (section 3.1)? Trade-offs: (b) is the smaller change and adds no warnings, but its page sentence appears only on digs that record a status, and none of the six published digs does, so their pages say nothing about publication status and silence can be read as clean; a site-wide sentence (About page, or a note on every dig's Sources) would fix that but changes published pages. Required `checked` dates need a journal-article field and give an asserted, not verified, lookup.
2. Keep `corrected` exempt, or raise it to a PS3 warning (3.4)? Exempt avoids notices on sound claims and cannot judge materiality; a warning surfaces every corrected source but cannot tell an affiliation erratum from a corrected table. Effect: none on today's digs (no `publication` blocks on `main`); three warnings on the dig.
3. Non-claim citation sites (timeline, tests, actors, transmission): keep them as errors, or make them warnings (3.2)? An error is stronger but forces a flag that readers do not see on those pages (the page shows it only in the top list); a warning weakens the rule for those sites. Showing the flag on the timeline page (5) would make the error meaningful.
4. Add the manual retraction check to the review checklist (section 6.2): cheap, catches unrecorded retractions no rule can, varies by reviewer. And whether to commission a Retraction Watch/Crossref lookup tool that fills `publication`, as a separate proposal (6.4): the best answer to selective checking, but needs a licence and a network dependency.
5. Whether the timeline page should also show an event's `flagged_sources` (not done here; small, but changes the timeline renderer).

Owner decision: pending.
