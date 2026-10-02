# Refutation classes: define the five, add two, and require the evidence

**Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.**

Author: an agent (Claude Sonnet 5.5), session https://claude.ai/code/session_01CHPX2Whoid8Mecyfqx5j6p. The owner has said on 2026-10-02 that he wants refutation classes made. That is a preference, not a failure case; the justification for this proposal is section 1, which stands without it. This file proposes how, so that the owner's decision rests on a proposal that meets the seven standards. Nothing in it is applied: no claim, `CONTRIBUTING.md`, `build/SCHEMA.md` or `build/conformance.py` is changed. This is revision 2, after an independent assessment (verdict: meets the standards with specific changes); every change it required is made and listed in the revision note at the end. Every number below was produced by running the code named in the text; the patch was applied only in a scratch worktree of `origin/main` (91f6218), which was removed afterwards.

## Summary

- CONTRIBUTING Rule 12 says each class "has its own evidential bar". No bar is written anywhere. `build/conformance.py` checks only that the name is one of five.
- Six refuted claims on `main` already carry a class (five in `incandescent-lamp`, one in `teti-pyramid-texts`); four fail the bars proposed here, the validator passes all six, and a motive class was already imputed once with no evidence (lamp L-05) and caught only by hand. (The vaccines-autism branch sets none.)
- Proposal: a class stays optional, but when set it must carry a separate `refutation_origin` block showing, from documents read, how the false belief arose. Every class has a fixed evidence type and required fields the validator checks. The classes that allege intent (`fabrication`, `motivated_error`, `institutional_propaganda`) need two sources, the holder's own quoted words with source and locator, a stated link to the claim, and a holder who is an institution or public figure; they are capped at moderate. The two-document classes need both documents and the passages. The origin block is checked by the validator and, for quotations, by `review_dig.py` against stored sources.
- Two classes are added, `misreading` and `failed_hypothesis`, because 6 of the 17 refuted claims fit none of the five. `failed_hypothesis` makes no claim about good faith. No class is added for which there is no refuted claim.
- A class names how the belief arose and carries no weight on whether the claim is refuted. A competing origin in the same dig is shown with `see_also`.
- Impact on the 15 digs: 0 errors before; 6 errors after the validator patch alone (5 in `incandescent-lamp`, 1 in `teti-pyramid-texts`); 0 errors after the migration, with the 93 warnings unchanged. Of the 17 refuted claims, 1 can be classed in full today (Canada, `narrative_drift`), 5 in part, 7 have a candidate class that needs one more document read, and 4 have none.
- The migration keeps two classes with origin blocks, removes four with log entries and a prose fix, and does not add a Tonkin class (it is partial).

## 1. The failure case

### 1.1 What Rule 12 promises

CONTRIBUTING.md Rule 12: "`refutation_class` may only be set on a claim whose state is `refuted`. Each class (`narrative_drift`, `misattribution`, `motivated_error`, `institutional_propaganda`, `fabrication`) has its own evidential bar." docs/REVIEW.md (section B) tells the reviewer: "Each `refutation_class` meets its bar: `fabrication` needs evidence of deliberate invention; `institutional_propaganda` needs an anchored institutional campaign; otherwise use a weaker class." build/SCHEMA.md lists "`refutation_class` definitions and their evidential bars" as an open item. docs/COORDINATION.md (item 2) records the agent who wrote two digs declining to set a class "rather than guess". The vaccines-autism log (L-07, on `origin/dig/vaccines-autism`) says the same for five more.

What the repository delivers: a name list in `build/conformance.py` (lines 32-33) and the check at lines 182-187:

```
rc = c.get("refutation_class")
if rc is not None:
    if state != "refuted": r.err(... "only allowed on refuted claims")
    if rc not in REFUTATION_CLASSES: r.err(... f"unknown refutation_class `{rc}`")
```

So the rule promises a bar per class, the reviewer is told to check the bar, and there is nothing to check it against. REVIEW.md's two example bars (deliberate invention; anchored institutional campaign) are the only text, and cover two of five classes.

### 1.2 Every refuted claim today

Found by loading every `build/subjects/*/claims.yaml` and `state: refuted`, and the claims file on `origin/dig/vaccines-autism` (a dig in progress, not on `main`). 17 claims.

| # | Subject : claim | Class set today | Evidence class | What refutes it |
|---|---|---|---|---|
| 1 | apollo-landings : apollo-staged-hoax | none | material | Convergence: reflectors ranged by outside stations, about 150 labs dating the rock, later imaging of the sites. |
| 2 | gulf-of-tonkin : tonkin-aug4-attack-occurred | none | primary_text | Intercept reports 7, 12, 13 as re-read by Hanyok (NSA study). |
| 3 | incandescent-lamp : lamp-lodygin-first-claim | narrative_drift | primary_text | British patents 1841 and 1845 (Patent Office abridgments). |
| 4 | incandescent-lamp : lamp-canada-invented-claim | narrative_drift | primary_text | US 181,613 against US 223,898, both read in full. |
| 5 | incandescent-lamp : lamp-latimer-invented-claim | misattribution | primary_text | US 252,386 and 247,097 against US 223,898 and the 1845 patent. |
| 6 | incandescent-lamp : lamp-10000-ways-quote | narrative_drift | primary_text | Dyer and Martin 1910, vol. II pp. 615-616 (earliest version found). |
| 7 | incandescent-lamp : lamp-edison-sole-inventor | narrative_drift | primary_text | Patents of 1841, 1845, Woodward, Swan's 1878 report, 47 F. 454 and later opinions. |
| 8 | mcafee-and-surfside : surfside-deliberate-timed-to-mcafee | none | primary_text | NIST: failure began in early June 2021, before the death. |
| 9 | mcafee-and-surfside : mcafee-june8-tweet-posted | none | primary_text | Four fact-checks of the account's own record (absence, capped; anchor_checked secondary). |
| 10 | mcafee-and-surfside : mcafee-owned-unit | none | primary_text | Reported property-record reviews (absence; secondary). |
| 11 | proto-indo-european : anatolian-daughter-hypothesis | none | material | aDNA absence (legacy subject). |
| 12 | teti-pyramid-texts : pt-273-274-cannibalism-interpretation | motivated_error | material | "needs primary anchor"; anchor_checked no; evidential weight 1. |
| 13 | vaccines-autism : va-wakefield-paper-account-accurate | none | primary_text | Walker-Smith v GMC [2012] EWHC 503 (Admin) para 153: the ethics statement "was untrue". |
| 14 | vaccines-autism : va-measles-rna-gut | none | material | Hornig 2008, blinded three-laboratory replication. |
| 15 | vaccines-autism : va-thimerosal-removed-because-harmful | none | primary_text | MMWR 1999: "no data or evidence of any harm"; removal as a precaution. |
| 16 | vaccines-autism : va-henry-ford-shows-autism | none | primary_text | The draft's own Tables 2 and 3 and its text. |
| 17 | vaccines-autism : va-simpsonwood-autism-hidden | none | primary_text | The June 2000 transcript, all eight autism passages. |

(Run: `python3` over `claims.yaml` files, listing id, state, evidence_class, refutation_class. Rows 3-7 and 12 are the six that carry a class.)

### 1.3 What a reader cannot tell

- **Whether the class is evidence or a label.** In `main`, `lamp-lodygin-first-claim` has `refutation_class: narrative_drift` and its `basis` says "Class narrative_drift, not institutional_propaganda: the Soviet campaign is reported by one newspaper history and is not anchored here." The author applied the REVIEW.md bar by hand, correctly, for one class, and said so in prose. Nothing else in the repository does this, and the validator cannot see it.
- **That a class can be set with no origin evidence at all.** `pt-273-274-cannibalism-interpretation` (teti) says `motivated_error` on a claim with `anchor_checked: no`, `evidential_weight: 1`, and an anchor of type `needs-primary-anchor` ("Named in the source file, not read here"). `motivated_error` says someone's motive produced the error. Nothing read supports a motive for Faulkner (1924), or for anyone. This is exactly the imputation the repository's guardrails exist to prevent (docs/AGENT_RULES.md section 11: "an accusation is not a finding"), and the validator accepts it.
- **Whether a class's truth was checked.** `lamp-10000-ways-quote` is set to `narrative_drift`, but its transmission chain `tx-10000-ways` has one read event (the 1910 book, which is the true core) and five `read: no` events from a secondary source (Quote Investigator). The drift itself was not read. `lamp-edison-sole-inventor` and `lamp-latimer-invented-claim` have no transmission chain at all, so the page shows no instance of the false belief for either.
- **That an agent has already done this once.** `incandescent-lamp` log L-05 records "Class motivated_error, not fabrication, because no evidence read shows Göbel invented the story": a motive class chosen with no motive evidence, on a published dig. Review caught it, and L-15 moved the claim from refuted to contested with no class. Nothing in the validator would have caught it; review did, by hand.
- **Which question the reader is asking.** Take "a second North Vietnamese attack took place on 4 August 1964 is refuted". Was the belief a misreport, drift, or motivated error? The repository holds the answer in three other claims, not in a class: `tonkin-sigint-selectively-presented` (established, moderate: the intercepts reaching decision-makers were assembled selectively); `tonkin-midlevel-deliberate-skew` (proposed: individuals at NSA deliberately skewed it; Hanyok judges they themselves believed an attack had happened); `tonkin-senior-knowledge` (contested, low: whether senior officials knew). The refuted claim itself carries nothing. Hanyok's study also says the first belief arose from ship radar, sonar and visual reports (the dig's claim text quotes "overeager sonarmen" and "freak weather effects"), and that the summaries issued from late on 4 August were "deliberately skewed to support the notion that there had been an attack" while the NSA personnel "believed that the attack happened". A reader of `tonkin-aug4-attack-occurred` cannot tell that the intercepts contained "severe analytic errors, unexplained translation changes, and the conjunction of two unrelated messages" (Hanyok, as quoted in the claim's text) without reading four claims. None of the five existing classes fits the first part of that origin (signals and shipboard contacts read as an attack); the second part (deliberate skew) is a different claim, proposed and not established. See 3.2 and 5.2.
- **Whether the five classes are all the classes there are.** The vaccines-autism log, L-07, says `va-measles-rna-gut` fits "none of the five ... a good-faith hypothesis that failed a test, which suggests the gradient needs an 'honest_error' or 'failed_hypothesis' class." A claim set cannot be classified honestly if the set is incomplete, and the log says no one has been able to say.

### 1.4 Why this is a failure and not a preference

Rule 12 and REVIEW.md B each tell a person to check a bar that is not written. The only two possible results are a class set on the author's say-so (six claims on `main`, four of which fail the bars proposed here) or a class left off (11 claims on `main` and the branch, and the authors say so). Either way the reader is told something incorrect or nothing, and for the intent classes the incorrect result is an accusation.

## 2. Evidence

What was opened and run.

- `CONTRIBUTING.md` Rules 9 and 12 and the claim states table; `docs/REVIEW.md` section B (the two bars); `docs/AUTHENTICITY.md` (section 6 rule 4: a forgery finding needs a decisive anachronism or two independent lines of evidence); `build/SCHEMA.md` (claim fields, the open item, X1-X4, TH2, and rule A8 on digital items); `docs/AGENT_RULES.md` section 11; `docs/COORDINATION.md` item 2; `docs/PUBLISH_GATE.md`; `build/conformance.py` (the check at lines 182-187); `build/tools/review_dig.py` (which matches only `statement` and `anchor.description` against stored sources); `build/tools/build_teti_subject.py`; `method/index.html` line 58.
- Every `build/subjects/*/claims.yaml` for `state: refuted` (table in 1.2) and the claims, log, manifest and threads of `origin/dig/vaccines-autism`.
- Grep for `refutation_class` over the repository: used by the validator, the Teti generator (`build_teti_subject.py` line 65, a pass-through from the import files), the Teti import and utterance copies, and the five lamp claims; no page builder or review script reads it. A copy under `site/digs/` is generated and untracked.
- Baseline validator on a clean worktree of `origin/main`: `15 subjects and 107 shared nodes checked: 0 errors, 93 warnings`.
- Patch tests in the scratch worktree: `python3 build/tools/test_refutation_classes.py`: `Ran 18 tests ... OK`.
- The independent assessor opened seven origin documents and confirmed the quotations proposed here (Hanyok's "severe analytic errors, unexplained translation changes, and the conjunction of two unrelated messages"; Simpsonwood p. 44; Henry Ford Tables 2 and 3 against the manifest hash; Dyer and Martin 1910; Fontaine 1878; MMWR 1999; Walker-Smith para 153). It could not confirm the intercept reports 7, 12 and 13 (the stored OCR is too garbled) and it did not open the Scientific American 1874, Electrical World 1900, CBC 2017 or Kommersant pages. For those, "read" means the dig's manifest says so. The assessor found that `src-salon-2011` is recorded `read: full` and that rule A8 is in `build/SCHEMA.md`, not AUTHENTICITY.md; both are corrected here.

## 3. The proposed change

### 3.1 Principle and firewall

The class describes **how the false claim arose** (its origin and first transmission). It is separate from, and never raises, lowers or replaces, the evidence that the claim is **false**. That evidence is the claim's `anchor` and Rule 9. The class is also not a finding about anyone's state of mind: it says what the documents show about the origin, and the classes that allege intent say so only through the holder's own quoted words.

| Question | Where | Governed by |
|---|---|---|
| Is the claim false? | `anchor`, `evidence_class`, `evidential_weight`, `confidence` | Rule 9, N25 |
| How did the false belief arise? | `refutation_class` + `refutation_origin` | Rule 12 (this proposal), RC1-RC10 |
| How did it spread afterwards? | `transmission.yaml` | X1-X4, `confers_weight: false` |

The class confers no weight: it is not an anchor, it cannot be cited as one, and no check or page rule reads it to set a state, a weight, a headline or a publish status (RC10, tested twice: the Rule 9 verdict is identical with and without a class, and a test fails if any code other than the validator and the legacy Teti generator names the field). A refuted claim with no class is exactly as refuted as one with a class. The same standard applies to class words in prose: a headline, assessment, `basis` or thread that says "misattribution" or "drift" is held to the bar of the field (3.5). This is the same firewall as CONTRIBUTING section 3. A class is a statement about the history of an error and can itself be wrong, which is why it has its own confidence (RC4), separate from the claim's, and why it is optional.

### 3.2 The set: are five right?

Test: assign each of the 17 refuted claims from the five. Details in 5.2.

- `narrative_drift` fits rows 3 and 4 and, once their drift is read, 6, 7 and 15; `misattribution` fits row 5 (Latimer) once an instance of the false attribution is read.
- Six claims fit none of the five, in two groups:
  - **A record, document or data was taken to say what it does not**: Tonkin 4 August (intercepts analysed wrongly, and shipboard radar, sonar and visual contacts taken as an attack), Henry Ford (a draft whose tables show no association, said to show one), Simpsonwood (a transcript said to show the finding hidden). Three claims in two digs, pointing at a government account, a film and a campaign story. Proposed class: **`misreading`**, defined to cover contemporary records and sensor or witness data as well as documents. It is not `narrative_drift` (no true core retold through steps) and not `misattribution` (nothing credited to the wrong person or source).
  - **A hypothesis or interpretation that was tested or superseded**: `va-measles-rna-gut` (a mechanism proposed 1998-2002, then not replicated by three blinded laboratories including the original), `anatolian-daughter-hypothesis` (a scholarly hypothesis superseded), `pt-273-274-cannibalism-interpretation` (a 1924 scholarly interpretation). Proposed class: **`failed_hypothesis`**, the class the vaccines dig's author asked for (L-07 says `honest_error` or `failed_hypothesis`). The name says what happened (a hypothesis was tested) and the definition makes no claim about good faith: an earlier draft said "held in good faith", which is a state-of-mind finding made without evidence and the mirror image of the one this proposal guards against. The class says only that the origin is a hypothesis and what answered it, with `intent_searched: yes | no` recording whether anyone looked for evidence of intent.
- `satire_taken_literally`: no refuted claim in the repository is satire, so it is not added. A class with no case would be invented from outside; adding one takes the same proposal path.
- Not classed, no new class: `va-wakefield-paper-account-accurate` (a statement in a paper that a court called "untrue", with no finding of intent). A possible `misstatement` class has one case; it stays unclassed, a valid state (3.3).
- Apollo, Surfside and mcafee-owned-unit have no origin evidence in their digs; they stay unclassed.
- Limit: the classes cover claims already refuted under Rule 9. The strongest myths in the vaccines dig ("MMR causes autism") are `proposed` because statistics cannot refute under the owner's decision L-19 (option a), so they can receive no origin class. A class is never a route to `refuted`; `failed_hypothesis` applies only to a claim already refuted on material or primary-text evidence (the Hornig laboratory replication qualifies; a population statistic does not, and an author must not label statistics `material` to reach it).

The set proposed is seven. Owner choice 1 is to take the five only, or `misreading` alone.

### 3.3 Required or optional

**Optional, and checked whenever present.** 13 of the 17 refuted claims have no complete origin evidence in the repository; a required class would force a guess, which is the failure case, and an `unclassified` value is a class in name only. The cost of optional: a reader sees nothing where a class could be. Showing the class on the page is not part of this change (Owner choice 4): today no page reads the class, so nothing visible changes, and display is where harm would occur, so it should wait for a reviewer's tick (3.5) and its own proposal.

### 3.4 Definitions, minimum bars, exclusions, required fields, caps

Common to all seven: the class describes how the false belief arose, never whether it is false. The bar is about the origin and is in addition to Rule 9. `refutation_origin` always has `type` (fixed by the class), `description`, `sources` (manifest ids whose manifest `read` says yes, full or direct, not all of them the refutation's own anchor sources), `read: yes` and `confidence`. `confidence` rates the class, not the refutation; it is capped at moderate for the intent classes, and for every other class unless three distinct sources were read. The origin `type` is deliberately not the `anchor` type: the anchor is the evidence for falsity.

| Class | Definition | Minimum bar | Does NOT qualify | Required fields beyond the common ones |
|---|---|---|---|---|
| `narrative_drift` | A true statement or real event that changed in retelling until it said what the evidence does not support. | A transmission chain of this claim with at least two different forms of the claim among its read events, one of them the documented true core. | A claim that is merely popular. Forms known only from a secondary source marked `read: no`. A chain that shows spread but no change. A read event that is a later report of an earlier form, unless the `description` says so. | `chain` |
| `misattribution` | A real act, text or finding credited to the wrong person, group or source. | The true attribution shown by a dated document read, and one dated instance, read, where the credit goes to the claimed person or source. | Credit for something that did not happen. A recognition that overshoots, with no instance read. | `document_source`, `instance_source` (different, both in `sources`; the instance is not the refutation's anchor source), `passages.document`, `passages.instance` |
| `misreading` | A document, record or data set (including contemporaneous sensor, radar, sonar or witness reports) was taken to say what it does not. | The record or data and an instance of the false reading, both read, with the differing passages named. | A claim about a record that does not exist. A reading within the range of the record. A later, deliberate presentation of the record (that is a different origin: `see_also`). | as `misattribution` |
| `failed_hypothesis` | A hypothesis or interpretation that a test or later evidence did not support. Says nothing about the state of mind of those who held it. | The hypothesis stated in a document by its proponents, read (not the refutation's anchor source), and the test or evidence that answered it, read, and a refutation already valid under Rule 9. | Statistics offered as the answering test when Rule 9 would not accept them as refuting. A case where the proponent's own words show they knew otherwise (that is a different class). | `hypothesis_source`, `answering_source`, `passages.hypothesis`, `passages.answer`, `intent_searched: yes or no` |
| `fabrication` | An item or statement made up and presented as real. | A forgery finding meeting docs/AUTHENTICITY.md rule 4 (a decisive anachronism, or two independent lines of evidence) and at least two distinct sources. | A document found unreliable, mistaken or retracted. A hoax with no evidence the item was made rather than misread. A fact-checker's rating alone. A named maker is not required. | `anachronism` or `independent_lines` (two or more) |
| `motivated_error` | An error that the holder's own words show was shaped by a stated interest, commitment or purpose. | The holder named, with `holder_kind` institution or public_figure; the holder's own words (`quote`, 30 characters or more) from a source in `sources` (`quote_source`) at a stated `locator`; a `link` saying how those words connect the aim to this claim; a second source. | Interest, benefit, advocacy, profession, nationality, politics or silence, inferred by anyone, including us. "Who gains" is never enough. A private individual. A holder stating an aim that is not connected to this claim. | `holder`, `holder_kind`, `quote`, `quote_source`, `locator`, `link` |
| `institutional_propaganda` | A claim an institution issued or directed as part of a campaign to promote it. | The institution named; its own dated directive or publication (`quote`) from a source in `sources`, at a `locator`, showing the claim issued as policy or campaign; a `link`; a second source. | One institution's staff repeating a claim. A newspaper's account of a campaign as the only source. A government that was mistaken. | `institution`, `holder_kind`, `quote`, `quote_source`, `locator`, `link` |

What the validator can and cannot do with these fields. It checks presence, type and cross-references: the class and state, the fixed type, `read: yes`, that every source is a string in the manifest and read, that the origin is not wholly the refutation's own anchor, the pair of documents and passages, `intent_searched`, the holder kind, the quote length, that `quote_source` is among `sources`, `see_also` and `chain` resolve, and the caps. It cannot check that a quotation is real or that a description is true. For quotations, `review_dig.py` is extended (3.6) to match `refutation_origin.quote` and `.description` against the stored sources the way it already matches `anchor.description`; where a dig stores no source text (the lamp dig stores none), the check reports "no stored source to check against" and the independent reviewer must open the source. Two manifest ids that are the same document, or two secondary sources, still pass: independence is a reviewer judgement. `read` in the manifest is an author's statement, like `anchor_checked`.

Notes.
1. The intent classes are capped at moderate and need the actor's own words because a wrong class there is an accusation. Owner choice 3 asks whether the cap should be lower or the evidence higher. `fabrication` with a decisive anachronism could be allowed high, as AUTHENTICITY rule 4 would allow; the proposal keeps moderate.
2. A false belief with two origins gets one class and `see_also` pointing to the claims that record the other. Tonkin is the case (3.2, 5.2). Owner choice 6.
3. An unclassed claim is not a gap in the claim.

### 3.5 Text for build/SCHEMA.md and the owner-only files (not applied)

`build/SCHEMA.md`, checked with `git apply --check` against `origin/main`:

```diff
diff --git a/build/SCHEMA.md b/build/SCHEMA.md
index 9b9339c..dc7d4f4 100644
--- a/build/SCHEMA.md
+++ b/build/SCHEMA.md
@@ -13,7 +13,7 @@ Source of truth: `build/subjects/<subject>/{claims,tests,threads,log}.yaml`. Pag
 
 ## Claim fields (required unless noted)
 `id`, `state`, `statement`, `evidence_class`, `confidence`, `evidential_weight` (1-5), `anchor_checked`, `adoption_weight` (1-5), `adoption_note`, `would_change_if`, `anchor{type,description,accessible}`, `basis`.
-Conditional: `refutes_target` (when refuted); `next_step` (when searched_gap); `refutation_class` (only when refuted; classes undefined, see COORDINATION.md).
+Conditional: `refutes_target` (when refuted); `next_step` (when searched_gap); `refutation_class` (optional, only when refuted; with its `refutation_origin`, see Refutation classes below).
 
 | Field | Allowed values |
 |---|---|
@@ -40,7 +40,6 @@ Conditional: `refutes_target` (when refuted); `next_step` (when searched_gap); `
 
 ## Open items
 - ID scheme: `C-01` numbering (CONTRIBUTING) or slugs (PIE, Apollo, Tonkin). Suggested: numeric `id` plus a human `slug`.
-- `refutation_class` definitions and their evidential bars.
 - A validator. README-deploy.md refers to `build/conformance.py` and a 21-test suite; neither is in this repository.
 
 ---
@@ -368,3 +367,22 @@ CORRECTION in the log entry (`build_site.py` picks entries by that word); if the
 finding, follow the gate's revision loop (new log entry, revision round, independent check,
 visible correction). The validator does not enforce this paragraph. Recording a retraction turns the validator red until the claims carry
 `flagged_sources` and `source_notices` (intended).
+
+
+---
+## Refutation classes (RC1-RC10)
+
+`refutation_class` says how a false belief arose. It says nothing about whether the claim is refuted: that is Rule 9 alone, decided by the `anchor`. A class never adds or removes weight and is never cited as evidence (RC10). How a myth spread goes in `transmission.yaml`; the class only points to it. A class is not a finding about anyone's state of mind: it says what the documents show about the origin.
+
+Classes: `narrative_drift`, `misattribution`, `misreading`, `failed_hypothesis`, `fabrication`, `motivated_error`, `institutional_propaganda`.
+
+- **RC1** A class is optional. If set, the claim is `refuted` and carries a `refutation_origin` mapping. `refutation_origin` without a class is an error. A class on a claim that is not already refuted under Rule 9 is an error; a class is never a route to `refuted` (statistics, which cannot refute under Rule 9, cannot supply the "answer" of a `failed_hypothesis`).
+- **RC2** `refutation_origin.type` is fixed by the class (narrative_drift: transmission-chain; misattribution: attribution-record; misreading: reading-comparison; failed_hypothesis: hypothesis-record; fabrication: forgery-finding; motivated_error: stated-motive; institutional_propaganda: institutional-campaign). `description` says how the belief arose.
+- **RC3** `read: yes`. A class is never set on origin evidence that was not opened. Without it, leave the class off.
+- **RC4** `confidence` rates the class, not the refutation. The three intent classes are capped at moderate. The other classes are capped at moderate unless three distinct sources were read.
+- **RC5** `sources` are manifest ids whose manifest `read` says yes, full or direct. They may not all be the refutation's own anchor sources.
+- **RC6** misattribution and misreading need `document_source` and `instance_source` (two different members of `sources`) and `passages.document`, `passages.instance`; the instance of the false belief is not the refutation's own anchor source. failed_hypothesis needs `hypothesis_source` (not the refutation's anchor), `answering_source`, `passages.hypothesis`, `passages.answer` and `intent_searched: yes | no`; it says nothing about good faith or bad.
+- **RC7** The intent classes need two distinct sources. motivated_error and institutional_propaganda need `holder` or `institution`, `holder_kind` (institution or public_figure, never a private individual), `quote` (30 characters or more, the holder's own words), `quote_source` (one of `sources`), `locator`, and `link` (how those words connect the aim to this claim). fabrication needs `anachronism` or two `independent_lines` (docs/AUTHENTICITY.md rule 4). Benefit, silence or "who gains" never qualifies. `build/tools/review_dig.py` matches `quote` and `description` against stored sources.
+- **RC8** `see_also` (optional) lists other claims of the same subject that record a different or additional origin.
+- **RC9** `chain` names a chain in this subject's `transmission.yaml` whose `about` is this claim; required for narrative_drift, which needs two different read forms of the claim. A read event may itself be a later report of an earlier form: say so in `description`.
+- **RC10** No check reads the class to decide state, weight, headline or publish status. A class cannot be cited in `anchor` (TH2/X3 apply to chain ids). Class words in surface text (headline, assessment, basis, threads) are held to the same bar as the field (REVIEW.md B).
```

CONTRIBUTING.md Rule 12, docs/REVIEW.md B and method/index.html line 58 (which repeats Rule 12 on the public site) are owner-only. Proposed text, not applied:

> **Rule 12.** `refutation_class` is optional and may only be set on a claim whose state is `refuted`. It says how the false belief arose and carries no weight on whether the claim is refuted. Each class (`narrative_drift`, `misattribution`, `misreading`, `failed_hypothesis`, `motivated_error`, `institutional_propaganda`, `fabrication`) has its own evidential bar, in `build/SCHEMA.md` (RC1-RC10). The class never rests on belief, spread or who would gain; the classes that allege intent need the actor's own words.

> docs/REVIEW.md section B, replace the class line with: "Each `refutation_class` meets RC1-RC10. The validator cannot check that a `quote` is real or that a `description` is true: open the source. A class that names a person or institution whose own words are not in the quoted source, or a private individual, is a blocking finding. A class on a refutation whose origin is not read is removed, not downgraded. Class words in surface text (`headline`, assessment, `basis`, `adoption_note`, threads) are held to the same bar as the field: a page that says a claim is a misattribution, a drift or a propaganda campaign without the evidence is a finding. The independent reviewer records, in `review.yaml`, a tick for each class on the dig; before any class is displayed, and before any intent class is accepted on a published dig, that tick is required."

`method/index.html` line 58 takes the Rule 12 text above, with its markup.

### 3.6 The validator patch and the review-script extension (not applied)

`build/conformance.py`, as applied in the scratch worktree:

```diff
diff --git a/build/conformance.py b/build/conformance.py
index 8e0c5d7..2413c36 100644
--- a/build/conformance.py
+++ b/build/conformance.py
@@ -29,8 +29,20 @@ SUBJECTS = os.path.join(ROOT, "build", "subjects")
 STATES = {"established", "proposed", "contested", "refuted", "searched_gap"}
 CLASSES = {"material", "primary_text", "interpretive", "synthetic"}
 CLASS_ALIASES = {"primary-text": "primary_text"}  # older corpus spelling
-REFUTATION_CLASSES = {"narrative_drift", "misattribution", "motivated_error",
-                      "institutional_propaganda", "fabrication"}
+REFUTATION_CLASSES = {"narrative_drift", "misattribution", "misreading", "failed_hypothesis",
+                      "motivated_error", "institutional_propaganda", "fabrication"}
+# Rule 12 (SCHEMA RC1-RC10): the class says how the false belief arose. Its evidence is a separate
+# `refutation_origin` mapping and never part of the refutation's `anchor`.
+ORIGIN_TYPES = {"narrative_drift": "transmission-chain", "misattribution": "attribution-record",
+                "misreading": "reading-comparison", "failed_hypothesis": "hypothesis-record",
+                "fabrication": "forgery-finding", "motivated_error": "stated-motive",
+                "institutional_propaganda": "institutional-campaign"}
+INTENT_CLASSES = {"fabrication", "motivated_error", "institutional_propaganda"}
+# classes whose bar is two named documents: (field for the first, field for the second, passages keys)
+PAIR_FIELDS = {"misattribution": ("document_source", "instance_source", ("document", "instance")),
+               "misreading": ("document_source", "instance_source", ("document", "instance")),
+               "failed_hypothesis": ("hypothesis_source", "answering_source", ("hypothesis", "answer"))}
+HOLDER_KINDS = {"institution", "public_figure"}
 CONFIDENCE = {"high", "moderate", "low", "provisional"}
 # YAML reads a bare `no` as False; both mean "not checked".
 ANCHOR_CHECKED = {"no", "secondary", "primary"}
@@ -93,6 +105,131 @@ def check_anchor_format(r, subject, c, sdir):
                     r.err(where, f"anchor source `{s}` is not in sources/MANIFEST.yaml (SCHEMA N25)")
 
 
+def _nonempty(v):
+    return isinstance(v, str) and bool(v.strip())
+
+
+def _manifest_read(entry):
+    """True if the manifest says the source was read: a `read:` text starting yes, full or direct."""
+    v = (entry or {}).get("read")
+    if v is True:
+        return True
+    return isinstance(v, str) and v.strip().lower().startswith(("yes", "full", "direct"))
+
+
+def check_refutation_origin(r, subject, sdir, c):
+    """RC1-RC10 (SCHEMA.md, Refutation classes). A class is optional; when set it must show, in
+    `refutation_origin`, how the false belief arose. Nothing here changes whether a claim is refuted."""
+    rc = c.get("refutation_class")
+    if not isinstance(rc, str) or rc not in REFUTATION_CLASSES or c.get("state") != "refuted":
+        return                                       # name and state errors are raised in check_claim
+    where = f"{subject}:{c.get('id')}"
+    ro = c.get("refutation_origin")
+    if not isinstance(ro, dict):
+        r.err(where, f"RC1: refutation_class `{rc}` needs a `refutation_origin` mapping")
+        return
+    if ro.get("type") != ORIGIN_TYPES[rc]:
+        r.err(where, f"RC2: `{rc}` needs refutation_origin.type `{ORIGIN_TYPES[rc]}`, got `{ro.get('type')}`")
+    if not _nonempty(ro.get("description")):
+        r.err(where, "RC2: refutation_origin needs a `description` of how the false belief arose")
+    if ro.get("read") not in (True, "yes"):
+        r.err(where, "RC3: refutation_origin.read must be `yes`: a class is not set on origin evidence that was not read")
+    conf = ro.get("confidence")
+    if conf not in CONFIDENCE:
+        r.err(where, "RC4: refutation_origin.confidence must be high | moderate | low | provisional (it rates the class, not the refutation)")
+    manifest = load_sources(sdir) if sdir else {}
+    raw = ro.get("sources")
+    srcs = []
+    if not isinstance(raw, list) or not raw:
+        r.err(where, "RC5: refutation_origin needs `sources`, a non-empty list of manifest ids")
+    else:
+        for s_ in raw:
+            if not isinstance(s_, str):
+                r.err(where, f"RC5: refutation_origin source `{s_}` is not a manifest id (a string)")
+            elif s_ not in manifest:
+                r.err(where, f"RC5: refutation_origin source `{s_}` is not in sources/MANIFEST.yaml")
+            else:
+                srcs.append(s_)
+                if not _manifest_read(manifest[s_]):
+                    r.err(where, f"RC5: manifest says `{s_}` was not read (its `read` must start yes, full or direct)")
+    uniq = set(srcs)
+    asrc = (c.get("anchor") or {}).get("sources")
+    anchor_srcs = {x for x in asrc if isinstance(x, str)} if isinstance(asrc, list) else set()
+    if uniq and uniq <= anchor_srcs:
+        r.err(where, "RC5: the origin sources are all the refutation's own anchor sources; "
+                     "how the belief arose needs a document the refutation does not rest on")
+    # cap: high needs three distinct sources; the intent classes never reach high
+    if conf == "high" and rc in INTENT_CLASSES:
+        r.err(where, f"RC4: `{rc}` alleges intent; its origin confidence is capped at moderate")
+    elif conf == "high" and len(uniq) < 3:
+        r.err(where, f"RC4: `{rc}` origin confidence is capped at moderate unless three distinct sources are read")
+    # the two-document classes
+    if rc in PAIR_FIELDS:
+        f1, f2, pk = PAIR_FIELDS[rc]
+        a, b = ro.get(f1), ro.get(f2)
+        for k_, v in ((f1, a), (f2, b)):
+            if not isinstance(v, str) or v not in uniq:
+                r.err(where, f"RC6: `{rc}` needs `{k_}`, one of `sources`")
+        if isinstance(a, str) and a == b:
+            r.err(where, f"RC6: `{f1}` and `{f2}` must be two different documents")
+        if rc != "failed_hypothesis" and isinstance(b, str) and b in anchor_srcs:
+            r.err(where, f"RC6: `{f2}` is the refutation's own anchor source; the instance of the false belief must be another document")
+        if rc == "failed_hypothesis" and isinstance(a, str) and a in anchor_srcs:
+            r.err(where, "RC6: `hypothesis_source` is the refutation's own anchor source; the hypothesis must be stated in another document")
+        ps = ro.get("passages")
+        for k_ in pk:
+            if not isinstance(ps, dict) or not _nonempty(ps.get(k_)):
+                r.err(where, f"RC6: `{rc}` needs `passages.{k_}` naming the passage read")
+        if rc == "failed_hypothesis" and ro.get("intent_searched") not in (True, False, "yes", "no"):
+            r.err(where, "RC6: `failed_hypothesis` needs `intent_searched: yes | no` (the class says nothing about state of mind)")
+    # the intent classes
+    if rc in INTENT_CLASSES:
+        if len(uniq) < 2:
+            r.err(where, f"RC7: `{rc}` needs at least two distinct sources for the origin")
+        if rc == "fabrication":
+            lines = ro.get("independent_lines")
+            if not (_nonempty(ro.get("anachronism")) or (isinstance(lines, list) and len([x for x in lines if _nonempty(x)]) >= 2)):
+                r.err(where, "RC7: `fabrication` needs an `anachronism`, or two `independent_lines` (docs/AUTHENTICITY.md rule 4)")
+        else:
+            who = "holder" if rc == "motivated_error" else "institution"
+            if not _nonempty(ro.get(who)):
+                r.err(where, f"RC7: `{rc}` needs `{who}`")
+            if ro.get("holder_kind") not in HOLDER_KINDS:
+                r.err(where, "RC7: `holder_kind` must be institution | public_figure (a private individual is never named)")
+            qs = ro.get("quote_source")
+            if not isinstance(qs, str) or qs not in uniq:
+                r.err(where, "RC7: `quote_source` must be one of `sources`")
+            for k_ in ("quote", "locator", "link"):
+                if not _nonempty(ro.get(k_)):
+                    r.err(where, f"RC7: `{rc}` needs `{k_}` (the holder's own words, where they are, and how those words connect their aim to this claim; interest or benefit alone does not qualify)")
+            if _nonempty(ro.get("quote")) and len(ro["quote"].strip()) < 30:
+                r.err(where, "RC7: `quote` is too short to be the holder's own words (30 characters at least)")
+    # competing origins in the same dig
+    see = ro.get("see_also")
+    if see is not None:
+        cpath = os.path.join(sdir, "claims.yaml")
+        known = {x.get("id") for x in ((load(cpath) or {}).get("claims") or []) if isinstance(x, dict)} if os.path.exists(cpath) else set()
+        if not isinstance(see, list) or not all(isinstance(x, str) and x in known and x != c.get("id") for x in see):
+            r.err(where, "RC8: `see_also` must list other claim ids of this subject that record a different origin")
+    chain_id = ro.get("chain")
+    if rc == "narrative_drift" and not chain_id:
+        r.err(where, "RC9: `narrative_drift` needs `chain`, a transmission chain of this claim with dated steps read")
+    if chain_id is not None:
+        xpath = os.path.join(sdir, "transmission.yaml")
+        chains = {ch.get("id"): ch for ch in ((load(xpath) or {}).get("chains") or []) if isinstance(ch, dict)} \
+            if os.path.exists(xpath) else {}
+        ch = chains.get(chain_id) if isinstance(chain_id, str) else None
+        if ch is None:
+            r.err(where, f"RC9: chain `{chain_id}` is not in this subject's transmission.yaml")
+        elif ch.get("about") != f"{subject}:{c.get('id')}":
+            r.err(where, f"RC9: chain `{chain_id}` is about `{ch.get('about')}`, not this claim")
+        elif rc == "narrative_drift":
+            read_forms = {str(e.get("form")).strip().lower() for e in ch.get("events") or []
+                          if isinstance(e, dict) and e.get("read") in (True, "yes")}
+            if len(read_forms) < 2:
+                r.err(where, "RC9: `narrative_drift` needs at least two different forms of the claim, from read events of the chain")
+
+
 def check_claim(r, subject, c, legacy):
     cid = c.get("id", "<no id>")
     where = f"{subject}:{cid}"
@@ -178,13 +315,15 @@ def check_claim(r, subject, c, legacy):
             r.err(where, "Rule 9: refuted claim must name `refutes_target`")
         if ec not in ("material", "primary_text"):
             r.err(where, f"Rule 9: refutation must rest on material or primary_text, not `{ec}`")
-    # Rule 12
+    # Rule 12 (state and name; the evidence for the class is checked by check_refutation_origin)
     rc = c.get("refutation_class")
     if rc is not None:
         if state != "refuted":
             r.err(where, "Rule 12: refutation_class is only allowed on refuted claims")
-        if rc not in REFUTATION_CLASSES:
+        if not isinstance(rc, str) or rc not in REFUTATION_CLASSES:
             r.err(where, f"unknown refutation_class `{rc}`")
+    elif c.get("refutation_origin") is not None:
+        r.err(where, "RC1: `refutation_origin` without a `refutation_class`")
 
     if state == "searched_gap" and not c.get("next_step"):
         if c.get("gap_type") == "structural":
@@ -370,6 +509,7 @@ def check_subject(r, sdir):
             ids[cid] = c
             check_claim(r, subject, c, legacy)
             check_anchor_format(r, subject, c, sdir)
+            check_refutation_origin(r, subject, sdir, c)
 
         check_publication(r, subject, sdir, claims, d)
 
```

`build/tools/review_dig.py` (owner-only; proposed text). It adds the origin's quotation and description to the fields matched against stored sources; on the lamp dig the result is identical before and after (39 quotations, none found, because that dig stores no source text):

```diff
diff --git a/build/tools/review_dig.py b/build/tools/review_dig.py
index f57c00a..a9bedb6 100644
--- a/build/tools/review_dig.py
+++ b/build/tools/review_dig.py
@@ -87,7 +87,10 @@ def main():
             corpus += " " + norm(open(f, encoding="utf-8", errors="ignore").read())
     found = missing = unchecked = 0; miss = []
     for c in claims:
-        for field in (c.get("statement"), (c.get("anchor") or {}).get("description") if isinstance(c.get("anchor"), dict) else ""):
+        ro = c.get("refutation_origin") if isinstance(c.get("refutation_origin"), dict) else {}
+        # RC7: the origin's own words are matched against stored sources like any other quotation
+        for field in (c.get("statement"), (c.get("anchor") or {}).get("description") if isinstance(c.get("anchor"), dict) else "",
+                      ro.get("description"), f'"{ro["quote"]}"' if isinstance(ro.get("quote"), str) else ""):
             txt = N(field)
             if txt.count('"') % 2:                      # unbalanced quote marks: pairing would be wrong, leave it to the manual check
                 continue
```

### 3.7 Unit tests

New file `build/tools/test_refutation_classes.py`: 18 tests, passing in the scratch worktree (`Ran 18 tests ... OK`). Synthetic subjects only. It covers each class valid with its evidence; unknown and non-string class; class on a non-refuted claim; origin without a class and a class without origin; wrong type; origin not read; sources not in the manifest, not read, or without a `read` field; non-string sources (`[["a"]]`, a bare string, a mapping, `None`) producing an error instead of the TypeError the first draft raised; origin wholly the refutation's anchor; the two-document classes (same document twice, instance in the refutation's anchor, missing or empty passages); `failed_hypothesis` fields; the confidence caps for every class; the intent classes (one source, a one-character quote, each missing field, `quote_source` outside `sources`, a private individual); `see_also`; the drift chain (one form, forms differing only in case, wrong chain, missing chain, non-string chain); the firewall that the Rule 9 verdict is identical with and without a class; the firewall that no code outside the validator, this test and the legacy Teti generator names the field; and a neutrality test that varies what the validator reads, namely the holder and its kind across a defence ministry, a tobacco company, a university department and a senator, and shows the same evidence gives the same verdict for all and removing the same evidence fails all. (The first draft varied `refutes_target`, which the validator never reads, so it could not fail; it is replaced.)

```python
#!/usr/bin/env python3
"""Tests for refutation classes (rules RC1-RC10 in build/conformance.py).

    python3 build/tools/test_refutation_classes.py

Synthetic subjects only. Includes the firewall tests (the class never changes whether a claim is refuted,
and no code outside the validator reads it) and the neutrality test (the verdict depends only on the
evidence fields, not on who the holder is or which way the claim points)."""
import copy, glob, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import yaml
import conformance as cf

SOURCES = [{"id": "src-a", "read": "yes, directly"}, {"id": "src-o1", "read": "yes, directly"},
           {"id": "src-o2", "read": "full"}, {"id": "src-o3", "read": "yes"},
           {"id": "src-unread", "read": "no"}, {"id": "src-noread"}]
QUOTE = "We must keep this line in the public mind whatever the evidence shows."


def chain(about="s:c1", forms=("true core", "stretched")):
    ev = [{"id": f"e{i}", "date": f"19{i}0-01-01", "step": "origin", "form": f, "source": "src-o1", "read": "yes"}
          for i, f in enumerate(forms)]
    return {"chains": [{"id": "tx-1", "about": about, "confers_weight": False, "events": ev}]}


def dump(doc, path):
    with open(path, "w") as f:
        yaml.safe_dump(doc, f)


def run(claim, tx=None, other_claims=()):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "sources"))
    dump({"sources": SOURCES}, os.path.join(d, "sources", "MANIFEST.yaml"))
    dump({"claims": [claim] + list(other_claims)}, os.path.join(d, "claims.yaml"))
    if tx:
        dump(tx, os.path.join(d, "transmission.yaml"))
    r = cf.Report()
    cf.check_claim(r, "s", claim, False)
    cf.check_refutation_origin(r, "s", d, claim)
    return r


def refuted(cls=None, origin=None, state="refuted", ec="primary_text"):
    c = {"id": "c1", "state": state, "evidence_class": ec, "refutes_target": "t", "confidence": "high",
         "anchor": {"type": "primary_text", "description": "d", "sources": ["src-a"]}}
    if cls:
        c["refutation_class"] = cls
    if origin is not None:
        c["refutation_origin"] = origin
    return c


def org(typ, **kw):
    o = {"type": typ, "description": "how it arose", "sources": ["src-o1", "src-o2"], "read": "yes", "confidence": "moderate"}
    o.update(kw)
    return o


PAIR = dict(document_source="src-o1", instance_source="src-o2", passages={"document": "p. 4", "instance": "p. 9"})
GOOD = {
    "misreading": org("reading-comparison", **PAIR),
    "misattribution": org("attribution-record", **PAIR),
    "failed_hypothesis": org("hypothesis-record", hypothesis_source="src-o1", answering_source="src-o2",
                             passages={"hypothesis": "p. 2", "answer": "p. 7"}, intent_searched="no"),
    "fabrication": org("forgery-finding", independent_lines=["ink test", "template match"]),
    "motivated_error": org("stated-motive", holder="A Ministry", holder_kind="institution", quote=QUOTE,
                           quote_source="src-o1", locator="p. 3", link="The aim stated there is the claim made here."),
    "institutional_propaganda": org("institutional-campaign", institution="A Ministry", holder_kind="institution",
                                    quote=QUOTE, quote_source="src-o1", locator="p. 3", link="The directive orders this claim."),
}


def rc_errors(r):
    return [e for e in r.errors if "RC" in e or "Rule 12" in e or "refutation_class" in e]


def has(r, text):
    return any(text in e for e in r.errors)


class Classes(unittest.TestCase):
    def test_no_class_is_valid(self):
        self.assertEqual(rc_errors(run(refuted())), [])

    def test_unknown_class_and_non_string_class(self):
        self.assertTrue(has(run(refuted("satire_taken_literally", org("x"))), "unknown refutation_class"))
        self.assertTrue(has(run(refuted(["misreading"], org("x"))), "unknown refutation_class"))

    def test_class_on_non_refuted(self):
        self.assertTrue(has(run(refuted("misreading", GOOD["misreading"], state="proposed", ec="interpretive")), "only allowed on refuted"))

    def test_origin_without_class_and_class_without_origin(self):
        self.assertTrue(has(run(refuted(origin=GOOD["misreading"])), "RC1"))
        self.assertTrue(has(run(refuted("misreading")), "RC1"))

    def test_each_class_valid_with_evidence(self):
        for cls, o in GOOD.items():
            self.assertEqual(rc_errors(run(refuted(cls, o))), [], cls)
        self.assertEqual(rc_errors(run(refuted("narrative_drift", org("transmission-chain", chain="tx-1")), chain())), [])

    def test_wrong_type_and_not_read(self):
        self.assertTrue(has(run(refuted("misreading", dict(GOOD["misreading"], type="forgery-finding"))), "RC2"))
        self.assertTrue(has(run(refuted("misreading", dict(GOOD["misreading"], read="no"))), "RC3"))

    def test_sources_must_be_read_in_the_manifest(self):
        for bad in ("src-unread", "src-noread", "src-zzz"):
            o = dict(GOOD["misreading"], sources=["src-o1", bad], instance_source=bad)
            self.assertTrue(has(run(refuted("misreading", o)), "RC5"), bad)

    def test_non_string_sources_do_not_crash(self):
        for bad in ([["a"]], [{"a": 1}], "src-o1", [None]):
            r = run(refuted("misreading", dict(GOOD["misreading"], sources=bad)))
            self.assertTrue(has(r, "RC5"), bad)
        r = run(refuted("misreading", GOOD["misreading"]) | {"anchor": {"type": "x", "description": "d", "sources": [["a"]]}})
        self.assertIsNotNone(r)

    def test_origin_sources_all_in_the_refutation_anchor_is_an_error(self):
        o = dict(GOOD["misreading"], sources=["src-a"], document_source="src-a", instance_source="src-a")
        self.assertTrue(has(run(refuted("misreading", o)), "own anchor sources"))

    def test_pair_classes_need_two_documents_and_passages(self):
        for cls in ("misreading", "misattribution"):
            self.assertTrue(has(run(refuted(cls, dict(GOOD[cls], instance_source="src-o1"))), "two different documents"), cls)
            self.assertTrue(has(run(refuted(cls, dict(GOOD[cls], instance_source="src-a"))), "RC6"), cls)  # not in sources
            no_p = {k: v for k, v in GOOD[cls].items() if k != "passages"}
            self.assertTrue(has(run(refuted(cls, no_p)), "passages.document"), cls)
            self.assertTrue(has(run(refuted(cls, dict(GOOD[cls], passages={"document": "p. 4", "instance": " "}))), "passages.instance"), cls)
        # the instance of the false belief may not be the refutation's own evidence
        o = dict(GOOD["misreading"], sources=["src-o1", "src-a"], instance_source="src-a")
        self.assertTrue(has(run(refuted("misreading", o)), "refutation's own anchor source"))

    def test_failed_hypothesis_fields(self):
        g = GOOD["failed_hypothesis"]
        self.assertTrue(has(run(refuted("failed_hypothesis", {k: v for k, v in g.items() if k != "intent_searched"})), "intent_searched"))
        self.assertTrue(has(run(refuted("failed_hypothesis", dict(g, hypothesis_source="src-a", sources=["src-a", "src-o2"]))), "hypothesis_source"))
        self.assertEqual(rc_errors(run(refuted("failed_hypothesis", dict(g, intent_searched="yes")))), [])

    def test_confidence_caps(self):
        for cls in ("misreading", "misattribution", "failed_hypothesis"):
            self.assertTrue(has(run(refuted(cls, dict(GOOD[cls], confidence="high"))), "capped at moderate"), cls)
            three = dict(GOOD[cls], confidence="high", sources=["src-o1", "src-o2", "src-o3"])
            self.assertEqual(rc_errors(run(refuted(cls, three))), [], cls)
        for cls in ("fabrication", "motivated_error", "institutional_propaganda"):
            three = dict(GOOD[cls], confidence="high", sources=["src-o1", "src-o2", "src-o3"])
            self.assertTrue(has(run(refuted(cls, three)), "alleges intent"), cls)

    def test_intent_classes_need_more_than_a_non_empty_string(self):
        for cls in ("motivated_error", "institutional_propaganda"):
            g = GOOD[cls]
            self.assertTrue(has(run(refuted(cls, dict(g, sources=["src-o1"]))), "two distinct"), cls)
            self.assertTrue(has(run(refuted(cls, dict(g, quote="x"))), "too short"), cls)
            for k in ("quote", "locator", "link", "quote_source", "holder_kind"):
                self.assertTrue(rc_errors(run(refuted(cls, {a: b for a, b in g.items() if a != k}))), f"{cls} without {k}")
            self.assertTrue(has(run(refuted(cls, dict(g, quote_source="src-o3"))), "quote_source"), cls)
            self.assertTrue(has(run(refuted(cls, dict(g, holder_kind="private_individual"))), "never named"), cls)
        self.assertTrue(has(run(refuted("fabrication", org("forgery-finding", anachronism="x", independent_lines=[]) | {"anachronism": " "})), "fabrication"))
        self.assertEqual(rc_errors(run(refuted("fabrication", org("forgery-finding", anachronism="ink first made in 1954")))), [])

    def test_see_also_must_name_other_claims_of_the_subject(self):
        other = {"id": "c2", "state": "proposed"}
        g = dict(GOOD["misreading"], see_also=["c2"])
        self.assertEqual(rc_errors(run(refuted("misreading", g), other_claims=[other])), [])
        self.assertTrue(has(run(refuted("misreading", g)), "RC8"))
        self.assertTrue(has(run(refuted("misreading", dict(GOOD["misreading"], see_also=["c1"])), other_claims=[other]), "RC8"))

    def test_drift_needs_two_read_forms_and_matching_chain(self):
        o = org("transmission-chain", chain="tx-1")
        self.assertTrue(has(run(refuted("narrative_drift", o), chain(forms=("one",))), "two different forms"))
        self.assertTrue(has(run(refuted("narrative_drift", o), chain(forms=("a", "A"))), "two different forms"))
        self.assertTrue(has(run(refuted("narrative_drift", o), chain(about="s:other")), "not this claim"))
        self.assertTrue(has(run(refuted("narrative_drift", org("transmission-chain"))), "RC9"))
        self.assertTrue(has(run(refuted("narrative_drift", org("transmission-chain", chain=["x"]))), "RC9"))

    def test_firewall_class_never_changes_rule_9(self):
        base = run(refuted(ec="interpretive")).errors
        classed = run(refuted("misreading", GOOD["misreading"], ec="interpretive")).errors
        self.assertTrue(any("Rule 9" in e for e in base))
        self.assertEqual([e for e in classed if "Rule 9" in e], [e for e in base if "Rule 9" in e])

    def test_firewall_no_code_outside_the_validator_reads_the_class(self):
        """Only the validator, this test, and the legacy Teti generator (a pass-through) may name the field."""
        allowed = {"conformance.py", "test_refutation_classes.py", "build_teti_subject.py"}
        users = set()
        for p in glob.glob(os.path.join(ROOT, "build", "**", "*.py"), recursive=True) + glob.glob(os.path.join(ROOT, "*.py")):
            with open(p, encoding="utf-8", errors="ignore") as f:
                if "refutation_class" in f.read():
                    users.add(os.path.basename(p))
        self.assertIn("conformance.py", users)
        self.assertLessEqual(users, allowed)

    def test_neutrality_verdict_depends_only_on_the_evidence(self):
        """The same evidence, with the holder changed across a government, a company, a university and a public
        figure, gives the same verdict for every one; and removing the same piece of evidence fails every one."""
        holders = [("A Ministry of Defence", "institution"), ("A tobacco company", "institution"),
                   ("A university department", "institution"), ("A named senator", "public_figure")]
        for cls in ("motivated_error", "institutional_propaganda"):
            who = "holder" if cls == "motivated_error" else "institution"
            verdicts, broken = set(), set()
            for name, kind in holders:
                o = dict(GOOD[cls], holder_kind=kind)
                o[who] = name
                verdicts.add(tuple(rc_errors(run(refuted(cls, o)))))
                bad = {k: v for k, v in o.items() if k != "quote"}
                broken.add(tuple(rc_errors(run(refuted(cls, bad)))))
            self.assertEqual(verdicts, {()}, cls)
            self.assertEqual(len(broken), 1, cls)
            self.assertTrue(list(broken)[0], cls)


if __name__ == "__main__":
    unittest.main()
```

## 4. What it does not change

- **No state changes.** Rule 9 is untouched. A claim without a class is refuted exactly as now, and a class is never a route to `refuted` (RC1).
- **No weight changes.** `evidential_weight`, `adoption_weight`, `confidence`, `anchor_checked`, headline eligibility and the publish gate never read the class (RC10; two firewall tests). The class cannot be cited in `anchor`.
- **No finding changes.** What every claim says, and its state, weight and anchor, are as now. The migration (5.3) edits only the class field, the new origin block, and four pieces of published prose that name the removed classes (`incandescent-lamp` assessment text and thread wording, and the basis of one claim); each is a correction logged as a new entry (L-25 for lamp, L-05 for teti), not a change of finding.
- **No change to `transmission.yaml`**, X1-X4, TH1-TH4, or the anchor format (N25): `refutation_origin` is not an anchor.
- **What a class removal on a published dig needs.** `incandescent-lamp` is published and `review.yaml` (passed_with_open_items, five rounds) is owner-only and is not written by the author. Per docs/PUBLISH_GATE.md, a change to a published dig needs: a new append-only log entry (drafted in 5.3); the prose corrected so the page does not keep asserting the removed class; review of the pull request by an independent agent; and a recorded round or open item from that reviewer in `review.yaml`. A visible correction on the corrections page is not needed while no page displays the class. Teti is not published and has no `review.yaml`; it needs the log entry and the generator, import and utterance fixes.
- It does not decide any open question in a dig (for example Rule 9 for statistics, vaccines-autism L-05 and L-19).

## 5. Impact

### 5.1 Validator output on all 15 digs

Scratch worktree `git worktree add --detach <scratchpad>/rc2 origin/main`; command `python3 build/conformance.py --base origin/main`. Three runs: (a) before, (b) the validator patch only, (c) patch plus migration (5.3). Totals: (a) `0 errors, 93 warnings`; (b) `6 errors, 93 warnings`; (c) `0 errors, 93 warnings` (the WARNING lines are identical to (a), checked with `diff`). The `--base` run also checks that the log entries added in (c) are append-only.

| Dig | (a) before | (b) patch only | (c) patch + migration |
|---|---|---|---|
| apollo-landings | 0E / 5W | 0E / 5W | 0E / 5W |
| casket-letters | 0E / 4W | 0E / 4W | 0E / 4W |
| chemtrails | 0E / 0W | 0E / 0W | 0E / 0W |
| congress-promise-vote | 0E / 0W | 0E / 0W | 0E / 0W |
| dyatlov-pass | 0E / 0W | 0E / 0W | 0E / 0W |
| eikon-basilike | 0E / 2W | 0E / 2W | 0E / 2W |
| flood-myths-worldwide | 0E / 0W | 0E / 0W | 0E / 0W |
| flydubai-fz1073 | 0E / 8W | 0E / 8W | 0E / 8W |
| gulf-of-tonkin | 0E / 2W | 0E / 2W | 0E / 2W |
| incandescent-lamp | 0E / 3W | **5E** / 3W | 0E / 3W |
| mcafee-and-surfside | 0E / 3W | 0E / 3W | 0E / 3W |
| proto-indo-european | 0E / 42W | 0E / 42W | 0E / 42W |
| teti-pyramid-texts | 0E / 23W | **1E** / 23W | 0E / 23W |
| votes-2009-present | 0E / 0W | 0E / 0W | 0E / 0W |
| votes-johnson-tonkin | 0E / 0W | 0E / 0W | 0E / 0W |

The six errors in (b) are the six RC1 errors: `lamp-lodygin-first-claim`, `lamp-canada-invented-claim`, `lamp-latimer-invented-claim`, `lamp-10000-ways-quote`, `lamp-edison-sole-inventor` (each "refutation_class ... needs a `refutation_origin` mapping") and `teti-pyramid-texts:pt-273-274-cannibalism-interpretation` (the same). A sixteenth subject, `vaccines-autism` on `origin/dig/vaccines-autism` (not on `main`), has no class; with the patch the same six errors appear (inherited from `main`) and none in that dig.

### 5.2 Proposed class for each existing refuted claim, with evidence

"Read" means the dig's own file says the origin document was read, except where the assessor opened it (2). A class is proposed only where the bars of 3.4 are met by what the files say; otherwise the cell says why not. "Partial" means part of the bar is met and the rest is named.

| # | Claim | Class proposed | Evidence in the repository for how the belief arose | Bar met? |
|---|---|---|---|---|
| 1 | apollo-landings : apollo-staged-hoax | **Cannot be assigned: evidence of origin not read.** | Poll shares (6% in 1999, about 11-12% later; a Newsweek item "not read; unchecked"); no document on where the hoax belief arose; no `transmission.yaml`. | No. |
| 2 | gulf-of-tonkin : tonkin-aug4-attack-occurred | `misreading` is the candidate, with `see_also` to `tonkin-midlevel-deliberate-skew` and `tonkin-sigint-selectively-presented`. **Partial; no class in the migration.** | Hanyok [read; the assessor confirmed]: the few intercepts supporting an attack "contained severe analytic errors, unexplained translation changes, and the conjunction of two unrelated messages". The same study says the first belief also arose from shipboard radar, sonar and visual contacts, and that the summaries issued from late on 4 August were "deliberately skewed to support the notion that there had been an attack", while the NSA personnel "believed that the attack happened". | Partial. `misreading` shows only the milder half. The bar needs a document read (the intercepts: stored OCR too garbled to confirm reports 7, 12, 13) and an instance of the false reading read (the 4 August summaries or the Navy report; known through Prados, secondary). Not `motivated_error`: the deliberate-skew claim is proposed only. Not `institutional_propaganda`: no directive quoted. |
| 3 | incandescent-lamp : lamp-lodygin-first-claim | `narrative_drift` (keep), moderate. **Partial.** | `tx-lodygin-priority`: 1874 Lodygin first to put carbon in a sealed vessel (Fontaine 1878, read by the assessor); 1927 Howell and Schroeder; 1947-48 "made the lamp before Edison, who only improved it". | Partial. All four events are `read: yes`, but the last step is known only from a 2022 Kommersant history ("no Soviet newspaper of 1947-48 was read ... reported, not verified"), and the 1874 form only through Fontaine. The origin `description` says so. Not `institutional_propaganda`, as the claim's own basis says: one newspaper history, no directive. |
| 4 | incandescent-lamp : lamp-canada-invented-claim | `narrative_drift` (keep), moderate. **Met.** | `tx-canada-sale`: 1874 Scientific American "a patent for an electric light" (true core); 1900 Electrical World "purchased by Mr. Edison"; 2017 CBC "behind Edison's breakthrough". All `read: yes` in the manifest (not opened by the assessor). | Yes. |
| 5 | incandescent-lamp : lamp-latimer-invented-claim | **Cannot be assigned: no dated instance of the false attribution is read.** Candidate: `misattribution`. | The patents show his real work (read). The adoption note says it "grows out of real neglect" with no source. No chain. | No. Remove the class. |
| 6 | incandescent-lamp : lamp-10000-ways-quote | **Cannot be assigned: the drift is not read.** Candidate: `narrative_drift`. | `tx-10000-ways`: one read form (Dyer and Martin 1910, the true core, about a storage battery; the assessor confirmed it); the 1946 and 1982 forms and the 1921 and 1882 items are `read: no`. Already provisional. | No: one read form. Remove the class. |
| 7 | incandescent-lamp : lamp-edison-sole-inventor | **Cannot be assigned: no chain, no instance read.** Candidate: `narrative_drift`. | The `basis` argues the stretch; the adoption note cites schoolbooks and "the quote myth" with no source. | No. Remove the class. |
| 8 | mcafee-and-surfside : surfside-deliberate-timed-to-mcafee | **Cannot be assigned: evidence of origin not read.** | Rests on the claimed tweet and unit (rows 9, 10), both refuted; nobody who originated the theory is identified. `motivated_error` and `institutional_propaganda` excluded: no one's words are read. | No. |
| 9 | mcafee-and-surfside : mcafee-june8-tweet-posted | `fabrication` is the candidate. **Partial; not set.** | Four fact-checkers found no such post; USA Today notes a genuine 8 June tweet has the same timestamp ("could have been the template for a digitally fabricated tweet"); the screenshot gives "88th Street" for 8777 Collins Avenue. The manifest records it forged, strength moderate. Two lines of evidence (rule 4). | Partial. The item itself was not seen, only its text as quoted by the fact-checkers (the manifest says so), and rule A8 in `build/SCHEMA.md` asks for an independent capture. The claim is `anchor_checked: secondary`. If set, at most low to moderate. |
| 10 | mcafee-and-surfside : mcafee-owned-unit | **Cannot be assigned: evidence of origin not read.** | The ownership belief comes from the same screenshot; no source shows how it arose separately. | No. |
| 11 | proto-indo-european : anatolian-daughter-hypothesis | **Cannot be assigned: evidence of origin not read.** Candidate: `failed_hypothesis`. | Legacy subject; no document stating the hypothesis is read; no manifest. | No. |
| 12 | teti-pyramid-texts : pt-273-274-cannibalism-interpretation | **Cannot be assigned: evidence of origin not read.** Candidate: `failed_hypothesis`. Remove the present `motivated_error`. | Faulkner (1924) and Eyre 2002 are "named in the source file, not read here". Nothing read gives a motive. | No. The present class fails RC1 and RC7. (The refutation itself rests on absence of archaeology and "scholarly consensus"; Rule 9 says consensus cannot refute. That is a separate matter for the dig's owner.) |
| 13 | vaccines-autism : va-wakefield-paper-account-accurate | **Cannot be assigned: evidence of origin not read.** Not `fabrication` yet. | The court (read in full) says the ethics statement "was untrue and should not have been included" and makes no finding of intent. The GMC findings are "not reachable"; Deer (2011) and Godlee (2011) are read by tool summary only. | No. |
| 14 | vaccines-autism : va-measles-rna-gut | **Cannot be assigned yet.** Candidate: `failed_hypothesis`. | The answering test is read in full (Hornig 2008). The proponents' reports (1998-2002) are read only "as cited in the paper"; Wakefield 1998 is abstract only. | Not until a proponents' document is read. |
| 15 | vaccines-autism : va-thimerosal-removed-because-harmful | **Cannot be assigned: no dated instance of the stretched form is read.** Candidate: `narrative_drift`. | The true core is read (MMWR 1999: removal "as soon as possible" because "any potential risk is of concern", with "no data or evidence of any harm"; the assessor confirmed). No instance of "removed because harmful" is cited. | No. |
| 16 | vaccines-autism : va-henry-ford-shows-autism | `misreading` (not `misattribution`, as L-07 proposed). **Partial.** | The document is read in full (Tables 2 and 3; the assessor confirmed the figures against the manifest hash). Instances: Siri testimony (read by tool) and the film (not in the manifest). | Partial: the instance passage must be quoted. |
| 17 | vaccines-autism : va-simpsonwood-autism-hidden | `misreading` (L-07 proposed `narrative_drift`). **Partial.** | The transcript is read in full (p. 44; confirmed by the assessor). The instance, the 2005 "Deadly Immunity" article, is known only through its retraction; `src-salon-2011` is read in full, but it is the correction, not the false article. | Partial: the false instance must be quoted. |

Count of the 17: met in full today, 1 (row 4); partial, 5 (rows 2, 3, 9, 16, 17); a candidate class that needs one more document read, 7 (rows 5, 6, 7, 11, 12, 14, 15); no candidate, 4 (rows 1, 8, 10, 13). Of the six classes set on `main` today: 1 (row 4) is met in full, 1 (row 3) is partial, 4 (rows 5, 6, 7, 12) fail.

### 5.3 Migration (what applying it would take)

Applied in the scratch worktree and validated (0 errors, warnings unchanged, `--base` append-only check passed). Each edit to a published claim needs the gate in section 4.

- `incandescent-lamp` (published): add `refutation_origin` to rows 3 and 4; remove the class from rows 5, 6, 7; correct three phrases of published prose that name the removed classes (assessment text, `claims.yaml` line 29, "a Latimer misattribution is refuted" becomes "the claim that Latimer invented the bulb is refuted"; `threads.yaml` line 29 and the `basis` of `lamp-edison-sole-inventor`, "the drift is to" becomes "the stretch is to"); append log entry L-25 (drafted in the diff). L-05 and L-15 stay as written.
- `teti-pyramid-texts` (not published): remove `motivated_error` from `claims.yaml`, from `build/imports/teti-pyramid-texts/batch1/pt_273_274.yaml` and from `utterances/pt_273_274.yaml`; append log entry L-05 (drafted). The generator `build/tools/build_teti_subject.py` (owner-only, line 65) copies the field from the import file: with the field removed, regenerating writes `refutation_class: null`, which the validator accepts (it ignores a null) but which adds a line; the generator should only emit the key when it has a value. Re-running the generator without fixing the import would restore the class.
- `gulf-of-tonkin`: no class set (partial, row 2). If the owner takes `misreading`, add the class once the intercepts and an instance of the false reading are read, with `see_also`.
- `vaccines-autism` (branch, not yet on `main`): rows 13-17 stay unclassed until the missing documents are read.
- Owner-only text edits: CONTRIBUTING Rule 12, docs/REVIEW.md B, `method/index.html` line 58, `build/tools/review_dig.py` (3.5, 3.6).
- 12 of the 15 digs have no change.

Edits as made in the scratch worktree (for the assessor; not applied):

```diff
diff --git a/build/imports/teti-pyramid-texts/batch1/pt_273_274.yaml b/build/imports/teti-pyramid-texts/batch1/pt_273_274.yaml
index bb5ab6e..e46ba93 100644
--- a/build/imports/teti-pyramid-texts/batch1/pt_273_274.yaml
+++ b/build/imports/teti-pyramid-texts/batch1/pt_273_274.yaml
@@ -285,7 +285,6 @@ divergence_points:
       PT 273–274 reflects actual prehistoric cannibalistic practices that were
       'enshrined in religious literature' (Faulkner 1924).
     state: refuted
-    refutation_class: motivated_error
     refutation_basis: >
       No archaeological evidence of cannibalism in Fifth or Sixth Dynasty Egypt exists.
       Faulkner himself qualified the claim. The overwhelming scholarly consensus
diff --git a/build/subjects/incandescent-lamp/claims.yaml b/build/subjects/incandescent-lamp/claims.yaml
index a68dd44..429b2bc 100644
--- a/build/subjects/incandescent-lamp/claims.yaml
+++ b/build/subjects/incandescent-lamp/claims.yaml
@@ -26,7 +26,7 @@ assessment:
     Cragside (1880, per an archive blog, a proposed claim only) and the Savoy stage (28 December 1881, per a transcription of The Times), both before Edison's Pearl
     Street service began on 4 September 1882, but no document read shows who first made or sold a practical lamp. On the fourth, Edison's
     company is the one documented, and nothing earlier was searched for. Two national stories (Lodygin's, and Woodward and Evans's) each hold a real record that
-    is stretched beyond what it shows (Lodygin's "first" is refuted, the Canadian sale is unsupported on the documents read), and a Latimer misattribution is refuted on his patents; the Goebel
+    is stretched beyond what it shows (Lodygin's "first" is refuted, the Canadian sale is unsupported on the documents read), and the claim that Latimer invented the bulb is refuted on his patents; the Goebel
     1854 lamps are contested, resting on affidavit testimony (about forty affidavits per Colt J.) that US courts weighed differently on preliminary
     motions, with no dated document from before 1882 either way; de Changy's 1858 lamps are known only through Fontaine and his claim to be first is not dug.
     One stated standard (S1 to S4, in the description) is applied to every claimant, but the depth differs: some anchors are patent abridgments, a blog or
@@ -343,6 +343,13 @@ claims:
     state: refuted
     refutes_target: "Lodygin was the first inventor of the incandescent lamp (the first to describe or patent it)"
     refutation_class: narrative_drift
+    refutation_origin:
+      type: transmission-chain
+      chain: tx-lodygin-priority
+      description: "Chain tx-lodygin-priority: 1874, Lodygin reported as first to put carbon in a sealed oxygen-free vessel (Fontaine 1878, read); 1927, Howell and Schroeder repeat the prize story (read); 1947-48, press said to credit him with the lamp before Edison, who only improved it. LIMIT: that last step is known only from a 2022 Kommersant history; no 1947-48 Soviet text was read."
+      sources: [src-fontaine-1878, src-howell-schroeder-1927, src-kommersant-campaign]
+      read: yes
+      confidence: moderate
     statement: >
       Lodygin was not the first to patent an electric light or lamp in an enclosed globe: a British patent of 1841 (de Moleyns) covers an electric
       light fed with pulverized charcoal in an exhausted glass globe (the Supreme Court calls it incandescent; the abridgment does not), and one of 1845
@@ -499,6 +506,13 @@ claims:
     state: refuted
     refutes_target: "Woodward and Evans invented the light bulb, and Edison's lamp was built on their patent"
     refutation_class: narrative_drift
+    refutation_origin:
+      type: transmission-chain
+      chain: tx-canada-sale
+      description: "Chain tx-canada-sale: 1874 Scientific American notice of a patent for an electric light (the true core); 1900 Electrical World, a patent 'purchased by Mr. Edison'; 2017 CBC, the Canadian patent 'behind Edison's breakthrough'. All three read."
+      sources: [src-sciam-1874, src-elecworld-1900, src-cbc-2017]
+      read: yes
+      confidence: moderate
     statement: >
       Woodward and Evans were not the first to patent an electric lamp with carbon in an enclosed globe (carbon in a vacuum was
       patented in Britain in 1845), and their patented lamp is a different design from the one Edison patented: a piece of carbon in a
@@ -1157,7 +1171,6 @@ claims:
   - id: lamp-latimer-invented-claim
     state: refuted
     refutes_target: "Lewis Latimer invented the light bulb or the carbon filament"
-    refutation_class: misattribution
     statement: >
       Latimer did not invent the light bulb or the carbon filament. His 1882 patent is a manufacturing
       improvement filed in 1881, after carbon filaments had been patented by Edison (applied for November 1879, granted 1880) and carbon in
@@ -1186,7 +1199,6 @@ claims:
   - id: lamp-10000-ways-quote
     state: refuted
     refutes_target: "Edison said 'I have not failed, I've just found 10,000 ways that won't work' about the light bulb"
-    refutation_class: narrative_drift
     statement: >
       The earliest version found is in Dyer and Martin's 1910 biography, where Walter Mallory recalls Edison saying "I know several
       thousand things that won't work" about the nickel-iron storage battery after "over nine thousand experiments", not about the lamp; Mallory
@@ -1229,7 +1241,6 @@ claims:
   - id: lamp-edison-sole-inventor
     state: refuted
     refutes_target: "Thomas Edison invented the light bulb (as its first or only inventor)"
-    refutation_class: narrative_drift
     statement: >
       Edison did not invent the incandescent lamp from nothing and was not its first or only inventor. British patents of 1841 (de Moleyns) and
       1845 (King, for Starr) already described, respectively, an electric light fed with powdered charcoal in an exhausted globe and a heated carbon conductor in a vacuum; Woodward
@@ -1261,7 +1272,7 @@ claims:
         - {node: lamp-1891-47f454-wallace-upholds-edison-lamp-patent, verb: qualifies}
     basis: >
       The true core is large and is kept in lamp-edison-patent, lamp-edison-high-resistance, lamp-edison-patent-upheld and
-      lamp-pearl-street. The drift is from "made a lamp the courts called practical, and a system to run it" to
+      lamp-pearl-street. The stretch is from "made a lamp the courts called practical, and a system to run it" to
       "invented it". Under the dig's standard (S2, S3) the refutation rests on dated documents (patents, a society report, a court
       opinion) that show earlier descriptions and an earlier reported experiment, not on any claim that a lamp was built before Edison's
       beyond Swan's reported rod. The first version also said lamps were "built" by Lodygin and by Woodward and Evans before Edison, and
diff --git a/build/subjects/incandescent-lamp/log.yaml b/build/subjects/incandescent-lamp/log.yaml
index 33f0715..e30920d 100644
--- a/build/subjects/incandescent-lamp/log.yaml
+++ b/build/subjects/incandescent-lamp/log.yaml
@@ -271,3 +271,7 @@ log:
       lamp-1874-07-11-lodygin-russian-privilege (rev 3) and the timeline note, both details come from one newspaper history (Kommersant 6822124) with no scan, and the same page says the Russian patent came "only a
       year" after the 1872 petition ("Российский патент ему удалось получить только через год", re-read), which does not fit a July 1874 grant, so the number and date are unverified; confidence for those details is low; the claim's state
       (proposed, low) is unchanged.
+  - id: L-25
+    date: 2026-10-02
+    entry: >
+      CORRECTION (refutation classes; earlier entries stay as written, including L-05). Under the refutation-class bars (docs/proposals/refutation-classes.md, if approved) the refutation_class on four claims is removed because the evidence of how the belief arose is not read: lamp-latimer-invented-claim (no dated instance of the false attribution is read), lamp-10000-ways-quote (only one read form in tx-10000-ways; the later forms are read: no), lamp-edison-sole-inventor (no chain and no instance read). No finding changes: state, confidence, weights and anchors are as before. lamp-lodygin-first-claim and lamp-canada-invented-claim keep narrative_drift and gain a refutation_origin block pointing to their chains; the last step of the Lodygin chain is reported by one 2022 newspaper history and was not read in a 1947-48 source. Prose corrected to match: the assessment no longer says "a Latimer misattribution" (it names the claim) and the Edison and basis wording says "stretch", not "drift". Needs an independent reviewer round or open item before it counts (review.yaml is not written by the author).
diff --git a/build/subjects/incandescent-lamp/threads.yaml b/build/subjects/incandescent-lamp/threads.yaml
index c6efe88..9f07ad8 100644
--- a/build/subjects/incandescent-lamp/threads.yaml
+++ b/build/subjects/incandescent-lamp/threads.yaml
@@ -26,7 +26,7 @@ threads:
       - {claim: "incandescent-lamp:lamp-goebel-claim", attestation: preserved}
     see_transmission: [tx-goebel-legend, tx-canada-sale, tx-lodygin-priority]
     overlay_notes:
-      - "United States: the true core is a lamp the courts called practical and the Pearl Street district service of 4 Sep 1882; the drift is to 'invented the bulb'. Sources: src-47f454, src-52f300, src-tribune-1882-09-05."
+      - "United States: the true core is a lamp the courts called practical and the Pearl Street district service of 4 Sep 1882; the stretch is to 'invented the bulb'. Sources: src-47f454, src-52f300, src-tribune-1882-09-05."
       - "Britain: the true core is Swan's Dec 1878 report of a glowing carbon rod, his own account of a lamp shown about two years before Oct 1880, and Swan lamps at the Savoy (28 Dec 1881) and, per a blog only, Cragside (1880); the dig records no popular story that has drifted from these and files none. Sources: src-chemnews-1879, src-chemnews-1880, src-iet-cragside, src-times-savoy."
       - "Canada: the true core is an 1874 Canadian patent and Woodward's 1876 US patent; the drift is a sale with no document and a design that differs from Edison's. Sources: src-sciam-1874, src-us181613, src-elecworld-1900."
       - "Germany: the true core is a real New York mechanic with a real 1882 lamp-socket patent; the 1854 lamps have no dated document from before 1882, and US courts weighed the testimony differently on preliminary motions. Sources: src-us266358, src-54f678, src-56f496, src-57f616."
diff --git a/build/subjects/teti-pyramid-texts/claims.yaml b/build/subjects/teti-pyramid-texts/claims.yaml
index e31aa94..18931a9 100644
--- a/build/subjects/teti-pyramid-texts/claims.yaml
+++ b/build/subjects/teti-pyramid-texts/claims.yaml
@@ -315,7 +315,6 @@ claims:
   next_step: Read the named works directly and record each scholar's position in their own words.
   refutes_target: >-
     PT 273–274 reflects actual prehistoric cannibalistic practices that were 'enshrined in religious literature' (Faulkner 1924).
-  refutation_class: motivated_error
   refutation_basis: >-
     No archaeological evidence of cannibalism in Fifth or Sixth Dynasty Egypt exists. Faulkner himself qualified the claim. The overwhelming
     scholarly consensus since Renouf (who flagged this immediately upon publication in the 1880s) is that literal cannibalism is not
diff --git a/build/subjects/teti-pyramid-texts/log.yaml b/build/subjects/teti-pyramid-texts/log.yaml
index 7c09d83..b334a94 100644
--- a/build/subjects/teti-pyramid-texts/log.yaml
+++ b/build/subjects/teti-pyramid-texts/log.yaml
@@ -32,3 +32,7 @@ log:
     date: 2026-10-02
     entry: >
       CHRONOLOGY CHECK (read in the PeriodO dataset, not in the authorities' own books). Six authorities define the Egyptian Old Kingdom differently: it starts between 2700 and 2600 BCE and ends between 2190 and 2130 BCE, so a spread of about 100 years at the start and 60 at the end. The imported files' statement that Teti's dates are uncertain by plus or minus 10 years as 'scholarly consensus' (claim teti-reign-conventional-dates) is therefore not supported for the period as a whole; it stays a convention taken from Shaw 2000, which was not read. A shared node (period-old-kingdom-egypt) now carries the six definitions as a time window and appears on this excavation's timeline.
+  - id: L-05
+    date: 2026-10-02
+    entry: >
+      CORRECTION (refutation classes). The refutation_class motivated_error on pt-273-274-cannibalism-interpretation is removed. Nothing read gives a motive for anyone: the anchor is "needs primary anchor" and Faulkner (1924) and Eyre (2002) were not read. The claim, its state, confidence and weight are unchanged. The class was also removed from the import file and the utterance copy, so regenerating from the import does not bring it back.
diff --git a/build/subjects/teti-pyramid-texts/utterances/pt_273_274.yaml b/build/subjects/teti-pyramid-texts/utterances/pt_273_274.yaml
index bd747be..2d5bb4c 100644
--- a/build/subjects/teti-pyramid-texts/utterances/pt_273_274.yaml
+++ b/build/subjects/teti-pyramid-texts/utterances/pt_273_274.yaml
@@ -290,7 +290,6 @@ divergence_points:
       PT 273–274 reflects actual prehistoric cannibalistic practices that were
       'enshrined in religious literature' (Faulkner 1924).
     state: refuted
-    refutation_class: motivated_error
     refutation_basis: >
       No archaeological evidence of cannibalism in Fifth or Sixth Dynasty Egypt exists.
       Faulkner himself qualified the claim. The overwhelming scholarly consensus
```

## 6. Alternatives considered

1. **Do nothing, and delete Rule 12's class mention.** Honest about what the repository has, and costs nothing. Rejected because six classes are already set and nothing guards them, so "do nothing" leaves four unevidenced classes; removing the mention would also require removing the field from six published claims and the generator, nearly the migration of 5.3. This is the consistent fallback if the owner declines.
2. **Origin block only, no new classes** (the five names, with the evidence fields). This is the lighter option and the validator is the same with five names (Owner choice 1). It leaves six claims, in four digs, with no honest class.
3. **A free-text `how_arose` field, no classes.** Honest and no taxonomy to defend, and it could state exactly what happened in the Tonkin case. Rejected as the main design because the validator can check none of it and the failure case (a motive imputed with nothing read) stays open, and readers cannot filter or compare. It survives as `refutation_origin.description`, required for any class.
4. **Optional classes with prose definitions only** (no origin block). The present state plus a definition page; it does not stop the teti case.
5. **A required class on every refuted claim.** Forces a guess on 13 of 17.
6. **Five classes only.** See 2.
7. **A ranked gradient** ("honest_error < drift < motive < propaganda < fabrication", as L-07 put it). Rejected: it invites reading a class as a verdict on people, and the bars are about evidence of origin.
8. **Freezing the six existing classes with a dated note.** Not possible with this patch: a class without its origin block raises RC1, so a frozen class fails the validator. It would need a grace mechanism in the validator, which this proposal does not add.

## 7. Neutrality check

Whether the bars are the same whichever way a claim points, and whether the intent classes can impute motive without anchored evidence.

### 7.1 Refuted claims pointing in different directions

| Direction of the false belief | Claim | What the bars require | Result |
|---|---|---|---|
| A government or official account | Tonkin: the second attack occurred (the 1964 US account) | `misreading`: a record and an instance of the false reading, both read. | Partial (instance read only secondarily). `institutional_propaganda` would need the government's own directive quoted showing a campaign; `tonkin-senior-knowledge` is contested at low; not met. |
| An anti-institutional belief | Surfside deliberate/timed claim, Apollo hoax | Same bars; `fabrication` needs a forgery finding; `motivated_error` the holder's words. | Row 9 partial; rows 1, 8, 10 not met. The same absence of anyone's words blocks a motive for the believers as it does for the government in Tonkin. |
| A popular myth that favours a person or country | Lodygin first (Soviet campaign), Canada sale, Latimer, 10000-ways | `narrative_drift` two read forms; `misattribution` a read instance. | Canada met; Lodygin partial; Latimer, 10000-ways not met. The Soviet-campaign reading of Lodygin fails `institutional_propaganda` exactly as a US-government reading of Tonkin does: one secondary source, no directive. |
| A popular myth against a person or institution | Henry Ford "shows autism", Simpsonwood "hidden", thimerosal "because harmful" | `misreading` / `narrative_drift`, same evidence types. | Henry Ford and Simpsonwood partial; thimerosal not met. The same standard that leaves the film and the article unread blocks a full class for each. |
| A scholarly interpretation | Faulkner 1924, Anatolian daughter hypothesis, measles RNA in the gut | `failed_hypothesis`: the hypothesis in a proponents' document read, and what answered it. | Not met in any of the three: the proponents' documents are not read. A scholar's error gets no `motivated_error` without the scholar's own words, as for everyone else. |

The bars are symmetric because they ask the same two things of every claim: a dated document read, and the actor's own words. In this sample they were met in full for one popular myth, in part for a government account, popular myths and a scholarly-adjacent source alike, and not at all for the scholarly cases. No direction was favoured. The proposal's test (3.7) makes this mechanical: the verdict is unchanged when the holder is a defence ministry, a tobacco company, a university department or a senator.

A systematic softness remains and is stated: the benign classes are cheaper than the intent classes. They now need two documents, named passages, a manifest read, and a moderate cap, but they can still be pinned on a government, a myth or a scholar with two real documents, and each carries an implication of "no intent". That is why `failed_hypothesis` is defined without a state of mind and why the page display waits for a reviewer's tick.

### 7.2 Can the intent classes impute motive without anchored evidence?

- `motivated_error` and `institutional_propaganda` need the holder or institution named, a holder kind that excludes private individuals, a quotation of 30 or more characters, the source it is in (one of the claim's origin sources), where in it, a stated link from the quoted aim to this claim, two sources, a manifest `read`, and a cap of moderate. The validator rejects each missing piece (tested; `quote: "x"` no longer passes). `review_dig.py` matches the quotation against stored sources.
- Words that state an aim but not one connected to the claim do not qualify (`link`). "Benefit, silence or 'who gains'" is stated as not qualifying.
- `fabrication` needs a decisive anachronism or two independent lines and two sources, as rule 4 already says. It does not require a named maker.
- Surface text is covered by the REVIEW.md line (3.5), not by the validator.
- What remains with the reviewer: that the quotation says what `link` says it does, and that the `holder_kind` is right. The validator cannot check either.
- Present state: the one intent class on `main` (teti) fails these checks and is removed in 5.3.

## 8. Owner choices

These are the assessor's recommendations, not decisions.

1. **Seven classes or five.** Recommended: seven (after the redefinition of `failed_hypothesis`). Fallback: `misreading` only; or the five names with the origin block.
2. **Optional or required.** Recommended: optional (3.3).
3. **Caps.** Recommended: the intent classes at moderate, and the other classes at moderate unless three distinct sources were read. `fabrication` stays at moderate; a decisive anachronism could be allowed high.
4. **Show the class on the page.** Recommended: not in this change. A separate proposal after the reviewer's tick exists.
5. **The six existing classes.** Recommended: remove four (Latimer, 10000-ways, Edison-sole, teti), keep two with origin blocks, with log entries and the prose fix; do not freeze (6.8).
6. **One class per claim or several.** Recommended: one class plus `see_also`.
7. **Reviewer tick.** Recommended: yes. The independent reviewer records a tick per class in `review.yaml` before any display and before any intent class on a published dig.
8. **Owner-only text edits.** Recommended: applied by the owner: Rule 12, REVIEW.md B (with the class-words line), `method/index.html` line 58, and `review_dig.py`.

## 9. What the independent assessor of this revision should check

- That the six classes in 1.2 rows 3-7 and 12 are on `main` (`grep refutation_class build/subjects/*/claims.yaml`) and that nothing is applied: `git status` shows only this file.
- That `git apply --check` accepts the SCHEMA diff and the diffs in 3.6 and 5.3 against `origin/main`, the validator gives 6 errors with the patch alone and 0 after the migration, and the tests pass.
- That every change the first assessment required is made (the revision note below).
- Known weak points: `read` and the quotation text are author-asserted; independence of two sources is not checked; the intercept reports and the four web sources were not opened by anyone; whether `misreading` and `failed_hypothesis` are the right split is a judgement; some classes have only two or three cases.

## 10. Process

Per docs/SCHEMA_PROPOSALS.md: this file on a `process/<topic>` branch and a pull request; an independent reviewer who did not write it checks the seven points and records the result on the pull request; the owner decides and the reason is logged on the pull request; only then is the change made, in its own commit, with the validator updated in the same change. This file is on branch `claude/jolly-hopper-ira8mk`; no pull request has been opened, and moving it to a `process/<topic>` branch and opening one is the step before the owner decides.

## Revision note (revision 2)

Changes made after the independent assessment:
1. The three benign classes now have required fields, two different documents with named passages, an error (not a warning) when the origin is wholly the refutation's own anchor, a manifest `read` check, and a moderate cap unless three sources were read (3.4, RC4-RC6).
2. The intent classes need `quote_source`, `locator`, `link`, `holder_kind` excluding private individuals, and a quote of at least 30 characters; `review_dig.py` is extended (as proposed text) to match quotations against stored sources.
3. The validator no longer crashes on non-string `sources`; tested.
4. `failed_hypothesis` no longer says "good faith"; `intent_searched` is added, and the class is limited to claims already refuted under Rule 9.
5. `see_also` is added; `misreading` covers shipboard and other records; Lodygin and Tonkin are moved to partial; the Lodygin chain's last step is stated as a 2022 secondary report; no Tonkin class is in the migration.
6. The migration is complete: log entries drafted, lamp prose corrected, the Teti import, utterance copy and generator covered, `method/index.html` added to the owner list, the diff fence closed, and what a class removal on a published dig needs is stated.
7. A REVIEW.md B line holds class words in surface text to the same bar (3.5).
8. The neutrality test varies what the validator reads; a firewall test checks that no code outside the validator reads the class.
9. The Goebel precedent (L-05, L-15) is added to the failure case.
10. Minor: `src-salon-2011` is `read: full`; rule A8 is in `build/SCHEMA.md`; the header no longer reads as a mandate; "origin block only, no new classes" and "freeze" are in the alternatives; the Rule 9 limit on `failed_hypothesis` (L-19) is stated.
