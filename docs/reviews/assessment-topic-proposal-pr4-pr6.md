# Independent assessment: topic admission proposal, PR #6, PR #4

Assessor: independent (did not write any of the three). Date: 2026-10-02. Standard: docs/SCHEMA_PROPOSALS.md (seven standards).
Basis: origin/main at 035a82d (main moved from 7d3093b during the assessment; all results below were re-run on 035a82d), PR #6 head ff5b849, PR #4 head 197af6f, dig/vaccines-autism head d43c49a (PR #7). Scratch worktrees only; nothing pushed, merged or commented.
Baseline: `python3 build/conformance.py --base origin/main` on main = 0 errors, 93 warnings.

## Summary

| Item | Verdict |
|---|---|
| (1) docs/proposals/topic-admission.md | **Meets with specific changes** (standards 1, 2, 3, 5 are not yet met as written; 4, 6, 7 are largely met) |
| (2) PR #6, publication status PS1-PS4 | **Meets with specific changes** (technically sound and verified; procedural and scope gaps, below) |
| (3) PR #4, review gate | **Does not meet as submitted** (not a proposal; conflicts with main; narrows the owner-only list in a way that contradicts GOVERNANCE.md and SCHEMA_PROPOSALS.md). Its validator substance is good and could be re-proposed. |

Common procedural point: #4 and #6 change SCHEMA.md and conformance.py but neither carries a proposal file under docs/proposals/ nor the seven points. Both were authored before the proposals rule landed (#4 commits 13:20-13:28 EDT, #6 7e46310 at 14:08 EDT; the rule 0bc9ff9 is 18:40Z = 14:40 EDT), but neither is merged, so the rule now governs them. The topic proposal itself reached main as part of the squash of PR #2 and not on its own `process/<topic>` PR (docs/SCHEMA_PROPOSALS.md, Process step 1); minor.

---

## (1) Topic admission test (TA1-TA8)

### Standard-by-standard
1. **Failure case: not met.** The standard needs "a concrete case, with files and claim ids". The three examples ("Is the president an idiot?", "Prove the election was stolen", a private person) are hypothetical; no real submission, issue number or file is cited. The repository has one open issue (#5, unrelated) and no submitted topic. No wrong or unusable result is demonstrated. Required: cite a real submission or state honestly that this is pre-emptive and ask the owner to accept it as such.
2. **Evidence: partly wrong.** Section 2 says the News Review form and docs "apply no test". That is inaccurate. `docs/NEWS_REVIEW.md` ("What gets reviewed") already requires a suggestion to "name the specific claims to check and give at least one source" and says "'prove it was staged' is not a claim"; `.github/ISSUE_TEMPLATE/news-review.yml` makes claims and sources required fields and says "We do not name suspects or speculate about anyone's beliefs or background"; `docs/GOVERNANCE.md` already says the owner opens topics and counts carry no weight. There is no "suggest a topic" issue form, only news-review.yml, dig-step.yml and challenge.yml (the Ideas page is generated from build/ideas.yaml and has no form). So the real gap is narrower: no written test for digs and ideas, and no recorded reasons. Required: restate the evidence accurately and show what the existing News Review rule already catches.
3. **Exact change: not met.** No SCHEMA.md or docs text, no file named for the rules (a `docs/TOPICS.md`?), no form field list, no format for the declined-topics page or its record, and no statement that no validator check exists. Section 5 says no validator change; then the enforcement is purely procedural and should say so. Required: exact text and location, exact form fields, exact record format for declines (reason by TA number, rewrite, date, no identity), and who writes it.
4. **What it does not change: met** (claims, schema, validator, publish gate, challenge test untouched).
5. **Impact: not met as written.** Section 6 says existing digs were checked "below", but the table covers only three. I ran TA1-TA8 against all 15 subjects (results below). None would be rejected, but two readings need clarifying (TA4 and TA8), and the rules collide in wording with the taxonomy's own question type "What does it say or mean?" (TA1/TA5). Required: the full table.
6. **Alternatives: met** (do nothing, free-form moderation, voting). Missing: extend the existing News Review test and S1-S5 to digs instead of a new eight-point test.
7. **Neutrality: partly met.** The table pairs mirror-image submissions, but all pairs are symmetric by construction, so they cannot expose asymmetry. See below.

### ID collisions
TA1-TA8 do not collide with any rule id in the repository (text grep of origin/main for `TA[0-9]`, `TH[0-9]`, `PS[0-9]` finds nothing; existing families: T1-T7 timelines, T1-T4 threads, P1-P11, N1-N26, X1-X4, A1-A10, S1-S5, C1-C9, R). The proposal text still says "T-tests; to be named ... e.g. TA1 to TA8": the final name must be fixed in the text. Note TA is one letter away from T-rules; acceptable.

### Existing digs against TA1-TA8 (subject question; result)
- gulf-of-tonkin "Did a second attack ... happen?": pass.
- casket-letters "Did Mary write the Casket Letters?": pass (public record).
- eikon-basilike "Who wrote the King's Book?": pass.
- incandescent-lamp "Who invented the light bulb?": pass; TA1 holds only because "invented" is defined in the dig (partly answerable).
- flydubai-fz1073 "Was the ... attack ... manufactured?": passes TA3 only because the dig is worded as a claim to test; a strict reading of TA8 ("promote a conspiracy narrative") and TA3 ("loaded term") could reject it. It conflicts with TA4 as written (see "TA4" below) in that it concerns named crew and a co-pilot.
- mcafee-and-surfside "tied to John McAfee's death?": pass TA1; strict TA8 could reject it (conspiracy link as premise); TA4 applies to a deceased public figure.
- chemtrails, apollo-landings: popular conspiracy claims; pass only if TA8 means "as a premise, not as a hypothesis under test".
- proto-indo-european, teti-pyramid-texts, flood-myths-worldwide: "origin" and "what does it mean" questions; TA1 ("something evidence could settle") and TA5 ("unfalsifiable questions are declined") would exclude interpretive and unsettleable questions that the taxonomy deliberately includes (types `origin`, `what_does_it_mean`). Casket Letters and Eikon Basilike are `unsettled` by the project's own assessment.
- votes-2009-present, votes-johnson-tonkin, congress-promise-vote: pass.
- vaccines-autism (PR #7): pass.

### Test of rules against 12 submissions from different directions
Result column is my application of the text literally, then the issue.

| # | Submission (direction) | Literal result | Issue |
|---|---|---|---|
| 1 | "Did the Biden administration pressure platforms to remove content?" (right-coded) | Admit (TA1, public record) | none |
| 2 | "Did the 2016 Trump campaign coordinate with Russia?" (left-coded) | Admit; "coordinate" is neutral | mirror of 1; fine |
| 3 | "Prove the 2020 election was stolen" / "Prove it was not stolen" | Both decline (TA3, TA6), rewrite | rewrite is an editorial act: the proposal's own rewrite ("Did court cases A to C find fraud?") narrows to court findings, which can decide the outcome (many cases ended on standing). Rewrites are unspecified for the mirror |
| 4 | "Did Dominion machines change vote totals?" (right-coded) | Admit under TA1; TA8 ("conspiracy narrative") could be invoked | TA8 undefined: a reviewer can decline right-coded conspiracy questions and admit left-coded ones ("2000 election decided by the Supreme Court", "Russian collusion") |
| 5 | "Is Israel committing genocide in Gaza?" / "Did Hamas commit atrocities on 7 October?" | Both decline (TA2 moral/legal conclusion, TA8 group guilt) | "genocide", "fraud", "treason", "murder", "stolen" are legal and moral at once. TA2 lists "corrupt" but not legal terms. Outcome depends on reviewer's classification, not on text. Loophole in both directions |
| 6 | "Did Hunter Biden's laptop contents get authenticated?" (right-coded) vs "Did Trump's inaugural-day crowd match the figure he stated?" (left-coded) | Admit both, but TA4 "private individual" applies to the first | no definition of public figure vs private person; relatives, donors, officials' staff are unaddressed; risk of uneven application |
| 7 | "Is Biden senile?" / "Is Trump suffering dementia?" | Both decline (TA2, TA4 health) | symmetric, but TA4 bars health "of anyone"; officials' published medical reports and 25th-amendment records are public record. Over-broad |
| 8 | "Was the Butler rally shooter acting alone?" (live event, named perpetrator) | TA4 declines (private individual) | contradicts NEWS_REVIEW guardrail 1, which allows naming a suspect named by authorities and multiple outlets. Two rule sets disagree |
| 9 | "Was the COVID lab-leak hypothesis true?" | TA8 would have excluded it as a conspiracy narrative in 2020; TA5 may decline as unsettleable | time-dependent: TA8 uses the then-current consensus as the test. Loophole |
| 10 | "Should the US ban TikTok?" / "Should the minimum wage rise?" | Decline (TA7) | symmetric. But "Does the minimum wage raise unemployment?" and "Does gun ownership reduce homicide?" are empirical and pass; policy questions can be rephrased to pass TA7. Not an asymmetry, a loophole |
| 11 | "Do vaccines cause autism?" / "Did the 1619 Project's claim about the Revolution hold up?" | Admit | fine; TA4's "religion" ban must be limited to persons or "Was America founded as a Christian nation?" is wrongly caught |
| 12 | "Why does the media hide that crime is rising?" / "Why does the right ignore climate science?" | Decline (TA3), rewrite to checkable form | symmetric |
| 13 | "Is [neighbour] an illegal immigrant?" | Decline (TA4) | fine |
| 14 | "Prove my product is the best" | Decline (TA6) | fine |

### Asymmetry and loopholes (summary)
- No asymmetry in the text; the mirrored pairs behave identically. The risk is in four undefined terms that give reviewers discretion: "conspiracy narrative" (TA8), "presume the guilt of a group" (TA8), "private individual" (TA4) and "evaluative" for legal terms (TA2).
- **The unrecorded step:** TA admits "for consideration" only; the owner then chooses which to open with no criteria and no record. Only declines are listed publicly, so selection bias among admitted topics is invisible. Required: record admitted-but-not-opened with a reason and date, and publish counts by area.
- Rewrites change the question. Required: the submitter's original and the rewrite are both kept; the rewrite is a new question the submitter may accept or not.
- TA4 contradicts NEWS_REVIEW guardrail 1 and P6/P11 ("motive is not assessed") only partly; align wording ("does not speculate about motives", which P11 already says).
- TA1/TA5 should read "evidence can bear on" not "could settle", or they exclude the project's own unsettled digs.

### Required changes (topic proposal)
1. Cite a real failure case or state it is pre-emptive. 2. Correct section 2 against NEWS_REVIEW.md, news-review.yml and GOVERNANCE.md. 3. Give exact text, location, form fields and decline-record format; state that no validator check exists. 4. Fix the final id name. 5. Define "private individual" (public figure and person named by authorities), "conspiracy narrative" (as a premise, not a hypothesis under test), and legal terms in TA2 (allowed when tied to a named legal instrument or body). 6. TA1/TA5 "bear on". 7. Resolve TA4 vs guardrail 1. 8. Add the full 15-dig table and a non-mirror neutrality test (cases 4-9). 9. Record admitted-not-opened. 10. Keep rewrites separate from the original.

---

## (2) PR #6: publication status for sources (PS1-PS4)

Trial merge of ff5b849 onto main 035a82d: **clean, no conflicts** (the branch already merges main 7d3093b; GitHub reports mergeable). Result on the merged tree: 0 errors, 93 warnings, warning list identical to main (diffed). An earlier version of the branch (7e46310) read only `anchor.ref`/`anchors[].ref`, which N25 forbids, so PS3 would have been dead; ff5b849 fixed this by also reading `anchor.sources`. I verified that on the merged tree.

### Standards
1. **Failure case: met in substance, not shown in the PR.** The case is the Wakefield paper and Hooker 2014, which vaccines-autism cites. The PR body says "Merge before dig/vaccines-autism" but gives no run showing what goes wrong today. On main today a retracted source could be cited with nothing flagged; I confirmed the validator accepts a manifest `publication:` block as an unknown key with no checks.
2. **Evidence: met.** The PR states a removal test on vaccines-autism. I reproduced it (below).
3. **Exact change: met.** SCHEMA.md text (28 lines) and `check_publication` (60 lines). Weaknesses: the text says "the page shows" the status, but `build/tools/build_site.py` is not changed and renders neither `source_notices` nor `flagged_sources` (grep of main and the branch: no match). The rule is validated but the reader-facing promise is unimplemented. Also `source_notices` is documented as "at the top of claims.yaml", fine.
4. **Does not change: partly.** Not stated in the PR. It does not alter any claim; vaccines-autism is the only dig that uses it.
5. **Impact: met for existing digs; vaccines-autism needs work.**
   - On main's 15 subjects: before 0 errors / 93 warnings; after 0 errors / 93 warnings (identical).
   - vaccines-autism (not on main, PR #7), overlaid on merged main+#6: **39 errors, all N25** (`ref:` inside anchors; the dig predates N25), 0 PS errors. After changing `ref:` to `sources:` mechanically: **0 errors, 106 warnings, 0 PS hits**. So its source flags validate under PS1-PS4: wakefield-1998 and hooker-2014 are `retracted` with date and notice (PS2), both listed in `source_notices` (PS4), and the three claims citing them (va-mmr-causes-autism, va-timing-shows-cause, va-thompson-subgroup-real) carry `flagged_sources` (PS3). `corrected` (3) and `unpublished`/`published` entries are accepted by PS1 and need no date.
   - Removal test: delete the three `flagged_sources` lines: 3 PS3 errors. Delete `source_notices`: 2 PS4 errors. On the branch's own base (13 subjects): 0 errors.
   - Synthetic checks on main digs: marking a cited source retracted in incandescent-lamp gives 7 PS3 errors and PS4; bad status gives PS1; expression of concern without date gives PS2; expression of concern citation gives a PS3 warning. Marking src-hanyok-2001 in gulf-of-tonkin gives PS4 only (no PS3), because that dig cites sources through shared nodes.
6. **Alternatives: not in the PR.** Needed: doing nothing; a Retraction Watch or Crossref lookup tool; a plain `retracted: true` flag.
7. **Neutrality: met in design, shown only on one side.** The rule keys on `publication.status`, never on a claim's direction. vaccines-autism has two retracted sources that both favour the vaccine-harm hypothesis, which is the only dig tested. My synthetic injections show the same behaviour on a patent dig and a Tonkin dig, so the check is direction-blind. The real asymmetry risk is selective checking: `publication` is optional, so the rules enforce only what someone looked up. A dig on a topic that is scrutinised gets flagged; another dig with a retracted paper that supports the opposite or a different view is flagged only if its author checked. Nothing in the validator detects an unflagged retraction.

### Gaps and required changes
1. Add a proposal file with the seven points (alternatives, neutrality on two digs, before/after).
2. Require a check statement rather than optional silence: for any journal-article source, `publication` with `checked: <date>` (a warning at first), so absence of a flag means "checked, clean" and not "not looked at".
3. Scope: PS3 reads only `anchor.sources`. It misses retracted sources reached through shared nodes (`build/nodes/*.yaml` sources have no `publication` field), `tests.yaml`, `timeline.yaml` and `transmission.yaml`. vaccines-autism's timeline.yaml cites the retracted sources twice with no PS check. Either extend, or state the scope.
4. Implement or drop the display promise in `build_site.py`.
5. `corrected` has no required `date`/`notice` and no PS3 warning; vaccines-autism has three `corrected` entries "not read". State that this is intended.
6. The vocabulary cannot express "an earlier version retracted, later version published" (src-mawson-2017 is `published` with the note in `reason`). Acceptable, but say so.
7. vaccines-autism (PR #7) must be brought to N25 before it can merge; that is a PR #7 issue, not #6.

---

## (3) PR #4: review gate

PR #4 head 197af6f (base 1c0593e, before main's publish gate, N25, N26, challenges, taxonomy, nodes). Reviews on the PR: first REQUEST CHANGES, second ESCALATE (no blocking findings; reviewer ran old and new validators on the PR's own tree: identical output). Issue #5 lists non-blocking follow-ups.

### What #4 contains
(a) A validator refactor: thread and transmission-chain checks move out of `check_subject` into a new cross-subject `check_links`, rules renamed TH1-TH4, whole-id matching for the T2/X3 firewall, repository-wide unique thread and chain ids, X2 fails closed without a manifest, `absence_anchor` cap text, robustness. (b) Docs: REVIEW.md owner-only list rewritten ("What only the owner merges"), a "Known limit" section, CLAUDE.md step 5 reworded, README-deploy.md and method/index.html lines updated. (c) A comment-only edit in incandescent-lamp/threads.yaml.

### Trial merge into main 035a82d
`git merge origin/process/review-gate`: **conflicts in three files**: `build/SCHEMA.md`, `build/conformance.py` (two hunks), `docs/REVIEW.md` (two hunks). Auto-merged: CLAUDE.md, README-deploy.md, method/index.html, incandescent-lamp/threads.yaml.

- **Naive resolution (take #4's side of each hunk): breaks the validator.** The run crashes with `NameError: name 'nodes' is not defined`, because #4's side silently drops main's `check_taxonomy`, `check_publish_gate`, `check_definitions`, `check_nodes`, the challenges.yaml checks (S1-S5 intake, N24), and the headline-length warning. That would disable the publish gate and challenge checks. This is the main danger of the conflict.
- **Careful resolution** (I did this by hand): conformance.py hunk 1 keep main's headline and challenge blocks and drop only the old thread/chain code (moved to `check_links`); hunk 2 keep main's four checks and add `check_links`; SCHEMA.md take #4's thread-rules text and keep main's N25 and N26 sections; REVIEW.md keep main's N25 bullet and "How this fits the publish gate (reconciled 2026-10-02)" section and take #4's absence bullet, owner-only list and Known limit. Result: **0 errors, 93 warnings, identical to main's warning list** on all 15 subjects including the newly published incandescent-lamp. #4 and #6 then merge together with no further conflict (0 errors, 93 warnings).
- Injection test on the resolved tree: a reception-overlay member in another subject that is `established` (`gulf-of-tonkin:tonkin-aug2-maddox-engaged`) gives a TH4 error; on main's validator the same edit gives only a warning ("cross-subject check not built yet") and 0 errors. So the validator change is a real improvement and tightens behaviour; no existing dig is affected.

### Rules duplicated or contradicted after merge
1. **Owner-only list narrowed, contradicting main.** #4's list (REVIEW.md, CLAUDE.md, CONTRIBUTING.md, SCHEMA.md, method/index.html, conformance.py, build/tools/, .github/, netlify.toml) omits docs/SCHEMA_PROPOSALS.md, docs/GOVERNANCE.md, docs/PUBLISH_GATE.md, docs/CHALLENGES.md, docs/NEWS_REVIEW.md, build/site.yaml, build/taxonomy.yaml and review.yaml. Main says "Agents never merge" changes to the rules, schema, validator or GOVERNANCE (GOVERNANCE.md table) and that SCHEMA_PROPOSALS.md is changed only by the proposal path; CODEOWNERS covers all of `/docs/`. After #4, REVIEW.md and CLAUDE.md would let an agent merge a change to the standards document itself. #4 also replaces CLAUDE.md's "rules" with the list. This is the main contradiction; it is also the thing SCHEMA_PROPOSALS exists to prevent.
2. **Process change without proposal.** #4 changes rules (REVIEW.md, CLAUDE.md, SCHEMA.md, validator) with no proposal, assessment or owner approval record; it predates the rule but is unmerged.
3. **Residual stale ids after merge.** SCHEMA.md line 59 (Files table) still says "rules T1-T4", X3 still says "same firewall as threads, T2", and docs/COORDINATION.md and other threads.yaml comments still use T-ids (issue #5 notes this).
4. **REVIEW.md "validator covers" list** is from the old base and omits N25, the publish gate, taxonomy and challenge checks; not contradictory but now incomplete.
5. **Known-limit section** (the review is procedural, not enforced) is accurate and is not duplicated on main.
6. Rules duplicated: none exactly; REVIEW.md would carry both #4's gate text and main's "How this fits the publish gate", which restate the same two-control picture and need to be reconciled once.

### Standards
1. Failure case: partly (reviewers found real gaps: cross-subject threads unchecked, X2 failing open); not stated as a proposal. 2. Evidence: yes in the PR reviews (24 injections). 3. Exact change: the diff exists; no proposal text. 4. Does not change: stated in reviews ("weakens no rule"), but the owner-only narrowing does weaken the escalation scope. 5. Impact: shown on its own base only; main has moved (conflicts above). 6. Alternatives: none. 7. Neutrality: a process/validator change, direction-neutral; none shown.

### Required changes
Split #4 in two proposals: (A) the validator/TH rules refactor, rebased on main with the careful resolution above (the substance is sound: 0 new errors, closes real gaps); (B) the REVIEW.md/CLAUDE.md owner-only list, which must be a superset of main's (all of `docs/`, `build/site.yaml`, `build/taxonomy.yaml`, `**/review.yaml` per CODEOWNERS) or explained. Rebase on 035a82d, update the stale T-ids, keep main's publish-gate section, and add proposal files.

---

## Recommendation to the owner
1. Topic proposal: return for the ten changes above; it is not ready for a decision. Its real value is the written test and the public decline record; the main risk is reviewer discretion, which TA2/TA4/TA8 do not constrain.
2. PR #6: the closest to ready. Ask for a proposal file, the check-statement requirement (or an explicit statement that silence means unchecked), and a scope statement (nodes, timeline, tests). It validates the vaccines-autism flags once that dig is moved to N25; merging #6 first is the right order.
3. PR #4: do not merge as is. Rebase and re-submit as two proposals; never accept a conflict resolution that takes #4's side of conformance.py.
4. Order if all proceed: #6, then #4(A), then the owner-list proposal, then the topic test.

Files: /tmp/claude-0/-home-user-strata/01ac625e-87f9-5ed5-babc-df0fe5bd5eeb/scratchpad/assessment-report.md. Validator outputs: conf-main.txt, conf-ps-merged.txt, conf-ps-vx.txt, conf-ps-vx2.txt, conf-rg-naive.txt, conf-rg-careful.txt in the same folder.
