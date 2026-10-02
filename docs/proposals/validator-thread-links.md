# Proposal A: cross-subject thread and chain checks, rules renamed TH1 to TH4

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`, split out of PR #4. Not in force. Needs an independent assessment, then the owner's decision. Companion: `docs/proposals/owner-only-list.md` (independent; either can be decided without the other).
Basis: origin/main at 035a82d merged into this branch. Validator runs: `python3 build/conformance.py --base origin/main`.

## 1. The failure case
Four cases where main's validator gives a wrong or misleading result. Each was reproduced on main and on this branch by editing a scratch copy and restoring it (nothing committed).

1. **Cross-subject thread members are never checked.** Main warns "cross-subject check not built yet" and skips the member. A reception-overlay thread in `apollo-landings` (`thread-apollo-hoax-framing`) given the member `gulf-of-tonkin:tonkin-aug2-maddox-engaged` (state `established`, primary_text) passes on main with a warning. The same member inside `gulf-of-tonkin` is an error on main. Threads exist to connect subjects, so the most useful case is the unchecked one.
2. **The firewall (a claim may not cite a thread or chain as an anchor) only sees its own subject, and matches by substring.** (a) An anchor note in `incandescent-lamp:lamp-davy-arc` saying "see tx-canada-sale-notes.md and thread-edison-legend-draft.md (files, not thread ids)" is a false error on main (two T2/X3 errors); (b) the same claim saying "relies on thread-apollo-hoax-framing" (a thread in another subject) passes on main with 0 errors.
3. **Thread and chain ids may repeat across subjects.** Renaming the `mcafee-and-surfside` thread to `thread-apollo-hoax-framing` gives 0 errors on main. A firewall keyed on ids then cannot tell the two apart.
4. **X2 fails open.** Main's check is `elif manifest and event source not in manifest`: with an empty or missing `sources/MANIFEST.yaml` a transmission event can name any source and pass the X2 rule (emptying the `incandescent-lamp` manifest produces no X2 error on main; this branch reports X2 for every event).
5. **Rule ids collide.** Thread rules are named T1 to T4 in code and messages; the timeline rules in `build/SCHEMA.md` are T1 to T7. "T4" means two different rules. Renamed here to TH1 to TH4.

## 2. Evidence
Runs below. Baselines: main 0 errors, 93 warnings (`conf-main`); this branch 0 errors, 93 warnings; `diff` of the two full outputs is empty.
```
case 1 (cross-subject established member in apollo-landings)
  main: WARNING apollo-landings:thread-apollo-hoax-framing: member `gulf-of-tonkin:tonkin-aug2-maddox-engaged` is in another subject; cross-subject check not built yet  -> 0 errors, 94 warnings
  here: ERROR   apollo-landings:thread-apollo-hoax-framing: reception-overlay member `gulf-of-tonkin:tonkin-aug2-maddox-engaged` is `established` (primary_text); only contested claims, or interpretive claims that are not settled, may be members (TH4). ...  -> 1 errors, 93 warnings
case 1 control (same member inside gulf-of-tonkin): error on both (T4 on main, TH4 here)
case 2a (file names in an anchor note)
  main: ERROR incandescent-lamp:lamp-davy-arc: cites `thread-edison-legend` ... (T2/X3); ERROR ... cites `tx-canada-sale` ... (T2/X3)  -> 2 errors
  here: 0 errors
case 2b (cites another subject's thread)
  main: 0 errors
  here: ERROR incandescent-lamp:lamp-davy-arc: cites `thread-apollo-hoax-framing` (thread in apollo-landings) in its anchors; ... (TH2/X3)
case 3 (duplicate thread id across subjects)
  main: 0 errors
  here: ERROR mcafee-and-surfside:thread-apollo-hoax-framing: id `thread-apollo-hoax-framing` is already used by thread in apollo-landings
case 4 (empty incandescent-lamp manifest)
  main: no X2 error (132 errors, all from other rules)
  here: ERROR incandescent-lamp:tx-lodygin-priority: event `tx-l-04` source `src-kommersant-campaign` is not in sources/MANIFEST.yaml (X2) ... (one per event)
```
Cases 1 to 4 are validator bugs in the sense of `docs/SCHEMA_PROPOSALS.md` (a wrong or unusable result: a false error, and passes that the rule text says must fail).

## 3. The change, exactly
**SCHEMA.md** (`build/SCHEMA.md`, thread rules section; the Files-table row for threads and the X3 line cite TH rules): the text now reads
- **TH1** members resolve to a claim in some subject; write them as `subject:claim-id` (bare ids warn).
- **TH2** no claim, in any subject, cites a thread or transmission-chain id in its anchors; whole-id match; prose in `basis` may point a reader to a thread.
- **TH3** (morphology threads) members carry an attestation; not yet enforced.
- **TH4** reception-overlay members are `contested` claims, or `interpretive` claims whose state is not established or refuted. Settled myths go in `transmission.yaml`, pointed to with `see_transmission`.
- Thread and chain ids are unique across the whole repository.
- X2 needs a non-empty `sources/MANIFEST.yaml` for any subject with `transmission.yaml`; X4 `about` is written `subject:claim-id` and names a claim in its own subject.

**conformance.py**: the thread and chain code leaves `check_subject` and becomes `check_links(r, subjects, index)`, called once from `main()` after every subject has been checked and before main's `check_taxonomy`, `check_publish_gate`, `check_definitions`, `check_nodes` (all kept). It also tolerates a malformed `threads.yaml` (non-list, non-mapping entries) with an error instead of a crash. Main's headline and challenge checks stay in `check_subject` unchanged. Ids renamed in messages and in the comments of `threads.yaml` (apollo-landings, gulf-of-tonkin, mcafee-and-surfside, proto-indo-european, incandescent-lamp) and `transmission.yaml` (incandescent-lamp); `docs/COORDINATION.md` gains one line saying the import script's T1-T4 are TH1-TH4 (its T1 to T7 are timeline rules and are correct).

**Behaviour that is stricter than main** (each is a case above): TH1 and TH4 apply across subjects (main warned); TH2 across all subjects by whole id (main: own subject, substring); repository-wide unique ids; X2 fails closed; X4 requires a subject-qualified `about`; TH4 narrows "any interpretive claim" to interpretive claims that are not established or refuted. Of the 6 claims that are both `established` and `interpretive`, none is a thread member today.

## 4. What it does not change
No claim, state, confidence, anchor or log entry in any subject. No site output (`python3 build/tools/build_site.py` builds: 6 excavations, 16 correction notes). Main's N25, N26, publish gate, taxonomy, challenge and node checks are untouched and still run. The review gate (REVIEW.md) and owner-only list are not part of this proposal.
Note on resolving the merge with main: PR #4's side of the `conformance.py` conflict must not be taken as is; it drops `check_taxonomy`, `check_publish_gate`, `check_definitions`, `check_nodes`, the challenge checks and the headline warning, and crashes with `NameError: name 'nodes' is not defined`. This branch keeps all of them.

## 5. Impact on all 15 digs (errors / warnings)
Same warning list: `diff` of the full validator output, main versus this branch, is empty.
| Dig | Main | This branch |
|---|---|---|
| apollo-landings | 0 / 5 | 0 / 5 |
| casket-letters | 0 / 4 | 0 / 4 |
| chemtrails | 0 / 0 | 0 / 0 |
| congress-promise-vote | 0 / 0 | 0 / 0 |
| dyatlov-pass | 0 / 0 | 0 / 0 |
| eikon-basilike | 0 / 2 | 0 / 2 |
| flood-myths-worldwide | 0 / 0 | 0 / 0 |
| flydubai-fz1073 | 0 / 8 | 0 / 8 |
| gulf-of-tonkin | 0 / 2 | 0 / 2 |
| incandescent-lamp | 0 / 3 | 0 / 3 |
| mcafee-and-surfside | 0 / 3 | 0 / 3 |
| proto-indo-european | 0 / 42 | 0 / 42 |
| teti-pyramid-texts | 0 / 23 | 0 / 23 |
| votes-2009-present | 0 / 0 | 0 / 0 |
| votes-johnson-tonkin | 0 / 0 | 0 / 0 |
| shared nodes (1 warning, not a dig) | 0 / 1 | 0 / 1 |
Total: main 0 errors, 93 warnings; this branch 0 errors, 93 warnings. The previous "cross-subject check not built yet" warning does not occur in any dig (no existing thread has a cross-subject member), so no warning disappears. Threads in existing digs: 8 in 7 subjects; 4 members in total (all in `incandescent-lamp`, same subject, all contested or interpretive and not settled). Migration for each dig: none, except the comment text renames above (comment lines only; log files untouched, so the append-only rule is not engaged; the `incandescent-lamp` log still says T4 and T1 in a past entry and is left as written).

## 6. Alternatives considered
- **Do nothing:** cases 1 to 4 stay; a cross-subject thread could carry an established claim without any error.
- **Warn instead of error for cross-subject TH4:** keeps main's behaviour but leaves an inconsistent rule (same member errors in one subject, warns in another). Rejected.
- **Keep T1 to T4 and renumber the timeline rules:** renumbering published rule ids touches more files and past logs. Rejected.
- **Only fix X2 and the substring match (smallest bug fix):** fixes cases 2a and 4 and leaves 1, 2b, 3. Available as a fallback if the owner finds the cross-subject strictness too much.

## 7. Neutrality check
The rules key on claim state and evidence class and on id strings, never on a claim's direction or subject. Tested on two digs that point in different directions: `gulf-of-tonkin` (a government-conduct question) and `incandescent-lamp` (priority disputes). Case 1 injects a Tonkin established claim into the `apollo-landings` overlay, which fails; the same injection of an `incandescent-lamp` established claim would fail identically because the check reads only `state` and `evidence_class`. No existing dig changes result (table above).

## 8. Independent assessment and decision
Independent assessment of the unmerged PR #4 content: docs/reviews/assessment-topic-proposal-pr4-pr6.md (on the assessor's branch), section 3. Assessment of this proposal: pending. Owner decision: pending.
