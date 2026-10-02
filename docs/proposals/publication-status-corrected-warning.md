# Proposal: a cited `corrected` source is a PS3 warning

Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.

Author: an agent. Written 2026-10-02 on branch `claude/jolly-hopper-ira8mk`. Nothing in `build/` was changed on this branch; the patches below were applied only in scratch worktrees of `origin/main` (91f6218) to measure them. `build/SCHEMA.md` and `build/conformance.py` are owner-only (CLAUDE.md), so no agent merges the change.

Owner decision this proposal serves: on 2026-10-02 the owner chose, among the options in `docs/proposals/publication-status.md` section 9 (choice 2), to raise `corrected` from exempt to a PS3 warning. This document supplies what `docs/SCHEMA_PROPOSALS.md` requires so the choice can be assessed.

## 1. The failure case

Today PS3 ignores a `corrected` source. A claim can anchor on a paper that carries a published correction, and neither the author nor the reviewer gets any signal from the validator that the correction exists or was looked at.

The real case is `build/subjects/vaccines-autism` on `origin/dig/vaccines-autism` (9a90bf0, read only). Its manifest records three `corrected` sources: `src-jain-2015` (Jain et al., JAMA 2015; erratum JAMA 2016;315(2):204), `src-verstraeten-2003` (Verstraeten et al., Pediatrics; erratum Pediatrics 2004;113(1):184) and `src-andersson-2025` (Ann Intern Med 2025; correction Ann Intern Med 2025;178(10):1527). (The brief for this proposal named four; "Jain 2015/2016" is one source and its 2016 erratum, so there are three sources.) Their `reason` fields each say "Not read" (Jain: "Not read; check before quoting figures."): the corrections were recorded, not opened.

They are cited at eight sites in that dig:
- `claims.yaml`: `va-mmr-no-detectable-increase` (Jain), `va-thimerosal-no-detectable-increase` (Verstraeten), `va-aluminum-no-detectable-increase` (Andersson), `va-simpsonwood-autism-hidden` (Verstraeten), `va-small-effect-not-excludable` (Jain), and one summary figure in `short_answer.summary_figures` (Jain, line 92, no claim id).
- `timeline.yaml`: events `a25` (Jain) and `b01` (Andersson).

Three of those claims (`va-mmr-no-detectable-increase`, the headline claim, and the thimerosal and aluminum claims) are in the dig's assessment `basis`, so a reader who relies on the answer is relying on these papers.

### Why a correction matters to a reader
The Jain correction exists and is a real published item: "Correction of Description of MMR Vaccine Receipt Coding and Minor Errors in MMR Vaccine and Autism Study", JAMA 2016 Jan;315(2):202-204 (PMID 26757474, doi 10.1001/jama.2015.17065; the dig's manifest cites page 204 only). Its title says what it corrects: the description of how MMR receipt was coded, which is how exposure is defined, and "minor errors". I read the correction's abstract on one page only (https://jamanetwork.com/journals/jama/article-abstract/2480998, through a fetch tool that summarises the page; jamanetwork.com returned 403 to the independent assessor and PubMed carries no abstract), so the following is a summary of the abstract, not a primary read of the correction: it says the correction did "not have a material effect on the findings" and that the conclusion stands. I did not open the full text. What a reader weighs is the authors' own statement plus the exposure-coding detail; a validator that says nothing hides both. I have no opened source on what the Verstraeten or Andersson corrections changed; the dig's manifest says "Not read" for them, which is itself the failure: the dig cites a paper whose correction nobody in the dig opened, and nothing flags it.

### Why exemption can hide it
A correction can range from a typo in an affiliation to a changed table. The exemption in `build/SCHEMA.md` is right that the validator cannot tell which. It then draws the wrong conclusion: because it cannot judge weight, it makes no request at all. The citing item is silent whether or not the author ever looked, and a `flagged_sources` entry on a corrected source is optional and nothing prompts it. The author's own flag is the only place the page can show the correction beside the claim (`pubstatus.claim_notice_html`, label "Corrected source"), so exempting the status means the notice appears only if the author thought of it unprompted.

## 2. Evidence

All run in scratch worktrees of `origin/main` (91f6218), with the dig's subject folder at 9a90bf0 and the dig's one-line `build/taxonomy.yaml` entry copied in to overlay it (the dig branch is behind main and lacks PS rules itself; its folder is validated with main's validator). The baseline is 104 warnings with the taxonomy entry; without it 105, because the missing entry is itself a warning (`taxonomy: vaccines-autism has no entry`). The first draft of this proposal said 105 to 113, which left the entry out; the delta of 8 is the same either way. Outputs are shown, not described.

Today's validator on the overlay, corrected sources cited, no `flagged_sources`:
```
$ python3 build/conformance.py | grep -c PS3
0
16 subjects and 107 shared nodes checked: 0 errors, 104 warnings
```
The same, after adding `flagged_sources` to the five claims and two events (and `source_notices` entries appended):
```
$ python3 build/conformance.py | grep -c PS3
0
16 subjects and 107 shared nodes checked: 0 errors, 104 warnings
```
Identical. Flagging or not flagging gives the same output today, which is the failure: the validator cannot distinguish a dig that saw the correction from one that did not.

Existing tests: `build/tools/test_publication_status.py` has 21 tests; one, `test_corrected_unpublished_published_and_unrecorded_are_silent`, asserts the exemption.

## 3. The proposed change, exactly

Rule: a source whose `publication.status` is `corrected`, cited by an item that does not list it in `flagged_sources`, gives a PS3 **warning**. Not an error. Everything else about PS3 is reused as is: where it looks, how it follows nodes, who may acknowledge.

### 3.1 Non-claim citation sites
The warning applies at every site where PS3 looks (timeline, tests, transmission, actors and the others), the same as it does for expression of concern. Reasons: (a) one rule for every warning-level status, so an author learns one thing; (b) a warning is cheap at every site, and the proposal that created PS3 (section 9 choice 3 on `docs/proposals/publication-status.md`) is a separate owner choice about errors at those sites that this change does not touch; (c) the sites measured in section 5 behave the same whichever file they are in. The cost: on non-claim pages the acknowledgement is recorded but the page does not show it (SCHEMA, Scope of PS3), so the author clears a warning that the reader of the timeline does not see. That is true today of the retracted error and is not changed here.

### 3.2 Acknowledgement
Listing the source in `flagged_sources` on the citing item (or an enclosing item, as for the other statuses) clears the warning. `source_notices` is not required for `corrected` (PS4 remains for retracted and withdrawn only), with one exception found while measuring: the summary figure at `claims.yaml:92` sits in `short_answer.summary_figures`, outside any claim. A `flagged_sources` placed on it is an existing error ("must be on the claim itself"), verified by running it:
```
ERROR    vaccines-autism:None: PS3: `flagged_sources` must be on the claim itself, not inside it (the page reads only the claim's own list)
```
so without a way out this warning could not be cleared at all. The patch therefore lets a `source_notices` entry for the source clear a `corrected` citation that is in `claims.yaml` outside any item with an `id` (the notice is shown first on the page, so the reader does see it). The exact condition is `item is None and fn == "claims.yaml"`. That is wider than "summary figure": it also covers an id-less claim and any top-level `claims.yaml` block such as `assessment` (assessor's observation, accepted: an id-less claim is reported by other rules, and the notice is a visible acknowledgement either way); the SCHEMA text in 3.3 says so. For these sites the warning does not tell the author to use `flagged_sources` (which errors there); it names the place and points to `source_notices`: `vaccines-autism:claims.yaml (outside any claim): PS3: cites <id>, which is corrected, outside any claim (for example in short_answer.summary_figures); add a source_notices entry for it, since flagged_sources is not read there; a warning, not an error`. In another file an item-less citation (for example a top-level `sources:` in `timeline.yaml`) gets the ordinary message and cannot be cleared; no dig on `main` has one (checked: item-less sites occur only in the dig's `claims.yaml`), and a synthetic test shows it. It applies to `corrected` only. The identical unclearable site for a retracted or withdrawn source is an existing defect that I did not change; it should be raised separately (no dig on `main` hits it, because no dig has a `publication` block).

### 3.3 Text added to `build/SCHEMA.md`
```diff
diff --git a/build/SCHEMA.md b/build/SCHEMA.md
index 9b9339c..53ffa37 100644
--- a/build/SCHEMA.md
+++ b/build/SCHEMA.md
@@ -291,7 +291,7 @@ top (`source_notices`) and as a notice on each claim that lists the source in it
 retracted and withdrawn sources only: a `source_notices` entry for every such source in the
 manifest, cited or not (PS4), and a `flagged_sources` acknowledgement on every item that cites
 one, in claims, timeline, tests, transmission or actors files (PS3). An expression of concern
-is a warning; `corrected` and `unpublished` are not enforced. Only claims show the
+and a corrected source are warnings; `unpublished` is not enforced. Only claims show the
 acknowledgement beside them.
 
 ### What silence means
@@ -310,12 +310,14 @@ publication:
   notice: <url or citation> # the notice itself (required for the same three)
   reason: >                 # optional: the notice's own stated reason, in plain words
 ```
-`corrected` and `unpublished` are **deliberately exempt** from `date`, `notice` and PS3: whether a
-correction changes what a source can support is a judgment, not a mechanical fact, and a dig that
-cites an erratum-bearing paper is not wrong to do so. They are shown on the page when recorded, and
-an author may list one in `flagged_sources` to show a notice beside a claim. `date`/`notice` are
-recommended for them. A paper whose earlier version was retracted and later republished is recorded
-as `published` with the history in `reason`.
+`corrected` and `unpublished` are **deliberately exempt** from `date` and `notice` (recommended for
+them), and `unpublished` from PS3: whether a correction changes what a source can support is a
+judgment, not a mechanical fact, and a dig that cites an erratum-bearing paper is not wrong to do
+so. For that reason a cited `corrected` source is a **warning** under PS3, never an error: the
+validator cannot tell an erratum to an affiliation from one to a table, so it asks the author to
+show that the correction was seen (`flagged_sources`) and leaves the judgment to the author and the
+reviewer. Both are shown on the page when recorded. A paper whose earlier version was retracted
+and later republished is recorded as `published` with the history in `reason`.
 
 ### In `claims.yaml`
 - `source_notices:` (top level) lists every retracted or withdrawn source, and may list others:
@@ -330,11 +332,20 @@ as `published` with the history in `reason`.
 - **PS1** `publication.status` is one of the six values.
 - **PS2** `expression_of_concern`, `withdrawn` and `retracted` need `date` and `notice`.
 - **PS3** A retracted or withdrawn source may be cited only by an item that lists it in
-  `flagged_sources` (error); for an expression of concern, a warning. A `flagged_sources` id must
+  `flagged_sources` (error); for an expression of concern or a corrected source, a warning (a corrected source needs no
+  `date` or `notice`). A `flagged_sources` id must
   resolve to a manifest source with a valid `publication` status (error).
 - **PS4** Every retracted or withdrawn source has an entry in `source_notices` (error); every
   `source_notices` entry names a source with a recorded status and carries a `notice` (error).
 
+A corrected source cited in `claims.yaml` outside any item that has an `id` (for example a summary
+figure in `short_answer.summary_figures`, where a `flagged_sources` is an error because the page
+reads only a claim's own list) is acknowledged by a `source_notices` entry for it; this covers every
+such citation in `claims.yaml`, including an id-less claim. The same site for a retracted or
+withdrawn source is unchanged. A corrected source cited outside any item with an `id` in another file
+(for example a top-level `sources:` in `timeline.yaml`) has no way to clear the warning; no dig on
+`main` has one.
+
 ### Scope of PS3, exactly
 PS3 looks for a manifest source id as a string anywhere in every `*.yaml` file directly in the
 subject folder (`claims.yaml`, `timeline.yaml`, `tests.yaml`, `transmission.yaml`, `actors.yaml`,
@@ -367,4 +378,6 @@ control and the log. To have it appear on the public corrections page, put the w
 CORRECTION in the log entry (`build_site.py` picks entries by that word); if the change alters a
 finding, follow the gate's revision loop (new log entry, revision round, independent check,
 visible correction). The validator does not enforce this paragraph. Recording a retraction turns the validator red until the claims carry
-`flagged_sources` and `source_notices` (intended).
+`flagged_sources` and `source_notices` (intended). Recording a correction adds warnings, not errors,
+for every item that cites the source and does not list it; the same log entry should say which
+items were looked at and whether any finding changed.
```

### 3.4 Validator change, `build/conformance.py` (not applied)
```diff
diff --git a/build/conformance.py b/build/conformance.py
index 8e0c5d7..4637096 100644
--- a/build/conformance.py
+++ b/build/conformance.py
@@ -295,6 +295,8 @@ def check_publication(r, subject, sdir, claims, d, nodes_dir=None):
             if not pub.get("date") or not pub.get("notice"):
                 r.err(f"{subject}:{sid}", f"PS2: a `{st}` publication needs its `date` and `notice`")
             flagged[sid] = st
+        elif st == "corrected":
+            flagged[sid] = st                 # PS3 warning only; no `date`/`notice` required (PS2)
     hits, ack_lists = [], []
     nodemap = _ps_nodes(subject, nodes_dir) if sources else {}
     if sources:
@@ -307,6 +309,8 @@ def check_publication(r, subject, sdir, claims, d, nodes_dir=None):
             except yaml.YAMLError:
                 continue                      # reported elsewhere
             _ps_walk(doc, set(sources), frozenset(), None, 0, fn, hits, ack_lists, nodemap)
+    noticed = {n.get("source") for n in (d.get("source_notices") if isinstance(d.get("source_notices"), list) else [])
+               if isinstance(n, dict) and isinstance(n.get("source"), str)}
     seen = set()
     for sid, fn, item, acked, names in hits:
         if (sid, fn, item, acked) in seen:
@@ -317,10 +321,19 @@ def check_publication(r, subject, sdir, claims, d, nodes_dir=None):
                                        "(the page reads only the claim's own list)")
             continue
         st = flagged.get(sid)
+        if st == "corrected" and item is None and fn == "claims.yaml" and sid in noticed:
+            continue          # cited outside any claim (summary figure): the top notice is its acknowledgement
         if st and not acked:
             msg = (f"PS3: cites `{sid}`, which is {st.replace('_', ' ')}; list it in "
                    "`flagged_sources` on that item (claim, event, test, statement) to show the status was seen")
+            if st == "corrected":
+                msg += "; a correction may or may not affect what it supports, so a warning, not an error"
             where = f"{subject}:{item}" if fn == "claims.yaml" else f"{subject}:{fn}:{item}"
+            if st == "corrected" and item is None and fn == "claims.yaml":
+                where = f"{subject}:claims.yaml (outside any claim)"
+                msg = (f"PS3: cites `{sid}`, which is corrected, outside any claim (for example in "
+                       "`short_answer.summary_figures`); add a `source_notices` entry for it, since "
+                       "`flagged_sources` is not read there; a warning, not an error")
             (r.err if st in ("retracted", "withdrawn") else r.warn)(where, msg)
     for fn, item, ids in ack_lists:
         for sid in ids:
```
The warning goes through the existing `r.warn` path in `check_publication`, so it appears in `build/conformance.py` output and in the `conformance_warnings` count that `build/tools/review_dig.py` gives a reviewer. The new warning text is: `PS3: cites <id>, which is corrected; list it in flagged_sources on that item (claim, event, test, statement) to show the status was seen; a correction may or may not affect what it supports, so a warning, not an error`.

### 3.5 Tests, `build/tools/test_publication_status.py`
```diff
diff --git a/build/tools/test_publication_status.py b/build/tools/test_publication_status.py
index 7ebf09c..ada8b2b 100644
--- a/build/tools/test_publication_status.py
+++ b/build/tools/test_publication_status.py
@@ -105,11 +105,66 @@ class Rules(unittest.TestCase):
         self.assertEqual(r.errors, [])
         self.assertEqual(len(r.warnings), 1)
 
-    def test_corrected_unpublished_published_and_unrecorded_are_silent(self):
-        for pub in ({"status": "corrected"}, {"status": "unpublished"}, {"status": "published"}, None):
+    def test_unpublished_published_and_unrecorded_are_silent(self):
+        for pub in ({"status": "unpublished"}, {"status": "published"}, None):
             r = run(make({"claims.yaml": {"claims": [claim()]}}, [src(pub)]))
             self.assertEqual((r.errors, r.warnings), ([], []), pub)
 
+    def test_corrected_cited_without_flag_is_one_warning_no_error(self):
+        for pub in ({"status": "corrected"}, {"status": "corrected", "date": "2016-01-19", "notice": "Erratum"}):
+            r = run(make({"claims.yaml": {"claims": [claim()]}}, [src(pub)]))
+            self.assertEqual(r.errors, [])
+            self.assertEqual(len(r.warnings), 1)
+            self.assertIn("PS3", r.warnings[0])
+            self.assertIn("corrected", r.warnings[0])
+
+    def test_corrected_flagged_is_silent_and_needs_no_source_notice(self):
+        r = run(make({"claims.yaml": {"claims": [claim(flagged=["src-a"])]}}, [src({"status": "corrected"})]))
+        self.assertEqual((r.errors, r.warnings), ([], []))
+
+    def test_corrected_uncited_is_silent(self):
+        r = run(make({"claims.yaml": {"claims": [claim(sid="src-b")]}}, [src({"status": "corrected"}), src(None, "src-b")]))
+        self.assertEqual((r.errors, r.warnings), ([], []))
+
+    def test_corrected_other_files_and_node_route_warn(self):
+        nd = tempfile.mkdtemp()
+        with open(os.path.join(nd, "n1.yaml"), "w") as f:
+            yaml.safe_dump({"id": "n1", "manifest": {"subject": "s", "source": "src-a"}}, f)
+        files = {"claims.yaml": {"claims": []},
+                 "timeline.yaml": {"events": [{"id": "e1", "sources": ["src-a"]}, {"id": "e2", "node": "n1"}]},
+                 "actors.yaml": {"actors": [{"id": "p", "statements": [{"id": "st", "source": "src-a"}]}]}}
+        r = run(make(files, [src({"status": "corrected"})]), nd)
+        self.assertEqual(r.errors, [])
+        self.assertEqual(len(r.warnings), 3)
+        files["timeline.yaml"]["events"] = [dict(e, flagged_sources=["src-a"]) for e in files["timeline.yaml"]["events"]]
+        files["actors.yaml"]["actors"][0]["statements"][0]["flagged_sources"] = ["src-a"]
+        r = run(make(files, [src({"status": "corrected"})]), nd)
+        self.assertEqual((r.errors, r.warnings), ([], []))
+
+    def test_corrected_cited_outside_a_claim_is_cleared_by_source_notice_only(self):
+        doc = {"short_answer": {"summary_figures": [{"figure": "f", "source": ["src-a"]}]}, "claims": []}
+        pub = {"status": "corrected"}
+        r = run(make({"claims.yaml": doc}, [src(pub)]))
+        self.assertEqual((r.errors, len(r.warnings)), ([], 1))
+        self.assertIn("source_notices", r.warnings[0])
+        self.assertNotIn("list it in", r.warnings[0])
+        r = run(make({"claims.yaml": dict(doc, source_notices=NOTICE)}, [src(pub)]))
+        self.assertEqual((r.errors, r.warnings), ([], []))
+        # the same site for a retracted source stays an error (not changed by this proposal)
+        r = run(make({"claims.yaml": dict(doc, source_notices=NOTICE)}, [src(RETRACTED)]))
+        self.assertEqual(len(r.errors), 1)
+
+    def test_corrected_neutrality_state_and_direction_do_not_matter(self):
+        out = []
+        for state in ("established", "contested", "refuted", "proposed", "searched_gap"):
+            for text in ("The lamp was invented by X.", "The lamp was not invented by X."):
+                c = claim(state=state)
+                c["statement"] = text
+                r = run(make({"claims.yaml": {"claims": [c]}}, [src({"status": "corrected"})]))
+                out.append((r.errors, sorted(w.split(": ", 1)[1] for w in r.warnings)))
+        self.assertTrue(all(o == out[0] for o in out))
+        self.assertEqual((out[0][0], len(out[0][1])), ([], 1))
+
     def test_unresolved_ids(self):
         files = {"claims.yaml": {"source_notices": [{"source": "src-zz", "notice": "n"}] + NOTICE,
                                  "claims": [claim(flagged=["src-a", "src-yy"])]}}
```
Results (run, not asserted): on `main` 21 tests pass; with the patch 27 pass; with the new tests against the unpatched validator, 4 of the new tests fail (as they should) and the replaced test is the only one removed.

## 4. What it does not change
- Errors for `retracted` and `withdrawn` (PS3 error, PS4, PS2) are unchanged, as are the expression of concern warning and the `unpublished` exemption. A corrected source still needs no `date` or `notice`.
- No existing finding, claim state, anchor, confidence or log is altered. No dig content changes. A dig with no `publication` block gets no new output (section 5).
- Published pages: unchanged. `build_site.py` and `pubstatus.py` are not touched. Validator warnings are not published anywhere: they appear in the validator output and in the reviewer's `conformance_warnings` count, and nowhere on a page. A page shows a correction only if the author lists `flagged_sources` (notice beside a claim) or `source_notices` (list at the top), as today.
- The warning does not block merge or publication: `conformance.py` exits clean with warnings (shown above: "0 errors, 112 warnings" is a pass; exit status 0), and `docs/PUBLISH_GATE.md` makes only a failing validator (errors) stop deployment; it does not mention warnings. The reviewer sees the count.
- Flagging prints the manifest `reason` publicly beside the claim (`pubstatus.claim_notice_html`). SCHEMA says `reason` is the notice's own stated reason in plain words. An author who flags to clear a warning must first make `reason` say that, not a to-do: the dig's three reasons today are "Not read; check before quoting figures." (Jain), "Not read." (Verstraeten) and "Not read. A 2026 reanalysis says the updated supplement shows autism associations." (Andersson), which are internal notes and would be printed to readers as they stand. This is a cost of the change for any dig that records `corrected` without having read the notice.
- It does not make any author read the correction. An author can list the source in `flagged_sources` without opening the erratum. The rule shows the correction was seen only in the sense that someone listed it; it is a prompt, not proof (same as the other PS rules).

## 5. Impact

### 5.1 All 15 digs on `main`
Validator output before and after, `python3 build/conformance.py` in worktrees of `origin/main` with and without the patch, compared with `diff`:
```
$ diff before.txt after.txt   (15 digs, as on main)
(no output)
15 subjects and 107 shared nodes checked: 0 errors, 93 warnings     (before and after)
```
Per dig, from a scripted read of every `sources/MANIFEST.yaml`: no dig on `main` has a `publication` block on any source. Digs with a manifest and zero `publication` blocks: casket-letters (7 sources), congress-promise-vote (5), eikon-basilike (9), flydubai-fz1073 (33), gulf-of-tonkin (11), incandescent-lamp (44), mcafee-and-surfside (10), teti-pyramid-texts (7). Digs with no manifest: apollo-landings, chemtrails, dyatlov-pass, flood-myths-worldwide, proto-indo-european, votes-2009-present, votes-johnson-tonkin. Warnings added: 0 for each of the 15. Migration: none.

### 5.2 `origin/dig/vaccines-autism` overlay
Before the patch: 104 warnings with the dig's taxonomy entry (105 without it), 0 PS3 lines (section 2). After, at dig commit 9a90bf0:
```
WARNING  vaccines-autism:claims.yaml (outside any claim): PS3: cites `src-jain-2015`, which is corrected, outside any claim (for example in `short_answer.summary_figures`); add a `source_notices` entry for it ...
WARNING  vaccines-autism:va-mmr-no-detectable-increase: PS3: cites `src-jain-2015`, which is corrected ...
WARNING  vaccines-autism:va-thimerosal-no-detectable-increase: PS3: cites `src-verstraeten-2003`, which is corrected ...
WARNING  vaccines-autism:va-aluminum-no-detectable-increase: PS3: cites `src-andersson-2025`, which is corrected ...
WARNING  vaccines-autism:va-simpsonwood-autism-hidden: PS3: cites `src-verstraeten-2003`, which is corrected ...
WARNING  vaccines-autism:va-small-effect-not-excludable: PS3: cites `src-jain-2015`, which is corrected ...
WARNING  vaccines-autism:timeline.yaml:a25: PS3: cites `src-jain-2015`, which is corrected ...
WARNING  vaccines-autism:timeline.yaml:b01: PS3: cites `src-andersson-2025`, which is corrected ...
16 subjects and 107 shared nodes checked: 0 errors, 112 warnings
```
(113 without the taxonomy entry.) That is 8 warnings (the brief expected 3: it is 3 corrected sources, which are cited at 8 sites). Added 8 warnings, 0 errors: 104 becomes 112 (105 becomes 113 without the taxonomy entry; an earlier draft gave only the second pair). The summary figure is reported as "outside any claim" with its own wording (section 3.2). The dig has since moved to c41e40f (L-28), where `va-mmr-no-detectable-increase` no longer cites Jain: there the same measurement gives 102 to 109, 7 sites. Figures in this proposal are at 9a90bf0 unless stated.

Migration, run and checked: adding `flagged_sources` on the five claims and the two timeline events, and a `source_notices` entry for each of the three sources, brings the overlay back to `0 errors, 104 warnings` (the baseline) and no PS3 line. Adding only the seven `flagged_sources` leaves exactly one warning (105), the summary figure, and a `source_notices` entry for `src-jain-2015` clears it. **Migration trap, reproduced:** the dig already has `source_notices` entries for `src-wakefield-1998` and `src-hooker-2014`; the three new entries must be appended to that list. Replacing the list gives two PS4 errors (`src-wakefield-1998` and `src-hooker-2014` retracted with no entry). The dig's owner-level content decisions are the author's; this proposal does not edit the dig. A published dig follows 5.3.

### 5.3 Interaction with "Changing a status after publication"
That rule (SCHEMA.md, end of Publication status) says recording or changing a status on a published dig is a correction under the gate and needs a new `log.yaml` entry. Recording a `corrected` status was silent before and now adds warnings, not errors: the dig stays green but the log entry is still required, and the added sentence in 3.3 asks that it say which citing items were looked at and whether any finding changed. If a finding changes, the gate's revision loop applies as before. Nothing in the validator enforces the log entry (as now).

## 6. Alternatives considered
1. **Keep `corrected` exempt (today).** Rejected: section 2 shows flagged and unflagged give identical output, so the validator cannot prompt the author. The existing reason (the validator cannot judge materiality) is true, and is why the proposal stops at a warning.
2. **Make it an error.** Rejected. A correction can be an affiliation fix; an error would force a notice on sound claims, which the first proposal's section 3.4 rightly says teaches authors to ignore notices, and would turn the validator red on a dig for something the validator cannot weigh. Retracted and withdrawn are errors because the source's own journal has withdrawn it; a correction is a statement that the paper stands with changes.
3. **Warn only at review time (a checklist item for the reviewer).** Rejected as the only measure, kept as a complement. A checklist is not run on every commit, varies by reviewer and was the proposal's own remedy for what no rule can see; but this case is a fact the validator already holds (a recorded status) and a reviewer should not be the first to find it. A reviewer sees the warning count in `review_dig.py` anyway.
4. **Warn on claims only, not non-claim sites.** Considered (3.1). Rejected for rule uniformity; the owner can still choose it, noted in section 8.
5. **Clear the warning by `source_notices` anywhere.** Rejected: it would exempt every corrected citation the moment a top notice exists, which removes the per-item acknowledgement. The narrow clause in 3.2 is limited to the one place a per-item flag cannot go.

## 7. Neutrality check
The rule keys on `publication.status` of a source, never on the claim's state, direction or topic. Checked three ways, all run.

(a) Unit test `test_corrected_neutrality_state_and_direction_do_not_matter`: the same corrected source against claims in each of five states, once stating a thing and once its opposite; the ten results are identical (no error, one warning).

(b) Real digs pointing different ways. In a temporary copy of each dig, one manifest source at a time was set to `corrected` (synthetic: no date, no notice) with no flags, `check_publication` run, and warnings counted by the state of the claim they sit on or the file they sit in. For the same source set to `retracted` the PS3 error sites were counted too: in every dig the warning sites for `corrected` equal the error sites for `retracted` (last column), so the new rule finds exactly the sites PS3 already finds and nothing else.

| Dig (its own answer) | Sources injected | PS3 warnings | Errors | By claim state or file | Warning sites differing from retracted error sites |
|---|---|---|---|---|---|
| gulf-of-tonkin (answer: no) | 11 | 23 | 0 | established 11, searched gap 2, actors.yaml 8, timeline.yaml 2 | 0 |
| casket-letters (unsettled) | 7 | 12 | 0 | established 6, proposed 5, contested 1 | 0 |
| eikon-basilike (unsettled) | 9 | 9 | 0 | established 3, proposed 6 | 0 |
| congress-promise-vote | 5 | 12 | 0 | established 6, actors.yaml 6 | 0 |
| incandescent-lamp (partly) | 44 | 165 | 0 | established 32, contested 22, refuted 19, searched gap 14, proposed 7, timeline.yaml 44, transmission.yaml 27 | 0 |
| flydubai-fz1073 (unsettled) | 33 | 135 | 0 | established 54, searched gap 61, proposed 16, transmission.yaml 4 | 0 |

These totals match the PS3 site counts the first proposal recorded for the retracted injection (section 7 of `docs/proposals/publication-status.md`, re-run figures: 23, 12, 9, 12, 165, 135). Every claim state is hit; a source cited only by established claims and one cited only by proposed claims behave the same.

(c) What is not neutral. Warnings appear only where someone recorded a correction. A dig on a topic that draws scrutiny gets its sources looked up and so gets warnings; one that does not may never be. That asymmetry belongs to who records, not to the rule, and is the one the first proposal already states (silence means unchecked). The proposal also adds more work for a dig that records more, which could discourage recording; that is the cost of the warning, and why it is not an error.

## 8. Decisions for the owner
None expected beyond final approval. The independent assessment (`assessment-corrected-warning.md`, verdict: meets the standards with specific changes, all now made) recommends the following. These are RECOMMENDATIONS only; the decision is the owner's.
1. The `source_notices` clause for citations outside a claim (3.2): keep it, with its own warning wording and the SCHEMA text stating its full reach; and open a separate proposal for the existing retracted/withdrawn summary-figure defect (an unclearable error that no dig on `main` hits today).
2. Non-claim sites (3.1): warn at all PS3 sites, as PS3 does. The warning sites equal the retracted error sites in every dig tested, and none is uncleared on `main`.
3. Approve as a warning, not an error. Keep-exempt is rejected on the evidence in section 2.

Also noted by the assessor: on the vaccines-autism dig dig-level warnings rise from 11 to 19, and three claims would show two warnings each; clearing is one pass (7 flags, 3 notices). A rule cleared without reading invites rubber-stamping; this is stated in section 4.

## 9. Files this proposal would change, if approved
`build/SCHEMA.md` (the text in 3.3), `build/conformance.py` (3.4), `build/tools/test_publication_status.py` (3.5), each in the same owner-approved commit. This branch adds only `docs/proposals/publication-status-corrected-warning.md`.

## 10. Independent assessment and decision
Independent assessment: done (meets the standards with specific changes R1 to R5; this revision makes them). Owner decision: pending.
