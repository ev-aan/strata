# Refutation classes: define the five, add two, and require the evidence

**Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.**

Author: an agent (Claude Sonnet 5.5), session https://claude.ai/code/session_01CHPX2Whoid8Mecyfqx5j6p. The owner decided on 2026-10-02 to "make refutation classes". This file proposes how, so that the decision rests on a proposal that meets the seven standards. Nothing in it is applied: no claim, `CONTRIBUTING.md`, `build/SCHEMA.md` or `build/conformance.py` is changed. Every number below was produced by running the code named in the text; the patch was applied only in a scratch worktree of `origin/main` (91f6218), which was removed afterwards.

## Summary

- CONTRIBUTING Rule 12 says each class "has its own evidential bar". No bar is written anywhere. `build/conformance.py` checks only that the name is one of five.
- The repository already contains six refuted claims with a class set (five in `incandescent-lamp`, one in `teti-pyramid-texts`) and none of them shows how the false belief arose, so a reader cannot tell what the class rests on. The validator passes all six. (The brief for this proposal said no refuted claim sets a class. That is true only of the vaccines-autism branch; on `main` six do.)
- Proposal: a class stays optional, but when set it must carry a separate `refutation_origin` block that shows, from documents read, how the false belief arose. Each class has a fixed evidence type and a minimum bar. The three classes that allege intent (`fabrication`, `motivated_error`, `institutional_propaganda`) are capped at moderate and need two sources and the holder's or institution's own words; benefit, silence or "who gains" never qualifies.
- Two classes are added, `misreading` and `failed_hypothesis`, because 6 of the 17 refuted claims in the repository (3 on `main`, 3 on `dig/vaccines-autism`; see section 3.2) fit none of the five and the author of that dig said so in its log (L-07). No class is added for which there is no refuted claim (`satire_taken_literally` is not added).
- Applying it: validator output on all 15 digs is 0 errors before; 6 errors after the validator patch alone (5 in `incandescent-lamp`, 1 in `teti-pyramid-texts`); 0 errors after a migration of those two digs. Of the 17 refuted claims, 3 can be given a class today on the evidence in the files (2 `narrative_drift`, 1 `misreading`), 3 more meet the bar only in part, 7 have a candidate class that needs one more document read, and 4 have no candidate. Of the six classes already set on `main`, 2 meet the bar and 4 do not.
- The class carries no weight. No existing finding changes.

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
- **Which question the reader is asking.** Take "a second North Vietnamese attack took place on 4 August 1964 is refuted". Was the belief a misreport, drift, or motivated error? The repository holds the answer in three other claims, not in a class: `tonkin-sigint-selectively-presented` (established, moderate: the intercepts reaching decision-makers were assembled selectively); `tonkin-midlevel-deliberate-skew` (proposed: individuals at NSA deliberately skewed it; Hanyok judges they themselves believed an attack had happened); `tonkin-senior-knowledge` (contested, low: whether senior officials knew). The refuted claim itself carries nothing. A reader of `tonkin-aug4-attack-occurred` cannot tell that the intercepts contained "severe analytic errors, unexplained translation changes, and the conjunction of two unrelated messages" (Hanyok, as quoted in the claim's text) without reading four claims. And none of the five existing classes fits that origin: it is a misreading of signals (see 3.2), not drift (no true core retold), not misattribution, not an established motive, not a campaign, not an invention.
- **Whether the five classes are all the classes there are.** The vaccines-autism log, L-07, says `va-measles-rna-gut` fits "none of the five ... a good-faith hypothesis that failed a test, which suggests the gradient needs an 'honest_error' or 'failed_hypothesis' class." A claim set cannot be classified honestly if the set is incomplete, and the log says no one has been able to say.

### 1.4 Why this is a failure and not a preference

Rule 12 and REVIEW.md B each tell a person to check a bar that is not written. The only two possible results are a class set on the author's say-so (six claims on `main`, four of which fail the bars proposed here) or a class left off (11 claims on `main` and the branch, and the authors say so). Either way the reader is told something incorrect or nothing, and for the intent classes the incorrect result is an accusation.

## 2. Evidence

What was opened and run.

- `CONTRIBUTING.md` Rules 9 and 12 and the claim states table; `docs/REVIEW.md` section B (the two bars); `docs/AUTHENTICITY.md` (section 6 rule 4: a forgery finding needs a decisive anachronism or two independent lines of evidence; rule 5: a genuineness finding needs provenance and a test that could fail); `docs/AGENT_RULES.md` section 11; `docs/COORDINATION.md` item 2; `build/SCHEMA.md` (claim fields, the open item, X1-X4, TH2); `build/conformance.py` (validation of `refutation_class` at lines 182-187, anchor format N25 at `check_anchor_format`, transmission rules in `check_links`).
- Every `build/subjects/*/claims.yaml` for `state: refuted` (table in 1.2) and the claims, log, manifest and threads of `origin/dig/vaccines-autism`. For the twelve claims on `main` the statement, anchor, basis and adoption note were read; for the five on the branch the same, plus the manifest `read` flags of the origin sources. The origin documents themselves (Hanyok, the patents, the transcripts) were NOT re-opened for this proposal. Where the table in section 5 says an origin is "read", it means the dig's own file says it was read; the assessor should spot-check.
- Baseline validator: `python3 build/conformance.py --base origin/main` on a clean worktree of `origin/main`: `15 subjects and 107 shared nodes checked: 0 errors, 93 warnings`.
- Patch tests in the scratch worktree: `python3 build/tools/test_refutation_classes.py`: `Ran 14 tests ... OK`.

## 3. The proposed change

### 3.1 Principle and firewall

The class describes **how the false claim arose** (its origin and first transmission). It is separate from, and never raises, lowers or replaces, the evidence that the claim is **false**. That evidence is the claim's `anchor` and Rule 9. The two questions are answered by two blocks:

| Question | Where | Governed by |
|---|---|---|
| Is the claim false? | `anchor`, `evidence_class`, `evidential_weight`, `confidence` | Rule 9, N25 |
| How did the false belief arise? | `refutation_class` + `refutation_origin` | Rule 12 (this proposal), RC1-RC8 |
| How did it spread afterwards? | `transmission.yaml` | X1-X4, `confers_weight: false` |

The class confers no weight: it is not an anchor, it cannot be cited as one, no validator check or page rule reads it to set a state, a weight, a headline or a publish status (RC8, tested). A refuted claim with no class is exactly as refuted as one with a class. This is the same firewall as CONTRIBUTING section 3 ("How a claim spread is recorded as transmission, not as support for the claim"). A class is a statement about the history of an error, and it too can be wrong, which is why it has its own confidence (RC4) separate from the claim's.

### 3.2 The set: are five right?

Test: assign each of the 17 refuted claims from the five. The result (details in section 5):

- `narrative_drift` fits rows 3 and 4 now and, once their drift is read, 6, 7 and 15; `misattribution` fits row 5 (Latimer) once an instance of the false attribution is read.
- Six claims fit none of the five, in two groups:
  - **A read document or data was taken to say what it does not**: Tonkin 4 August (intercepts misanalysed), Henry Ford (a draft whose tables show no association, said to show one), Simpsonwood (a transcript said to show the finding hidden). Three claims, across two digs, pointing at a government account, a popular film and a campaign story. Proposed class: **`misreading`**. It is not `narrative_drift` (there is no true core retold through steps, but one document read wrongly) and not `misattribution` (nothing is credited to the wrong person or source).
  - **A hypothesis or interpretation that was held in good faith and then failed a test, or was superseded**: `va-measles-rna-gut` (a mechanism proposed 1998-2002, then not replicated by three blinded laboratories including the original), `anatolian-daughter-hypothesis` (a scholarly hypothesis superseded), `pt-273-274-cannibalism-interpretation` (a 1924 scholarly interpretation). Three claims across three digs. Proposed class: **`failed_hypothesis`**. This is the class the vaccines dig's author asked for (L-07 calls it `honest_error` or `failed_hypothesis`). I chose the second name because it says what happened (a hypothesis was tested) without presuming a state of mind.
- `satire_taken_literally`: no refuted claim in the repository is satire, so it is not added. A class with no case would be invented from outside, and the bar for adding one is the same proposal path.
- Not classed, and no new class proposed: `va-wakefield-paper-account-accurate` (a statement in a paper that a court called "untrue"). The court did not find intent, and `fabrication` needs evidence of intent (below). A statement later held false that is neither a hypothesis, a misreading nor a drift would need a class of its own (for example `misstatement`), but with one case in the repository I do not propose it. It stays unclassed, which is a valid and honest state (3.3).
- Apollo, surfside, mcafee-owned-unit have no origin evidence in their digs; they stay unclassed.

So the set proposed is seven: the five and `misreading`, `failed_hypothesis`. Owner choice 1 below is to take the five only.

### 3.3 Required or optional

**Optional, and checked whenever present.** A class cannot honestly be required: 13 of the 17 refuted claims have no origin evidence in the repository and would need a class guessed, which is the failure case. A required class with an `unclassified` value is a class in name only. Optional costs one thing: a reader sees nothing where a class could be. The page should then show "Origin: not classified" (a site-builder change, outside this proposal; Owner choice 4). Optional also means the claim state, Rule 9 and every finding stay as they are.

### 3.4 Definitions, minimum bars, exclusions, anchor type, cap

Common to all seven: the class describes **how the false belief arose**, never whether it is false. The bar is about the origin and is **in addition to** Rule 9 (the claim must still be `refuted` on material or primary-text evidence). `refutation_origin.read: yes` is required: the origin documents were opened (RC3). `refutation_origin.confidence` rates the class, not the refutation (RC4). The "required anchor type" below is the `refutation_origin.type`; it is deliberately not the `anchor` type, because the `anchor` is the evidence for falsity.

| Class | Definition | Minimum bar (what must be shown about how it arose) | Does NOT qualify | `refutation_origin.type` and fields | Cap on origin confidence |
|---|---|---|---|---|---|
| `narrative_drift` | A true statement, or a real event, that changed in retelling until it said something the evidence does not support. | A transmission chain of this claim in `transmission.yaml` with at least two different forms of the claim among its **read** events, one of them the documented true core. | A claim that is merely popular. Forms known only from a secondary source (`read: no`). A chain that shows spread but no change of content. | `transmission-chain`, `chain: <id>` | high |
| `misattribution` | A real act, text or finding credited to the wrong person, group or source. | The true attribution shown by a dated document read, **and** one dated instance, read, where the credit goes to the claimed person or source. | Credit given for something that did not happen at all (that is fabrication or failed_hypothesis). A recognition that overshoots without an instance read. | `attribution-record` | high |
| `misreading` | A document or data set that exists was taken to say what it does not. | Both the document or data and an instance of the false reading, read, with the passages that differ named. | A claim about a document that does not exist. A reading that is a legitimate interpretation within the document's range. | `reading-comparison` | high |
| `failed_hypothesis` | A hypothesis or interpretation held in good faith, then not supported by a test or by later evidence. | The hypothesis stated in a document by its proponents, read; and the test or evidence that answered it. | Any case where the proponent is shown, by their own words, to have known otherwise (that is `motivated_error` or `fabrication`). Silence about their state of mind is not "good faith": the class asserts only that no evidence of intent was found, and says so. | `hypothesis-record` | high |
| `fabrication` | An item or statement made up and presented as real. | A forgery finding that meets docs/AUTHENTICITY.md rule 4: a decisive anachronism (`anachronism:`) or two independent lines of evidence (`independent_lines:`), and at least two distinct sources. | A document found unreliable, a mistaken or retracted one, or a hoax with no evidence the item was made rather than misread. A fact-checker's rating alone. Not knowing who made it does not bar the class: it says the item was made, and does not name a maker. | `forgery-finding` | moderate |
| `motivated_error` | An error that the holder's own words show was shaped by a stated interest, commitment or purpose. | The holder named, and their own words (`quote:`) naming the interest or purpose, read, plus a second source. | Interest, benefit, advocacy, profession, nationality, politics or silence, inferred by anyone, including us. "Who gains" is never enough. A holder who is a private individual (AGENT_RULES section 11). | `stated-motive`, `holder:`, `quote:` | moderate |
| `institutional_propaganda` | A claim an institution issued or directed as part of a campaign to promote it. | The institution named, its own dated directive or publication (`quote:`) read, showing the claim was issued by it as policy or campaign, plus a second source. | One institution's staff repeating a claim. A newspaper's account of a campaign that is the only source (the Kommersant case in lodygin). A government that was mistaken. | `institutional-campaign`, `institution:`, `quote:` | moderate |

Three notes on the table.

1. The two intent classes (`motivated_error`, `institutional_propaganda`) and `fabrication` carry more because they say something about people. They are the ones where a wrong class does harm, so they are capped at moderate and need the actor's own words. This is a design choice: Owner choice 3 asks whether the cap should be lower or the evidence higher.
2. A false belief with two origins (Tonkin: the 1964 reports misread the signals, and the presentation to decision-makers was then selective) gets one class, the one that describes how the belief arose. The second origin remains in its own claims, as it is today. Owner choice 6 asks whether a claim may carry two classes.
3. The class of a claim may be unclassified because the evidence of origin is not in the repository. That is not a gap in the claim.

### 3.5 Text for build/SCHEMA.md (not applied)

Checked with `git apply --check` against `origin/main`: applies cleanly.

```diff
diff --git a/build/SCHEMA.md b/build/SCHEMA.md
index 9b9339c..d53fa4c 100644
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
@@ -368,3 +367,18 @@ CORRECTION in the log entry (`build_site.py` picks entries by that word); if the
 finding, follow the gate's revision loop (new log entry, revision round, independent check,
 visible correction). The validator does not enforce this paragraph. Recording a retraction turns the validator red until the claims carry
 `flagged_sources` and `source_notices` (intended).
+
+
+---
+## Refutation classes (RC1-RC8)
+
+`refutation_class` says how a false belief arose. It says nothing about whether the claim is refuted: that is Rule 9 alone, decided by the `anchor`. A class never adds or removes weight and is never cited as evidence (RC8). How a myth spread goes in `transmission.yaml`; the class only points to it.
+
+- **RC1** A class is optional. If set, the claim is `refuted` and carries a `refutation_origin` mapping. `refutation_origin` without a class is an error.
+- **RC2** `refutation_origin.type` is fixed by the class (narrative_drift: transmission-chain; misattribution: attribution-record; misreading: reading-comparison; failed_hypothesis: hypothesis-record; fabrication: forgery-finding; motivated_error: stated-motive; institutional_propaganda: institutional-campaign) and `description` says how the belief arose.
+- **RC3** `read: yes`. A class is never set on origin evidence that was not opened. Without it, leave the class off.
+- **RC4** `confidence` rates the class, not the refutation. The three classes that allege intent (fabrication, motivated_error, institutional_propaganda) are capped at moderate.
+- **RC5** `sources` lists manifest ids. If they are all the refutation's own anchor, a warning asks the description to point to the passage that shows how it arose.
+- **RC6** The intent classes need two distinct sources. motivated_error needs `holder` and `quote` (their own words naming the motive). institutional_propaganda needs `institution` and `quote` (the institution's own dated document). fabrication needs `anachronism` or two `independent_lines` (docs/AUTHENTICITY.md rule 4). Benefit, silence or "who gains" never qualifies.
+- **RC7** `chain` (optional; required for narrative_drift) names a chain in this subject's `transmission.yaml` whose `about` is this claim. narrative_drift needs two different forms of the claim among its read events.
+- **RC8** No check reads the class to decide state, weight, headline or publish status. A class cannot be cited in `anchor` (TH2/X3 apply to chain ids).
```

CONTRIBUTING.md Rule 12 and docs/REVIEW.md B are owner-only files (CLAUDE.md, process step 5). The proposed text is below, not applied.

> **Rule 12.** `refutation_class` is optional and may only be set on a claim whose state is `refuted`. It says how the false belief arose and carries no weight on whether the claim is refuted. Each class (`narrative_drift`, `misattribution`, `misreading`, `failed_hypothesis`, `motivated_error`, `institutional_propaganda`, `fabrication`) has its own evidential bar, in `build/SCHEMA.md` (RC1-RC8). The class never rests on belief, spread or who would gain; the three classes that allege intent need the actor's own words.

> docs/REVIEW.md section B, replace the class line with: "Each `refutation_class` meets RC1-RC8. The validator cannot check that a `quote` is real or that a `description` is true: open it. A class that names a person or institution whose own words are not in the quoted source is a blocking finding. A class on a refutation whose origin is not read is removed, not downgraded."

### 3.6 The validator patch (not applied)

Diff of `build/conformance.py` as applied in the scratch worktree:

```diff
diff --git a/build/conformance.py b/build/conformance.py
index 8e0c5d7..ab182ec 100644
--- a/build/conformance.py
+++ b/build/conformance.py
@@ -29,8 +29,15 @@ SUBJECTS = os.path.join(ROOT, "build", "subjects")
 STATES = {"established", "proposed", "contested", "refuted", "searched_gap"}
 CLASSES = {"material", "primary_text", "interpretive", "synthetic"}
 CLASS_ALIASES = {"primary-text": "primary_text"}  # older corpus spelling
-REFUTATION_CLASSES = {"narrative_drift", "misattribution", "motivated_error",
-                      "institutional_propaganda", "fabrication"}
+REFUTATION_CLASSES = {"narrative_drift", "misattribution", "misreading", "failed_hypothesis",
+                      "motivated_error", "institutional_propaganda", "fabrication"}
+# Rule 12 (SCHEMA RC1-RC8): the class says how the false belief arose. Its evidence is a separate
+# `refutation_origin` mapping and never part of the refutation's `anchor`.
+ORIGIN_TYPES = {"narrative_drift": "transmission-chain", "misattribution": "attribution-record",
+                "misreading": "reading-comparison", "failed_hypothesis": "hypothesis-record",
+                "fabrication": "forgery-finding", "motivated_error": "stated-motive",
+                "institutional_propaganda": "institutional-campaign"}
+INTENT_CLASSES = {"fabrication", "motivated_error", "institutional_propaganda"}
 CONFIDENCE = {"high", "moderate", "low", "provisional"}
 # YAML reads a bare `no` as False; both mean "not checked".
 ANCHOR_CHECKED = {"no", "secondary", "primary"}
@@ -93,6 +100,67 @@ def check_anchor_format(r, subject, c, sdir):
                     r.err(where, f"anchor source `{s}` is not in sources/MANIFEST.yaml (SCHEMA N25)")
 
 
+def check_refutation_origin(r, subject, sdir, c):
+    """RC1-RC8 (SCHEMA.md, Refutation classes). A class is optional; when set it must show, in
+    `refutation_origin`, how the false belief arose. Nothing here changes whether a claim is refuted."""
+    rc = c.get("refutation_class")
+    if rc not in REFUTATION_CLASSES or c.get("state") != "refuted":
+        return                                       # name and state errors are raised in check_claim
+    where = f"{subject}:{c.get('id')}"
+    ro = c.get("refutation_origin")
+    if not isinstance(ro, dict):
+        r.err(where, f"RC1: refutation_class `{rc}` needs a `refutation_origin` mapping")
+        return
+    if ro.get("type") != ORIGIN_TYPES[rc]:
+        r.err(where, f"RC2: `{rc}` needs refutation_origin.type `{ORIGIN_TYPES[rc]}`, got `{ro.get('type')}`")
+    if not str(ro.get("description") or "").strip():
+        r.err(where, "RC2: refutation_origin needs a `description` of how the false belief arose")
+    if ro.get("read") not in (True, "yes"):
+        r.err(where, "RC3: refutation_origin.read must be `yes`: a class is not set on origin evidence that was not read")
+    if ro.get("confidence") not in CONFIDENCE:
+        r.err(where, "RC4: refutation_origin.confidence must be high | moderate | low | provisional (it rates the class, not the refutation)")
+    elif rc in INTENT_CLASSES and ro.get("confidence") == "high":
+        r.err(where, f"RC4: `{rc}` alleges intent; its origin confidence is capped at moderate")
+    ids = {s.get("id") for s in load_sources(sdir).values()} if sdir else set()
+    srcs = ro.get("sources")
+    if not isinstance(srcs, list) or not srcs:
+        r.err(where, "RC5: refutation_origin needs `sources`, a non-empty list of manifest ids")
+        srcs = []
+    for s_ in srcs:
+        if s_ not in ids:
+            r.err(where, f"RC5: refutation_origin source `{s_}` is not in sources/MANIFEST.yaml")
+    anchor_srcs = set((c.get("anchor") or {}).get("sources") or [])
+    if srcs and set(srcs) <= anchor_srcs:
+        r.warn(where, "RC5: the origin evidence is only the refutation's own anchor; the description must "
+                      "point to the passage that shows how the belief arose, not why it is false")
+    if rc in INTENT_CLASSES and len(set(srcs)) < 2:
+        r.err(where, f"RC6: `{rc}` needs at least two distinct sources for the origin")
+    need = {"motivated_error": ("holder", "quote"), "institutional_propaganda": ("institution", "quote")}.get(rc, ())
+    for k_ in need:
+        if not str(ro.get(k_) or "").strip():
+            r.err(where, f"RC6: `{rc}` needs `{k_}` (who, and their own words as read; interest or benefit alone does not qualify)")
+    if rc == "fabrication" and not (str(ro.get("anachronism") or "").strip()
+                                    or (isinstance(ro.get("independent_lines"), list) and len(ro["independent_lines"]) >= 2)):
+        r.err(where, "RC6: `fabrication` needs an `anachronism`, or two `independent_lines` (docs/AUTHENTICITY.md rule 4)")
+    chain_id = ro.get("chain")
+    if rc == "narrative_drift" and not chain_id:
+        r.err(where, "RC7: `narrative_drift` needs `chain`, a transmission chain of this claim with dated steps read")
+    if chain_id:
+        xpath = os.path.join(sdir, "transmission.yaml")
+        chains = {ch.get("id"): ch for ch in ((load(xpath) or {}).get("chains") or []) if isinstance(ch, dict)} \
+            if os.path.exists(xpath) else {}
+        ch = chains.get(chain_id)
+        if ch is None:
+            r.err(where, f"RC7: chain `{chain_id}` is not in this subject's transmission.yaml")
+        elif ch.get("about") != f"{subject}:{c.get('id')}":
+            r.err(where, f"RC7: chain `{chain_id}` is about `{ch.get('about')}`, not this claim")
+        elif rc == "narrative_drift":
+            read_forms = {str(e.get("form")) for e in ch.get("events") or []
+                          if isinstance(e, dict) and e.get("read") in (True, "yes")}
+            if len(read_forms) < 2:
+                r.err(where, "RC7: `narrative_drift` needs at least two different forms of the claim, from read events of the chain")
+
+
 def check_claim(r, subject, c, legacy):
     cid = c.get("id", "<no id>")
     where = f"{subject}:{cid}"
@@ -178,13 +246,15 @@ def check_claim(r, subject, c, legacy):
             r.err(where, "Rule 9: refuted claim must name `refutes_target`")
         if ec not in ("material", "primary_text"):
             r.err(where, f"Rule 9: refutation must rest on material or primary_text, not `{ec}`")
-    # Rule 12
+    # Rule 12 (state and name; the evidence for the class is checked by check_refutation_origin)
     rc = c.get("refutation_class")
     if rc is not None:
         if state != "refuted":
             r.err(where, "Rule 12: refutation_class is only allowed on refuted claims")
         if rc not in REFUTATION_CLASSES:
             r.err(where, f"unknown refutation_class `{rc}`")
+    elif c.get("refutation_origin") is not None:
+        r.err(where, "RC1: `refutation_origin` without a `refutation_class`")
 
     if state == "searched_gap" and not c.get("next_step"):
         if c.get("gap_type") == "structural":
@@ -370,6 +440,7 @@ def check_subject(r, sdir):
             ids[cid] = c
             check_claim(r, subject, c, legacy)
             check_anchor_format(r, subject, c, sdir)
+            check_refutation_origin(r, subject, sdir, c)
 
         check_publication(r, subject, sdir, claims, d)
 
```

What the validator can and cannot check. It checks: the class and state, the type fixed by the class, `read: yes`, confidence and its cap, that every source is in the subject's manifest, that the intent classes have two sources and the quote or finding, and that the chain exists, is about this claim and has two read forms. It cannot check that a quote is real, that `read: yes` is true, or that a description is accurate: those stay with the independent reviewer, as `anchor_checked: primary` does today. `read` is asserted by the author, like `anchor_checked`. A refuted claim whose `anchor` lists only `nodes` (Tonkin) makes the RC5 warning impossible to trigger; that is a known limit.

### 3.7 Unit tests

New file `build/tools/test_refutation_classes.py` (14 tests, passing in the scratch worktree: `Ran 14 tests in 0.04s OK`). It uses synthetic subjects, so it touches no dig. It covers: no class valid; unknown class; class on non-refuted; origin without a class; class without origin; each class valid with its evidence; wrong type; origin not read; unresolved sources; each intent class fails with one source and with confidence high; motive without a quote or without a holder; drift with one form, wrong chain, no chain; the firewall (the Rule 9 error is the same with and without a class); and the neutrality test (the same origin evidence gives the same verdict for a claim against a government, a popular myth and a scholarly view).

```python
#!/usr/bin/env python3
"""Tests for refutation classes (rules RC1-RC8 in build/conformance.py).

    python3 build/tools/test_refutation_classes.py

Synthetic subjects only. Includes the firewall test (the class never changes whether a claim is refuted)
and the neutrality test (the same origin evidence gives the same result whichever way the claim points)."""
import copy, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import yaml
import conformance as cf

SOURCES = [{"id": i} for i in ("src-a", "src-o1", "src-o2")]


def chain(about="s:c1", forms=("true core", "stretched")):
    ev = [{"id": f"e{i}", "date": f"19{i}0-01-01", "step": "origin", "form": f, "source": "src-o1", "read": "yes"}
          for i, f in enumerate(forms)]
    return {"chains": [{"id": "tx-1", "about": about, "confers_weight": False, "events": ev}]}


def subject(claim, tx=None):
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "sources"))
    yaml.safe_dump({"sources": SOURCES}, open(os.path.join(d, "sources", "MANIFEST.yaml"), "w"))
    if tx:
        yaml.safe_dump(tx, open(os.path.join(d, "transmission.yaml"), "w"))
    return d, claim


def refuted(cls=None, origin=None, state="refuted", ec="primary_text"):
    c = {"id": "c1", "state": state, "evidence_class": ec, "refutes_target": "t", "confidence": "high",
         "anchor": {"type": "primary_text", "description": "d", "sources": ["src-a"]}}
    if cls:
        c["refutation_class"] = cls
    if origin is not None:
        c["refutation_origin"] = origin
    return c


def run(claim, tx=None):
    d, c = subject(claim, tx)
    r = cf.Report()
    cf.check_claim(r, "s", c, False)
    cf.check_refutation_origin(r, "s", d, c)
    return r


def org(typ, **kw):
    o = {"type": typ, "description": "how it arose", "sources": ["src-o1"], "read": "yes", "confidence": "moderate"}
    o.update(kw)
    return o


def rc_errors(r):
    return [e for e in r.errors if "RC" in e or "Rule 12" in e or "refutation_class" in e]


class Classes(unittest.TestCase):
    def test_no_class_is_valid(self):
        self.assertEqual(rc_errors(run(refuted())), [])

    def test_unknown_class(self):
        self.assertTrue(any("unknown refutation_class" in e for e in run(refuted("satire_taken_literally", org("x"))).errors))

    def test_class_on_non_refuted(self):
        r = run(refuted("misreading", org("reading-comparison"), state="proposed", ec="interpretive"))
        self.assertTrue(any("only allowed on refuted" in e for e in r.errors))

    def test_origin_without_class(self):
        self.assertTrue(any("RC1" in e for e in run(refuted(origin=org("reading-comparison"))).errors))

    def test_class_without_origin(self):
        self.assertTrue(any("RC1" in e for e in run(refuted("misreading")).errors))

    def test_each_class_valid_with_evidence(self):
        good = {
            "misreading": org("reading-comparison"), "misattribution": org("attribution-record"),
            "failed_hypothesis": org("hypothesis-record"),
            "fabrication": org("forgery-finding", sources=["src-o1", "src-o2"], independent_lines=["a", "b"]),
            "motivated_error": org("stated-motive", sources=["src-o1", "src-o2"], holder="H", quote="in their words"),
            "institutional_propaganda": org("institutional-campaign", sources=["src-o1", "src-o2"], institution="I", quote="the directive"),
        }
        for cls, o in good.items():
            self.assertEqual(rc_errors(run(refuted(cls, o))), [], cls)
        self.assertEqual(rc_errors(run(refuted("narrative_drift", org("transmission-chain", chain="tx-1")), chain())), [])

    def test_wrong_type(self):
        self.assertTrue(any("RC2" in e for e in run(refuted("misreading", org("forgery-finding"))).errors))

    def test_origin_not_read(self):
        self.assertTrue(any("RC3" in e for e in run(refuted("misreading", org("reading-comparison", read="no"))).errors))

    def test_unresolved_and_anchor_only_sources(self):
        self.assertTrue(any("RC5" in e for e in run(refuted("misreading", org("reading-comparison", sources=["src-zzz"]))).errors))
        r = run(refuted("misreading", org("reading-comparison", sources=["src-a"])))
        self.assertEqual(rc_errors(r), [])
        self.assertTrue(any("only the refutation's own anchor" in w for w in r.warnings))

    def test_intent_classes_need_more(self):
        for cls, typ, extra in (("motivated_error", "stated-motive", {"holder": "H", "quote": "q"}),
                                ("institutional_propaganda", "institutional-campaign", {"institution": "I", "quote": "q"}),
                                ("fabrication", "forgery-finding", {"anachronism": "ink from 1954"})):
            one_source = run(refuted(cls, org(typ, **extra)))
            self.assertTrue(any("RC6" in e and "two distinct" in e for e in one_source.errors), cls)
            high = run(refuted(cls, org(typ, sources=["src-o1", "src-o2"], confidence="high", **extra)))
            self.assertTrue(any("capped at moderate" in e for e in high.errors), cls)

    def test_motive_needs_a_quote_not_benefit(self):
        r = run(refuted("motivated_error", org("stated-motive", sources=["src-o1", "src-o2"], holder="H")))
        self.assertTrue(any("quote" in e for e in r.errors))
        r = run(refuted("motivated_error", org("stated-motive", sources=["src-o1", "src-o2"], quote="q")))
        self.assertTrue(any("holder" in e for e in r.errors))

    def test_drift_needs_two_read_forms_and_matching_chain(self):
        o = org("transmission-chain", chain="tx-1")
        self.assertTrue(any("two different forms" in e for e in run(refuted("narrative_drift", o), chain(forms=("one",))).errors))
        self.assertTrue(any("not this claim" in e for e in run(refuted("narrative_drift", o), chain(about="s:other")).errors))
        self.assertTrue(any("RC7" in e for e in run(refuted("narrative_drift", org("transmission-chain"))).errors))

    def test_firewall_class_never_changes_rule_9(self):
        base = run(refuted(ec="interpretive")).errors
        classed = run(refuted("misreading", org("reading-comparison"), ec="interpretive")).errors
        self.assertTrue(any("Rule 9" in e for e in base))
        self.assertEqual([e for e in classed if "Rule 9" in e], [e for e in base if "Rule 9" in e])

    def test_neutrality_same_evidence_same_result(self):
        """A claim against a government, a popular myth and a scholarly view get the same verdict from the same origin evidence."""
        for target in ("A government statement", "A popular myth", "A scholarly interpretation"):
            c = refuted("misreading", org("reading-comparison"))
            c["refutes_target"] = target
            self.assertEqual(rc_errors(run(c)), [], target)
            bad = copy.deepcopy(c)
            bad["refutation_origin"]["read"] = "no"
            self.assertEqual(len(rc_errors(run(bad))), 1, target)


if __name__ == "__main__":
    unittest.main()
```

## 4. What it does not change

- **No state changes.** Rule 9 is untouched: a refutation still needs a named target and material or primary-text evidence. The check at `conformance.py` lines 177-181 is not edited. A claim without a class is refuted exactly as now.
- **No weight changes.** `evidential_weight`, `adoption_weight`, `confidence`, `anchor_checked`, headline eligibility and the publish gate never read the class (RC8; the firewall test). The class cannot be cited in `anchor`.
- **No finding changes.** What every claim says and its state, weight and anchor are as now. In the migration (section 5) the only edits to existing claims are to the `refutation_class` field and its new `refutation_origin` block: one class added with evidence (Tonkin), two kept with an origin block added (rows 3, 4), four removed (rows 5, 6, 7, 12). A class that is removed is a metadata correction, not a change of finding, but because it changes a published claim it needs a logged review entry in that dig (CLAUDE.md: logs are append-only, corrections are new entries).
- **No change to `transmission.yaml`** or to X1-X4, TH1-TH4. A chain is only pointed to.
- **No change to anchor format** (N25: one `anchor` mapping). `refutation_origin` is not an anchor.
- It does not decide any open question in a dig (for example the Rule 9 statistics question in vaccines-autism L-05).

## 5. Impact

### 5.1 Validator output on all 15 digs

Scratch worktree `git worktree add --detach <scratchpad>/rc origin/main`; command `python3 build/conformance.py --base origin/main`. Three runs: (a) before, (b) the validator patch only, (c) patch plus migration (section 5.3). Totals: (a) `0 errors, 93 warnings`; (b) `6 errors, 93 warnings`; (c) `0 errors, 93 warnings` (the warnings are identical, line for line).

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
| gulf-of-tonkin | 0E / 2W | 0E / 2W | 0E / 2W (adds a class, see 5.3) |
| incandescent-lamp | 0E / 3W | **5E** / 3W | 0E / 3W |
| mcafee-and-surfside | 0E / 3W | 0E / 3W | 0E / 3W |
| proto-indo-european | 0E / 42W | 0E / 42W | 0E / 42W |
| teti-pyramid-texts | 0E / 23W | **1E** / 23W | 0E / 23W |
| votes-2009-present | 0E / 0W | 0E / 0W | 0E / 0W |
| votes-johnson-tonkin | 0E / 0W | 0E / 0W | 0E / 0W |

The six errors in (b):

```
ERROR incandescent-lamp:lamp-lodygin-first-claim: RC1: refutation_class `narrative_drift` needs a `refutation_origin` mapping
ERROR incandescent-lamp:lamp-canada-invented-claim: RC1: refutation_class `narrative_drift` needs a `refutation_origin` mapping
ERROR incandescent-lamp:lamp-latimer-invented-claim: RC1: refutation_class `misattribution` needs a `refutation_origin` mapping
ERROR incandescent-lamp:lamp-10000-ways-quote: RC1: refutation_class `narrative_drift` needs a `refutation_origin` mapping
ERROR incandescent-lamp:lamp-edison-sole-inventor: RC1: refutation_class `narrative_drift` needs a `refutation_origin` mapping
ERROR teti-pyramid-texts:pt-273-274-cannibalism-interpretation: RC1: refutation_class `motivated_error` needs a `refutation_origin` mapping
```

A sixteenth subject, `vaccines-autism` on `origin/dig/vaccines-autism` (not on `main`): 0 errors, 104 warnings before; with the patch the same 0 errors in that dig (it sets no class), and the only 6 errors are the six above, which that branch inherits from `main`.

### 5.2 Proposed class for each existing refuted claim, with evidence

"Read" below means the dig's own file says the origin document was read. Not independently re-opened here. A class is proposed only where the bar of 3.4 is met by what the files say; otherwise "cannot be assigned" and the reason. Origin confidence is what the evidence would support, at most the cap.

| # | Claim | Class proposed | Evidence in the repository for how the belief arose | Bar met? |
|---|---|---|---|---|
| 1 | apollo-landings : apollo-staged-hoax | **Cannot be assigned: evidence of origin not read.** | The dig records poll shares (6% in 1999, about 11-12% later; a Newsweek item about Russia, "not read; unchecked") and no document on where the hoax belief arose. No `transmission.yaml`. | No. |
| 2 | gulf-of-tonkin : tonkin-aug4-attack-occurred | `misreading` (not possible with the five). Origin confidence moderate. | Hanyok, NSA study, read: the handful of intercepts supporting an attack "contained severe analytic errors, unexplained translation changes, and the conjunction of two unrelated messages"; intercept reports 7, 12, 13 read (Report 13 mentions aircraft, not ships). | Yes, on the files. Not `motivated_error`: `tonkin-midlevel-deliberate-skew` is only proposed and Hanyok judges the presenters believed an attack had happened; `tonkin-senior-knowledge` is contested at low. Not `institutional_propaganda`: no directive quoted. The selective presentation stays in its own claims. |
| 3 | incandescent-lamp : lamp-lodygin-first-claim | `narrative_drift` (keep). Moderate. | `tx-lodygin-priority`: 1874 Lodygin first to put carbon in a sealed vessel (Fontaine 1878, read, who also calls the apparatus impractical); 1927 Howell and Schroeder; 1947-48 "made the lamp before Edison, who only improved it" (Kommersant, read). Four events, all `read: yes`, four different forms. | Yes. Not `institutional_propaganda`, and the claim's own `basis` already says so: one newspaper history, not anchored. |
| 4 | incandescent-lamp : lamp-canada-invented-claim | `narrative_drift` (keep). Moderate. | `tx-canada-sale`: 1874 Scientific American "a patent for an electric light" (true core); 1900 Electrical World "purchased by Mr. Edison"; 2017 CBC "behind Edison's breakthrough". All `read: yes`. | Yes. |
| 5 | incandescent-lamp : lamp-latimer-invented-claim | **Cannot be assigned: no dated instance of the false attribution is read.** Candidate: `misattribution`. | The patents show his real work (read). The adoption note says it "grows out of real neglect of Latimer's work" with no source. No `transmission.yaml` chain for this claim. | No (first half of the bar only). Remove the class until an instance is read. |
| 6 | incandescent-lamp : lamp-10000-ways-quote | **Cannot be assigned: the drift is not read.** Candidate: `narrative_drift`. | `tx-10000-ways`: one read event (Dyer and Martin 1910, the true core, about a storage battery); the 1946 and 1982 forms and the 1921 and 1882 items are `read: no`, from Quote Investigator (secondary). The claim is already `provisional` for this reason. | No: one read form. Remove the class; re-add when the later forms are read. |
| 7 | incandescent-lamp : lamp-edison-sole-inventor | **Cannot be assigned: no chain and no instance read.** Candidate: `narrative_drift`. | The claim's `basis` argues the drift ("from 'made a lamp the courts called practical, and a system to run it' to 'invented it'"), and the adoption note cites schoolbooks and "the quote myth" with no source. | No. Remove the class. |
| 8 | mcafee-and-surfside : surfside-deliberate-timed-to-mcafee | **Cannot be assigned: evidence of origin not read.** | The theory rests on the claimed tweet (row 9) and the claimed unit (row 10), both refuted; nobody who originated the theory is identified in the files. Spread: "Instagram, Twitter, Reddit and blogs" (USA Today, secondary). `motivated_error` and `institutional_propaganda` are excluded: no one's words are read. | No. |
| 9 | mcafee-and-surfside : mcafee-june8-tweet-posted | **`fabrication` is the candidate; assignable only at low, and I would not set it yet.** | Four independent fact-checkers (PolitiFact, Snopes, USA Today, Check Your Fact) found no such post on the account's record; USA Today notes a genuine 8 June tweet has the same timestamp as the screenshot ("could have been the template for a digitally fabricated tweet"); the screenshot gives "88th Street" where the address was 8777 Collins Avenue. Recorded forged, strength moderate, in `sources/MANIFEST.yaml`. That is two lines of evidence (absence on the record plus template match), as AUTHENTICITY rule 4 requires. | Partly. Rule 4 is met in form, but the fact-checks are read and the item itself is not (AUTHENTICITY A8 asks for an independent capture, "not yet read by us"). The claim is `anchor_checked: secondary`. Owner or assessor to decide whether secondary reading of fact-checks suffices. |
| 10 | mcafee-and-surfside : mcafee-owned-unit | **Cannot be assigned: evidence of origin not read.** | The ownership belief comes from the same screenshot; no source in the dig shows how it arose separately. | No. |
| 11 | proto-indo-european : anatolian-daughter-hypothesis | **Cannot be assigned: evidence of origin not read.** Candidate: `failed_hypothesis`. | Legacy subject. The claim says the hypothesis was a scholarly one and records the later sister view as proposed. No document stating the hypothesis is read, no manifest. | No. |
| 12 | teti-pyramid-texts : pt-273-274-cannibalism-interpretation | **Cannot be assigned: evidence of origin not read.** Candidate: `failed_hypothesis`. Remove the present `motivated_error`. | Faulkner (1924) and Eyre 2002 are "named in the source file, not read here" (the anchor says so). Nothing read gives a motive. | No. Present class fails RC1/RC6 (no origin, no quote, no holder). |
| 13 | vaccines-autism : va-wakefield-paper-account-accurate | **Cannot be assigned: evidence of origin not read.** Not `fabrication` yet. | The court (Mitting J, read in full) says the ethics statement "was untrue and should not have been included"; it makes no finding of intent on it. The GMC findings are "not reachable"; Deer (2011) and Godlee (2011) are read via a tool summary only. L-07 proposes `fabrication (pending the GMC documents)`: under the bar that is exactly what would be needed (a forgery finding, two lines, two sources, deliberate invention shown). | No. |
| 14 | vaccines-autism : va-measles-rna-gut | **Cannot be assigned yet.** Candidate: `failed_hypothesis`. | The refutation is read in full (Hornig 2008). The original reports (1998-2002) stating the mechanism are read only "as cited in the paper"; the manifest lists Wakefield 1998 as abstract only. | Not until a proponents' document is read; then yes. |
| 15 | vaccines-autism : va-thimerosal-removed-because-harmful | **Cannot be assigned: no dated instance of the stretched form is read.** Candidate: `narrative_drift` (L-07's proposal). | The true core is read (MMWR 1999: removal "as soon as possible" because "any potential risk is of concern", with "no data or evidence of any harm"). Instances of "removed because harmful" are not cited in the claim ("Adoption: Not measured"). | No (first half only). |
| 16 | vaccines-autism : va-henry-ford-shows-autism | `misreading` (not `misattribution` as L-07 proposed). Near-candidate: needs one passage read. | The document is read in full (Tables 2 and 3: IRR 1.16 (0.16 to 8.62); HR 0.62 (0.10 to 3.69); the authors write no significant association). Instances of the claim: the Siri written testimony (read via tool) and the film "An Inconvenient Study" (cited, not in the manifest). | Almost. The author must quote the passage in the testimony that says it shows an association. Nothing is credited to a wrong person, so `misattribution` does not fit. |
| 17 | vaccines-autism : va-simpsonwood-autism-hidden | `misreading` (L-07 proposed `narrative_drift`). Candidate; needs an instance of the false reading read. | The transcript is read in full (autism passage p. 44: "slight, but not significant, increase"; the embargo request is for confidentiality ahead of a public release). The instance, the 2005 "Deadly Immunity" article, is known through its retraction (read, `src-salon-2011` via tool) and not read itself. | Not until the article, or the correction's description of it, is quoted. |

Count of the 17: assignable on the files today, 3 (rows 2, 3, 4); bar met only in part, 3 (rows 9, 16, 17); a candidate class that needs one more document read, 7 (rows 5, 6, 7, 11, 12, 14, 15); no candidate, origin not read, 4 (rows 1, 8, 10, 13).

### 5.3 Migration (what applying it would take)

Applied in the scratch worktree and validated (0 errors, warnings unchanged). Each edit to a published claim needs a logged review in that dig (CLAUDE.md gate).

- `incandescent-lamp`: add `refutation_origin` to rows 3 and 4 (`tx-lodygin-priority`, `tx-canada-sale`); remove the class from rows 5, 6, 7 until their origin is read. One log entry per dig edited (incandescent-lamp, teti-pyramid-texts, gulf-of-tonkin).
- `teti-pyramid-texts`: remove `motivated_error` from row 12. One log entry.
- `gulf-of-tonkin`: add `refutation_class: misreading` and its `refutation_origin` to row 2, only if the owner takes `misreading` (Owner choice 1).
- `vaccines-autism` (branch, not yet on `main`): L-07 says "Proposed when they are: ..." Rows 13-17 stay unclassed until the author reads the missing documents.
- Nothing else. 12 of the 15 digs have no change.

Edits as made in the scratch worktree (for the assessor; not applied):

```diff
diff --git a/build/subjects/gulf-of-tonkin/claims.yaml b/build/subjects/gulf-of-tonkin/claims.yaml
index 21ac074..cb8e9e7 100644
--- a/build/subjects/gulf-of-tonkin/claims.yaml
+++ b/build/subjects/gulf-of-tonkin/claims.yaml
@@ -247,6 +247,13 @@ claims:
     would_change_if: >
       new intercepts, ship logs or North Vietnamese records showing boats present and firing on 4 August, or recovery of the missing original Vietnamese text showing it concerned 4 August
     refutes_target: "A second North Vietnamese attack took place on 4 August 1964"
+    refutation_class: misreading
+    refutation_origin:
+      type: reading-comparison
+      description: "Hanyok [read]: the handful of intercepts that supported an attack on 4 August contained severe analytic errors, unexplained translation changes and the conjunction of two unrelated messages."
+      sources: [src-hanyok-2001, src-intercepts-1964]
+      read: yes
+      confidence: moderate
     anchor:
       nodes:
         - {node: tonkin-1964-08-04-second-attack-reported-then-refuted, verb: disputes}
diff --git a/build/subjects/incandescent-lamp/claims.yaml b/build/subjects/incandescent-lamp/claims.yaml
index a68dd44..646e5d6 100644
--- a/build/subjects/incandescent-lamp/claims.yaml
+++ b/build/subjects/incandescent-lamp/claims.yaml
@@ -343,6 +343,13 @@ claims:
     state: refuted
     refutes_target: "Lodygin was the first inventor of the incandescent lamp (the first to describe or patent it)"
     refutation_class: narrative_drift
+    refutation_origin:
+      type: transmission-chain
+      chain: tx-lodygin-priority
+      description: "Lodygin was reported in 1874 as first to put carbon in a sealed oxygen-free vessel (Fontaine, 1878, who also called the apparatus impractical); by the 1947-48 press push the lamp was said to be his, with Edison only improving it."
+      sources: [src-fontaine-1878, src-kommersant-campaign]
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
+      description: "A 1874 notice of a patent for an electric light (Scientific American) becomes, in 1900, a patent Edison purchased (Electrical World), and in 2017 the breakthrough behind Edison (CBC)."
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
     scholarly consensus since Renouf (who flagged this immediately upon publication in the 1880s) is that literal cannibalism is not```

## 6. Alternatives considered

1. **Do nothing, and delete Rule 12's class mention.** Keeps the repository honest about what it has, and costs nothing. Rejected as the owner's decision stands (2026-10-02) and for one more reason: six classes are already set and nothing guards them, so "do nothing" does not leave a clean state; deleting the class field would also have to remove it from six published claims, which discards the one honest use (lodygin, where the author applied the bar by hand). If the owner declines to proceed, deleting the mention of "its own evidential bar" from Rule 12 and removing the six values is the consistent fallback, and the migration in 5.3 is nearly the same size.
2. **A free-text `how_arose` field, no classes.** Honest, no taxonomy to defend, and it would let the Tonkin case say exactly what happened. Rejected as the main design because (a) it cannot be checked by the validator at all, so the failure case (a motive imputed with nothing read) is left standing, and (b) readers cannot filter or compare. It remains a good field to have: the `refutation_origin.description` is exactly this, required for any class, so the proposal includes it as the free-text part. Keeping a class optional means free text alone remains possible only in the claim's `basis`.
3. **Optional classes, no `refutation_origin` block** (names defined in prose only). That is the present state plus a definition page; it does not stop the teti case. Rejected for that reason.
4. **Required class on every refuted claim.** Forces a guess on 13 of 17. Rejected (3.3).
5. **Five classes only.** Leaves six claims, in four digs, with no honest class. The vaccines author asked for another class. Offered as Owner choice 1: the validator patch is the same with five names.
6. **A fixed, ranked gradient** ("honest_error < drift < motive < propaganda < fabrication", as L-07 calls it). Rejected: it invites reading a class as a verdict on people, and the bars are about evidence of origin, not severity.

## 7. Neutrality check

The check is whether the bars are the same whichever way a claim points, and whether the intent classes can be used to impute motive without anchored evidence.

### 7.1 Refuted claims pointing in different directions

| Direction of the false belief | Claim | What the bars require | Result |
|---|---|---|---|
| A government or official account | Tonkin: the second attack occurred (the 1964 US account) | `misreading`: document and the differing reading, both read. | Met on the files (Hanyok, intercepts). `institutional_propaganda` would need the government's own directive quoted showing a campaign; `tonkin-senior-knowledge` is contested at low; **not met**. |
| A government or institutional account (the other side of the same case) | Surfside deliberate/timed claim, Apollo hoax: popular or anti-institutional beliefs | Same bars. `fabrication` needs a forgery finding; `motivated_error` the holder's words. | Row 9 near-met for the forged item; rows 1, 8, 10 not met. The same absence of anyone's words blocks motive for the believers as it does for the government in Tonkin. |
| A popular myth that favours a person or country | Lodygin first (Soviet campaign), Canada sale, Latimer, 10000-ways | `narrative_drift` needs two read forms of the claim; `misattribution` an instance read. | Lodygin and Canada met; Latimer, 10000-ways not. The Soviet-campaign reading of Lodygin fails `institutional_propaganda` exactly as the US-government reading of Tonkin does: one secondary source, no directive. |
| A popular myth against a person or institution | Henry Ford "shows autism", Simpsonwood "hidden", thimerosal "because harmful" | `misreading` / `narrative_drift`, same evidence types. | Henry Ford near-met, Simpsonwood partly, thimerosal not (no instance read). The same standard that leaves the film and the testimony unread blocks a class for both. |
| A scholarly interpretation | Faulkner 1924 (cannibal hymn), Anatolian daughter hypothesis, measles RNA in gut | `failed_hypothesis`: the hypothesis in a document read, and what answered it. | Not met in any of the three: the proponents' documents are not read. A scholar's error gets no `motivated_error` without the scholar's own words, the same as everyone else. |

Result: the bars are symmetric because they are all about the same two things: a dated document read, and the actor's own words. They do not depend on whether the belief favoured or opposed an institution, a country, a person, a scientific view or a popular one. In this sample the bar failed for government claims, popular myths and scholarly views alike, and was met for one government account (misreading), two popular myths and no scholarly case.

### 7.2 Can the intent classes impute motive without anchored evidence?

- `motivated_error` needs the holder named and the holder's own words in `quote`, plus two sources and `read: yes` (RC3, RC6). The validator rejects each missing piece (tested: no quote, no holder, one source, confidence high). "Benefit, silence or 'who gains'" is stated as not qualifying.
- `institutional_propaganda` needs the institution named, its own dated directive or publication in `quote`, and two sources. A single newspaper history does not qualify; the lodygin author's own caution (no class on one Kommersant history) becomes the rule.
- `fabrication` needs a decisive anachronism or two independent lines of evidence and two sources, as AUTHENTICITY rule 4 already says for forgery findings. It does not require a named maker.
- All three are capped at moderate. Rows 8, 12 and 13 show the guard working: no class is proposed for them.
- Not done by the validator, and left to the reviewer: that the quote is real, that it names a motive and not a topic, and that no private individual is named. The proposed REVIEW.md line makes an unsupported intent class a blocking finding. Without that reviewer step the quote field can be filled with a plausible-looking string; this proposal does not close that, and the assessor should treat it as a limit.
- Present state: the one existing intent class on `main` (teti, `motivated_error`) fails these checks and is the first removal in 5.3.

## 8. Owner choices

1. **Seven classes or five.** Add `misreading` and `failed_hypothesis` (6 claims in this repository need them), or keep the five. With five, Tonkin 4 August and the other five stay unclassed. The validator patch is identical except for the name set.
2. **Optional or required.** Proposed: optional (3.3). Required would need an `unclassified` value.
3. **Caps.** Proposed: the intent classes are capped at moderate. The owner may choose lower (low) or no cap with higher evidence (for example two independent institutions' documents).
4. **Show the class on the page, and "Origin: not classified" when none.** Not in this proposal's validator; needs a site-builder change.
5. **How to handle the six existing classes.** Proposed: keep two (with origin blocks), remove four (teti, three lamp) with a logged review entry each. Alternative: freeze them with a dated `TODO` note until the origin evidence is read.
6. **One class per claim or several.** Proposed: one, naming how the belief arose; other origins stay in their own claims (Tonkin).
7. **Whether the `description`, `quote` and `read` fields are enough**, or whether a class should require an independent reviewer's tick (like `review.yaml`) before it shows. Proposed: reviewer step in REVIEW.md B only.
8. **Apply the owner-only text edits** (CONTRIBUTING Rule 12, REVIEW.md B): both are the owner's, not an agent's; this proposal only supplies the text.

## 9. What the independent assessor should check

- That the six claims in 1.2 rows 3-7 and 12 do carry classes on `main` (`grep refutation_class build/subjects/*/claims.yaml`).
- That nothing is applied: `git status` on the branch shows only this file.
- Standard 1: that 4 of the 6 classes in place fail the bars, by opening rows 5, 6, 7 and 12.
- Standard 4: run the test file and the validator in a clean `origin/main` worktree with the patch from 3.6 and confirm 6 errors, then 0 after the 5.3 edits.
- The weak points I know of: `read: yes` is self-asserted; the origin documents were not re-opened for this proposal; whether `misreading` and `failed_hypothesis` are the right names and the right split is a judgement the owner and assessor should test against their own cases; the sample of 17 refuted claims comes from 5 digs, 12 on `main` and 5 on one branch, so some classes have only two or three cases.

## 10. Process

Per docs/SCHEMA_PROPOSALS.md: this file on a `process/<topic>` branch and a pull request; an independent reviewer who did not write it checks the seven points against the repository and records the result on the pull request; the owner decides and the decision is logged on the pull request; only then is the change made, in its own commit, with the validator updated in the same change. This file was written on branch `claude/jolly-hopper-ira8mk` and not opened as a pull request.
