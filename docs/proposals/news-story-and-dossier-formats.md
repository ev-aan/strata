# Proposal: a case file and a live story for News Review entries (evidence dossier, media record, `story.yaml`)

Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.

Author: an agent (Claude Sonnet 5.5). Everything below was run on 2026-10-02 and 2026-10-03 in `/home/user/strata`, branch `claude/jolly-hopper-ira8mk`, tip `051778c` ("Flydubai FZ1073: record author responses to R5-1 and R5-2 in review.yaml", 15 digs, 6 on the site), through scratch worktrees in the session scratchpad. Nothing in the repository was changed except this file. Another agent was updating `build/subjects/flydubai-fz1073/` on this branch while I worked; I did not touch it, and every number about FZ1073 is for `051778c` (39 claims, 91 timeline events, 65 manifest sources, log L-01 to L-33, three transmission chains). If that folder has moved, re-run the commands in section 2 before the assessment. The branch moved from `a88dd65` to `051778c` (the FZ1073 author's responses to review round 5: L-31 to L-33, a corrected landing-time source note and small claim edits) while I worked; the tooling files (`build/tools`, `conformance.py`, `SCHEMA.md`) did not change between the two, claim counts and states are the same, and I re-ran every command and rebuilt every output at `051778c`. A first attempt at this proposal was cut off by a usage limit before it was committed; this is a redo, and I re-ran the prototype against the current tip rather than reusing its output.

This file stays on the branch `claude/jolly-hopper-ira8mk` for now. Under docs/SCHEMA_PROPOSALS.md it should go out as its own `process/news-story-and-dossier-formats` pull request (not bundled with other proposals), be assessed by an independent reviewer, and only then be decided by the owner. No agent merges it: it changes `build/SCHEMA.md`, `build/conformance.py`, `build/news.yaml` and `build/tools/`, all on the owner-only list (docs/REVIEW.md).

## Summary

- **The ask.** For the live, published FZ1073 News Review entry the owner asked for (1) a case file for legal review: an evidence dossier with no legal conclusions, a media timeline (who reported what, when, how it changed, how it spread, statements against material), and a flag where a lawyer would need the primary record; and (2) a news-outlet-style live story with academic rigor now (running story, dated updates, an evidence ledger, a correction log) and a long-form investigative report later.
- **Most of it needs no new data.** A dossier and a media timeline of the *timeline and transmission records the dig already has* can be generated from `claims.yaml`, `sources/MANIFEST.yaml`, `timeline.yaml`, `transmission.yaml`, `log.yaml` and `review.yaml`. I built that generator and ran it on all 10 dig-format subjects (0.01 to 0.32 s each). For FZ1073 it gives a 132-page A4 case file (HTML 450 KB) with no new file.
- **What genuinely needs new data, and only that:**
  1. `media.yaml` (optional, per subject): a record of reports with first-version time, in-place edits, origin and who was cited. The existing timeline's 41 media events cannot carry this: they have a time, a label, sources and a free-text `detail`, and only 19 of the 41 mention a modification at all, in prose (section 1.4). An alternative that extends timeline events is set out in 6.2 as an owner choice.
  2. `story.yaml` (optional, per News Review subject): dated updates of paragraphs whose every sentence cites a claim id and carries a *mode* (`attributes`, `open`, or `states`). A rule makes a sentence unable to be stronger than its claim (SR3).
  3. One optional manifest field, `address_withheld`, and one optional `review.yaml` line, `story_through`, written by the independent reviewer.
- **No data downloads are added.** The dossier and story are static HTML pages. The build writes no PDF; "Print, Save as PDF" is the reader's browser's job, helped by print CSS. `news.yaml` chooses `dossier: private` (written to the git-ignored `private/`, never deployed) or `public` (a `noindex` page). I recommend `private` until the owner decides (section 10).
- **Nothing that exists changes.** Claim states, weights, confidence and the publish gate are untouched; for each of the 15 subjects the validator gives the same errors and warnings before and after (section 5). A dig without the new files is built exactly as today.
- **One finding the owner should see now (section 1.6):** the current build already puts `claims.yaml`, `MANIFEST.yaml`, `review.yaml` and `timeline.yaml` on every published dig as downloads, and links three of them from the dig page. That sits against the owner's decision that data downloads stay private. This proposal adds none and does not touch them; the decision is the owner's.

## 0. What was asked, and the limits on it

| Owner request | Where it is met |
|---|---|
| Case file for legal review: chain of evidence per fact, provenance, who said what and when, conflicts, what is unverified | Dossier sections 3, 4, 5, 7, 9 (generated, section 3.1) |
| Media timeline: who reported what, when, how it changed; where each claim first appeared and how it spread; official statements against material evidence | Dossier sections 4 and 6 (generated from the timeline and transmission record; first-report, edit and origin data from `media.yaml`, section 3.2) |
| Flag where a lawyer would need the primary record | "primary record needed" flag per claim, section 8 "Primary records to obtain", section 7 "What we could not verify" |
| News-outlet-style live story with an evidence ledger, dated updates, correction log | `story.yaml` and the story page (section 3.3) |
| Long-form investigative report later | Not built now. It is the same sentence-and-claim format with longer prose; section 3.8 says what would be added and why it should not be designed yet |
| No legal conclusions; no data downloads; never name the suspect, private individuals or victims | Rules D1 to D6 and SR7 to SR9; section 8 |

## 1. The failure case

The dig page is a good statement of findings. It is not a case file and not a story, and the specific things below cannot be got from it. Each was measured by building the site at `051778c` and reading the output (`failure2.py`, output in 1.2).

### 1.1 What a reader gets today

`/digs/flydubai-fz1073-cockpit-attack-news-review/` is 177 KB with these sections only: Where it stands; The headline finding; Where evidence and belief differ; Timeline; Publication review; All claims; Sources; The data. There is no running story and no dated "what we knew when" on the page. `build/news.yaml` and the News Review page link to the dig page. Nothing reads like the story an outlet would run, and nothing ties a plain sentence to a claim, a confidence and a source.

The headline itself is true and plain ("Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; no evidence of staging found", 93 characters). The problem is the lack of a *story layer* that keeps the same discipline for every sentence, and the lack of a place where a correction such as L-26 (the Saudi statement quoted from CNN and Al Jazeera was not the agency's own wording) is visible in context.

### 1.2 What a lawyer cannot get today

Output of `failure2.py` against the built site and the files of `051778c`:

`````text
1. Fields the manifest holds per source vs what the page's Sources list prints
   sources in manifest: 65  listed on page: 65
   read        in manifest for 65 source(s); printed in the source line: no
   retrieved   in manifest for  0 source(s); printed in the source line: no
   stored_as   in manifest for  4 source(s); printed in the source line: no
   sha256      in manifest for  0 source(s); printed in the source line: no
   origin      in manifest for  0 source(s); printed in the source line: no
   provenance  in manifest for  4 source(s); printed in the source line: no
   tests       in manifest for  4 source(s); printed in the source line: no
   gaps        in manifest for  6 source(s); printed in the source line: no
   next_step   in manifest for 21 source(s); printed in the source line: no
   what each source line prints, in full: title, link, and '· authenticity: <status>'; example: FlightAware, FZ1073 (FDB1073) flight history, row for 30-Sep-2026 · authenticity: authenticated
2. Log
   log entries: 33  entry ids the dig page mentions: 14 ['L-01', 'L-04', 'L-05', 'L-11', 'L-12', 'L-14', 'L-15', 'L-16', 'L-17', 'L-18', 'L-20', 'L-21', 'L-31', 'L-33']
   log entries printed on any published page: 0 (log.yaml is not copied to the site and no template renders it)
   (L-24 says 'the log is published on the dig page'; the build does not do this.)
3. Corrections page: how the build cuts each FZ1073 correction
   L-14: entry  2134 chars, page shows  460; ends: ...' slice; treat as UNRESOLVED until the raw ADS-B CSV is read.'
   L-17: entry  2877 chars, page shows  137; ends: ..."xt stays). (1) L-03(a) said CNN's departure time ('6:05 a.m."
   L-18: entry  1367 chars, page shows  242; ends: ...' knowledge and was not taken from a source read in this dig.'
   L-22: entry  4222 chars, page shows  195; ends: ...'-event-simulated was held as refuted at moderate confidence.'
   L-26: entry  2143 chars, page shows  272; ends: ..."nd in it'). That was wrong: the statement is at https://www."
   L-31: entry  5267 chars, page shows  287; ends: ..."he Saudi item ('21:31 Local Time 18:31 GMT') a render clock."
   entries that state a correction but are not matched by the page's regex: ['L-23']
4. Timeline page exists: 181891 bytes; it plots event times and links each dot to a source; it shows no first-report time, no edit, no origin
`````

Reading it:

- **Provenance is in the manifest but not on the page.** Every one of the 65 sources has `read`; 21 have a `next_step`; 6 carry a checked date; 4 have a stored copy. The page's source line prints title, link and `authenticity: <status>` and nothing else: no provenance, tests run, gaps, stored copy or hash, and no origin. A lawyer cannot see from the page that `src-saudi-moi-original` was read in full, is authenticated at moderate strength, has a stored copy, and that its Arabic original and release hour were not seen.
- **The log is not on any page.** 33 entries (L-01 to L-33) record what was known when, including every correction. The build does not render `log.yaml`; the dig page mentions 14 of the 33 ids in passing. (Log entry L-24 says "the log is published on the dig page"; it is not.) The log is the "what was known when" the NEWS_REVIEW rules promise.
- **Corrections are cut by a regular expression.** `build_site.py` (line 272) takes the text from the word `CORRECTION` to the end of the third sentence. The corrections page shows L-17 as 137 characters of a 2,877-character entry, ending mid-sentence at "(6:05 a.m.". L-23 states a correction but does not match the pattern, so it does not appear. A reader of the corrections page cannot tell what was corrected.
- **No hash and no retrieval date per source.** The manifest has one `retrieved` date for the whole file and no `sha256` for any source. The four stored texts could be hashed at build time; nothing does.
- **No view of "who said what, and when" against material.** The timeline page is a chart: events with times, each dot linking to a source. It shows no first-report time, no edit and no origin (1.4).

### 1.3 What the dig does record that no page shows: claim ids

These claims are the cases where the missing view matters:

- `fz1073-both-pilots-injured` (established, high, primary): the Saudi Interior Ministry text, read at source on 2 October, says "an altercation occurred in which the co-pilot assaulted the captain". First-day pages (CNN, Al Jazeera) rendered it "revealed an assault on the captain by the co-pilot". The correction is L-26 item 2. Today it is visible only in the log, which is not on a page.
- `fz1073-landing-time` (contested, low): the ministry says "9:45 a.m." with no time zone; 06:45 UTC assumes Saudi time. AirNav Radar and Al Jazeera give about 06:58 UTC; CNN gives "9:54 a.m.". L-26 item 3 and L-17 are corrections that changed how this was worded.
- `fz1073-israel-says-omani` (established, moderate) and `fz1073-omani-nationality-unconfirmed` (searched gap, low): what Israel's Prime Minister said versus what an authority outside Israel has confirmed. A story sentence on this has to be an attribution and an open question; nothing today forces that.
- `fz1073-no-findings-yet`, `fz1073-motive-not-established`, `fz1073-event-simulated` (all searched gaps resting on an absence anchor): "we found no evidence of X" must never read as "X did not happen". Today a reader meets this only as one claim in 39.

### 1.4 The media timeline: what the existing timeline can and cannot carry

`timeline.yaml` has 91 events. 41 are `kind: media`; 35 of those sit in the three media panels (`media30`, `media01`, `media02`). Each media event has these keys and no others: `id, panel, lane, time, precision, date_basis, kind, status, sources, label, detail` (and `end`). I checked whether it can answer the owner's questions:

| Question | Can an existing media event carry it? |
|---|---|
| When did the outlet first publish? | Yes: `time` (UTC), with `date_basis` |
| Did the page change after publication? | Only as prose in `detail` ("modified 08:10:35Z"): 19 of 41 events mention modified, edited or updated; 15 mention `datePublished`. Not machine-readable, and one event is one moment |
| What was the first wording versus the current wording? | No field |
| Whose statement does the outlet carry (who was cited)? | No field (`label` sometimes says) |
| Which reports are copies of one origin? | No field. `sources` lists what the event cites, not what it copies |
| Which point of the story does the report carry, so first appearance can be computed? | No field |

So per-report first-appearance, edit history, origin and "said by" cannot be generated; the dossier can show the 41 events in time order but cannot compute "where each point first appeared". Section 3.2 proposes the smallest record that can, and 6.2 weighs the alternative of putting those fields on timeline events.

### 1.5 What is not a failure

To be fair to the current system: the dig page does show every claim with its state, confidence, anchor and what would change it; the timeline page works and links sources; the log exists and is append-only; the conformance validator rejects an anchor that cites a media record (checked in section 2, item 8). The gap is a *view* and a *story layer*, not the underlying discipline.

### 1.6 A separate finding: data files are already published

The built site at `051778c` contains, for FZ1073 (and likewise for the other published digs): `claims.yaml`, `MANIFEST.yaml`, `review.yaml` and `timeline/timeline.yaml`. The dig page links the first three under "The data" (`build_site.py` around lines 251 to 262). `deploy.yml` refuses `.csv`, `.geojson`, `.graphml` and `SHA256SUMS*` in the site but not `.yaml` or `.pdf`; `build/site.yaml` says "The data behind every page is plain YAML you can read and challenge."

The owner has decided that data downloads stay private. I read this as applying to what is added now. **This proposal adds no download and does not change the existing ones.** Whether the existing YAML links should stay, and whether `deploy.yml` should also refuse `*.pdf`, are owner choices (O5); `.github/` is owner-only.

## 2. The evidence: what I ran

All commands were run from the scratchpad `story/` folder with the proposed files in a scratch worktree `wtT` (detached at `051778c` plus the files of this proposal); a pristine worktree `wtB` (`051778c`) gives "before". Prototype files are in Appendices A to D.

1. `python3 wtB/build/tools/build_site.py siteB` then `python3 failure2.py`: the output in 1.2.
2. Validator before and after, all 15 subjects (`conftable.txt`, section 5): same errors and warnings per subject. With stories for Gulf of Tonkin and the incandescent lamp added in a scratch copy (neutrality, section 7): 0 errors; the only new warnings are two SR12 notices ("no `story_through`") because those scratch stories have no reviewer line.
3. `python3 build/tools/test_story_dossier.py -v`: 36 tests, all pass (list in Appendix D). `python3 build/tools/test_publication_status.py`: 21 tests, pass (unchanged).
4. `sh run_all.sh`: builds the FZ1073 dossier (HTML, then `weasyprint` to PDF for checking only), a dossier from existing data alone (`--bare`), the FZ1073 story, and dossiers and stories for Gulf of Tonkin and the lamp. Outputs inspected as text and as rendered pages (PDF pages 1 and 40 viewed).
5. `python3 table2.py`: dossier build for all 15 subjects, times and sizes (section 5).
6. `python3 bad_story_demo.py`: the validator run on eight deliberately broken copies of the FZ1073 story (section 3.6).
7. SR11 and SR12 end to end through `conformance.py --base`: a scratch commit of the proposed files, then (1) an in-place edit of an earlier sentence (error), (2) the same edit with a new log entry naming it in `redacts` (accepted: N26), (3) a renamed update (errors), (4) an appended update (accepted, with the SR12 notice that it is held back until reviewed); section 3.6.
8. A claim anchor citing a media-report id (`m-003`): `ERROR flydubai-fz1073:fz1073-diverted-tabuk: anchor source m-003 is not in sources/MANIFEST.yaml (SCHEMA N25)`. A media record therefore cannot be cited as evidence by the existing rule, with no new check needed.
9. `build_site.py` on the scratch worktree with `story_through` set to `u-004`, `u-003` and absent (SR12): story with all four updates, story without `u-004`, no story page at all.

## 3. The proposed change

Three layers, in order of how little they add.

### 3.1 Layer 1: generated from existing data, no new file

A dossier and a media timeline are *views* of files a dig already has. The generator reads `claims.yaml`, `sources/MANIFEST.yaml`, `timeline.yaml`, `transmission.yaml`, `log.yaml`, `review.yaml` and the shared nodes the timeline names, and the publication-status fields (`publication`, `source_notices`, `flagged_sources`; the rendering functions are the existing `pubstatus.py`). It adds no fact and no prose beyond fixed labels.

What each section is made from:

| Dossier section | Made from | Answers |
|---|---|---|
| 1 Position in one page | `assessment` (question, headline, key points); counts of claims by state; sources listed, not read, stored; claims needing a primary record; `review.yaml` status | What is the position; how much rests on what was not read |
| 3 Fact register | every claim: statement, state, kind, confidence, evidence and adoption ratings, `anchor_checked`, anchor, each cited source (read or not, authenticity, origin if known, stored copy), publication notices, `would_change_if`, `next_step`; flag "primary record needed" or "primary text read" | Chain of evidence per fact |
| 4 Who said what, and when | all timeline events in UTC order, labelled Statement (kind `official`), Material (`data`), Witness, Report (`media`), each with its sources; shared nodes expanded | Official statements beside the material they can be tested against |
| 5 Conflicts | events with `status: disputed` or `alt_time`; contested claims and their `disputed_by`; (with `media.yaml`) points reported in two or more wordings, by origin | What conflicts, without judging it |
| 6 Media timeline | with `media.yaml`: first appearance per point, reports in time order, in-place changes; always: the dig's own transmission chains (how a claim spread; confers no weight) | Who reported what, when, how it changed, how it spread |
| 7 What we could not verify | searched gaps and their next steps; established or refuted claims not read at primary level; sources not read; sources read but authenticity not checked; the reviewer's open items | A lawyer's "what is missing" list |
| 8 Primary records to obtain | sources not read, and primary-class sources with no stored copy, with the claims that rest on them | What a lawyer would have to fetch |
| 9 Source register | per source: address, kind, access, authenticity and strength, origin, date checked, stored copy and its **sha256 computed at build**, publication status or "not looked up", provenance, tests, tested by, gaps, next step, which claims cite it | Provenance and independence |
| 10 Log | `log.yaml` in full, in order | What was known when, including corrections |
| 11 Method and file fingerprints | sha256 of each data file used; time; commit | Which version of the record this is |

Run on FZ1073 with the existing data only (`--bare`, no `media.yaml`) the media section degrades honestly instead of inventing:

`````text
6. Media timeline: who reported what, when, and how it changed
No per-outlet media record is held for this subject (no media.yaml). What exists is shown below: the statements and material from the timeline, the transmission chain if there is one, and any "what was reported when" entry in the log. First appearance, in-place edits and spread by outlet cannot be shown without that record.
How a claim spread: How the claim that the FZ1073 incident was staged by Israel spread
About flydubai-fz1073:fz1073-event-simulated. Spread is adoption, never evidence of the claim; where a step is dated by day only, the order inside the day is not known.
2026-09-30 (day) origin: A first X post declaring the event an Israeli false flag, reported as 67 minutes after the emergency signal. Source src-jpost-910349, read: yes. As reported from a study by two advocacy groups (Combat Antisemitism Movement and Antisemitism Research Center); the post itself and the study were not read.
2026-09-30 (day) amplification: Posts containing 'false flag', counted over a 12-hour window by the same groups. Source src-jpo
`````

With the existing data alone, the dossier is 371 KB (no media record) and has all the other sections. The first-appearance table and the edit list need layer 2.

**What a lawyer sees (FZ1073, as generated).** Position and scope:

`````text
1. Position in one page
Was the Flydubai FZ1073 cockpit attack of 30 September 2026 manufactured?
Unsettled, leaning slightly no: no evidence of staging was found, but only statements and reports were read. Motive and vetting are open.
Flydubai and the UAE say an altercation; the Saudi ministry's own text says the co-pilot assaulted the captain, injuring both; landing at Tabuk. No raw data.
No evidence was found that anyone staged it or let it happen; the Omani-pilot and timing doubts are open questions, not findings.
No investigating body has given a motive, a weapon, how the co-pilot was rostered, or what the recorders show.
Claims39: 14 established, 2 contested, 5 proposed, 18 searched gapSources65 listed; 14 not read here; 4 stored in full or in partPrimary record needed35 of 39 claimsIndependent reviewpassed_with_open_items, 2026-10-02Generated2026-10-03 from commit 051778c
`````

One fact card (`fz1073-both-pilots-injured`), as generated:

`````text
fz1073-both-pilots-injured established reported
The Saudi Interior Ministry's own statement (SPA, English) says the captain and co-pilot were transferred to a local hospital, that "an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals", and that both pilots left Saudi Arabia for Abu Dhabi on 1 October "accompanied by the UAE security team"; the airline's CEO says the captain has returned to the UAE after medical clearance.
Our ratingconfidence high; evidence 4 of 5; public belief 5 of 5; evidence class primary_text; source checked: primaryAnchorofficial-statement: Saudi Press Agency, 1 Oct 2026 (English; raw HTML read; stored in sources/spa-moi-2026-10-01.txt): "The captain and co-pilot were transferred to a local hospital for medical evaluation and treatment." "Preliminary investigations conducted by competent Saudi authorities, in coordination with a security team from the United Arab Emirates, revealed that an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals." "following medical clearance, both pilots departed Saudi Arabia for Abu Dhabi on Thursday, October 1, accompanied by the UAE security team." The item attributes this to "an official source at the Ministry of Interior". It says nothing about a stabbing, a weapon, nationality, motive, terrorism, arrest, custody or charges. flydubai CEO statement [read]: the Captain "has now returned to the UAE following medical clearance". GCAA statement via Emirates 24|7 [read]: the Captain "is in good condition, and is receiving the necessary medical treatment". Tabuk airport, via Khaleej Times [read]: both injured and taken to hospital.
Cited sources (6). Origin recorded (media record) for 4 of 6; none is inferred. One origin is counted once however many outlets copy it, and a live blog can hold several.
src-saudi-moi-original read in full; authenticity authenticated, strength moderate; origin saudi-moi-spa-1001; stored copy
src-flydubai-updates read in full; authenticity authenticated, strength moderate; origin flydubai-statement-1, flydubai-statement-2, flydubai-statement-4; stored copy
src-gcaa-emirates247 read in full; authenticity not checked; origin gcaa-statement-1002; stored copy
src-khaleej-timeline read in full; authenticity not applicable (a news report)
src-aljazeera-saudi read in full; authenticity not applicable (a news report)
src-cnn-live read in full; authenticity not applicable (a news report); origin cnn-live-0930-captain-entry, cnn-live-0930-first-entry, cnn-live-0930-omani-entry, cnn-live-0930-terror-entry, saudi-moi-spa-1001
primary text read
 Copies held in the repository: 3 of 6 cited source(s); for the others the reader must retrieve the record from its address, and a page can change.
Would change if: the Arabic original or a later Saudi statement changing the wording; a medical or court record contradicting the injuries
`````

The same card as built (HTML; the anchor text is cut for this excerpt):

`````html
<div class="claim" id="fz1073-both-pilots-injured"><p><b>fz1073-both-pilots-injured</b> <span class="pill s-established">established</span> <span class="small">reported</span></p><p>The Saudi Interior Ministry&#x27;s own statement (SPA, English) says the captain and co-pilot were transferred to a local hospital, that &quot;an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals&quot;, and that both pilots left Saudi Arabia for Abu Dhabi on 1 October &quot;accompanied by the UAE security team&quot;; the airline&#x27;s CEO says the captain has returned to the UAE after medical clearance.</p><div class="kv"><b>Our rating</b><span>confidence high; evidence 4 of 5; public belief 5 of 5; evidence class primary_text; source checked: primary</span><b>Anchor</b><span>official-statement: Saudi Press Agency, 1 Oct 2026 (English; raw HTML read; stored in sources/spa-moi-2026-10-01.txt): &quot;The captain and co-pilot were transferred to a local hospital for medical evaluation and treatment.&quot; &quot;Preliminary investigati [anchor text cut for this excerpt]</span></div><p class="small" style="margin-bottom:0"><b>Cited sources (6).</b> Origin recorded (media record) for 4 of 6; none is inferred. One origin is counted once however many outlets copy it, and a live blog can hold several.</p><ul class="l tight"><li><a href="#src-saudi-moi-original">src-saudi-moi-original</a> <span class="small">read in full; authenticity authenticated, strength moderate; origin saudi-moi-spa-1001; stored copy</span></li><li><a href="#src-flydubai-updates">src-flydubai-updates</a> <span class="small">read in full; authenticity authenticated, strength moderate; origin flydubai-statement-1, flydubai-statement-2, flydubai-statement-4; stored copy</span></li><li><a href="#src-gcaa-emirates247">src-gcaa-emirates247</a> <span class="small">read in full; authenticity not checked; origin gcaa-statement-1002; stored copy</span></li><li><a href="#src-khaleej-timeline">src-khaleej-timeline</a> <span class="small">read in full; authenticity not applicable (a news report)</span></li><li><a href="#src-aljazeera-saudi">src-aljazeera-saudi</a> <span class="small">read in full; authenticity not applicable (a news report)</span></li><li><a href="#src-cnn-live">src-cnn-live</a> <span class="small">read in full; authenticity not applicable (a news report); origin cnn-live-0930-captain-entry, cnn-live-0930-first-entry, cnn-live-0930-omani-entry, cnn-live-0930-terror-entry, saudi-moi-spa-1001</span></li></ul><p><span class="flag ok">primary text read</span></p><p class="small"> Copies held in the repository: 3 of 6 cited source(s); for the others the reader must retrieve the record from its address, and a page can change.</p><p class="small"><b>Would change if:</b> the Arabic original or a later Saudi statement changing the wording; a medical or court record contradicting the injuries</p></div>
`````

One source-register entry, as generated (note the fields the dig page does not print: origin, hash of the stored copy, publication status, provenance, tests, gaps, next step, who cites it):

`````text
src-saudi-moi-original Saudi Press Agency, Interior Ministry Issues Statement Detailing Flydubai Emergency Landing in Tabuk Following Cockpit Altercation (dateline Riyadh, 1 October 2026) - English text
Addresshttps://www.spa.gov.sa/en/w2691027Kind of documentprimary_text (a government statement carried by the state news agency)Accessread in full (opened here)Authenticityauthenticated, strength moderateOriginsaudi-moi-spa-1001 (copies of one origin count once; recorded only where a media record exists)Retrieved or checked2026-10-02 (date of the authenticity check)Stored copysources/spa-moi-2026-10-01.txt; sha256 2dc6845ae9005f62aad6be2e445129fe9f80ea0380eb9777283d74313c9f0807 (computed at build from the stored file)Publication statusnot looked up (silence here does not mean the source is free of a retraction or correction)ProvenanceServed over HTTPS from spa.gov.sa, the Saudi Press Agency's own domain. The item attributes the statement to 'an official source at the Ministry of Interior'. Text stored in sources/spa-moi-2026-10-01.txt (from the page's og:description).Tests runDomain check: the state news agency's own site [read]; Content match: the facts (9:45 a.m. landing, 5:40 p.m. replacement flight, injuries to both, both pilots to Abu Dhabi on 1 October with the UAE security team) are reported by Al Jazeera, CNN, Khaleej Times and The National, though in different English renderings [read]; Wording check: the headline and body use 'altercation' and 'assaulted'; other outlets' renderings ('revealed an assault on the captain by the co-pilot', 'the pilot was assaulted by his co-pilot') differ, so they are translations or paraphrases of an Arabic original that was not seen [read]Tested byStratah session, 2026-10-02 (not an independent review; the statement is a party's own)GapsThe Arabic original and the release hour were not seen; the item body ends with the stamp '21:31 Local Time 18:31 GMT', probably the agency's dispatch stamp (an inference; it was identical in fetches about 30 minutes apart; not confirmed). The page's own embedded field published_at 1790879513 (1 Oct 2026 18:31:53 UTC) matches it; that is the page's publication field, not the agency's release record.; No time zone is given for the times in the text; Saudi time (UTC+3) is assumed.; Not archived by an independent capture.Next stepRead the Arabic SPA item and note its release time; obtain an independent web-archive capture.Cited byfz1073-diverted-tabuk, fz1073-flight-times, fz1073-both-pilots-injured, fz1073-captain-wounds, fz1073-israeli-attack-account, fz1073-landing-time, fz1073-persons-on-board, fz1073-replacement-flight-timing, fz1073-copilot-custody-unnamed, fz1073-israel-in-investigation, fz1073-event-simulated, fz1073-reports-inconsistent, fz1073-original-statements-gap
`````

And what it will not let the reader mistake: the same document lists 18 searched gaps, 10 established or refuted claims not read at primary level, 14 sources listed but not read and 2 read with authenticity unchecked:

`````text
Open questions: searched gaps (18)
Established or refuted, but not read at primary level (10)
Sources listed but not read (14)
Read, but authenticity not checked (2)
Open items recorded by the independent reviewer
`````

and the head of the "Primary records to obtain" table:

`````text
8. Primary records to obtain
Records a reader relying on a claim would need to obtain: sources listed but not read here, and primary-class sources with no stored copy. This lists records, not people.
Source | Title | Access | Claims resting on it | 
src-flightaware-history | FlightAware, FZ1073 (FDB1073) flight history, row for 30-Sep-2026 | read in part (list page only; the per-flight track log returned HTTP 429) | fz1073-diverted-tabuk, fz1073-flight-times, fz1073-event-simulated, fz1073-reports-inconsistent, fz1073-raw-tracks-gap | 
src-bloomberg | Bloomberg, FlyDubai Hijacker Pilot Was From Oman, Israel's Netanyahu Says (1 Oct 2026) | not read | no claim anchor lists it | 
src-axios | Axios, Netanyahu: FlyDubai Omani co-pilot went through religious Islamic radicalization (1 Oct 2026) | not read | no claim anchor lists it | 
src-flightradar24 | Flightradar24, FZ1073 data and posts on X | not read | fz1073-raw-tracks-gap | 
src-wam-original | WAM (UAE news agency) releases of 1 and 2 Oct 2026 | not read | fz1073-original-statements-gap | 
src-gov-il-entry | Israel Population and Immigration Authority, entry rules by nationality | not read | fz1073-legal-texts-gap | 
`````

Fingerprints of the files used (so a later reader can show which version this was):

`````text
File | sha256 | 
claims.yaml | 6ceaad3964e749f4d365fcba83bc732906443484e9f38a7d4249363ec6b6e15d | 
sources/MANIFEST.yaml | 7947f9fe34533b56098047c92675974ff4776489672feb5b932476fac163fd8e | 
timeline.yaml | 89804aece7adae83ea3342235f9103341debfbd9a6061277617c794b4299c958 | 
transmission.yaml | 723d7653497d9c99949381f43de48c27b197570c9c7c1c60b3a703ed73a4b48b | 
log.yaml | 54639269f8cd042eb64475a28ae2c6cd4d196cf67ff81be035f9024c4699f03b | 
media.yaml | 87ee2eaaa473ce37ae8693b42b4014ef45208b25872c18fd9770447abecd31cf | 
story.yaml | ef91e5989d4ee56581fbdd69b44f1ae2e3c98bf519be0d04b7ff14d47b77583b | 
Content: CC BY 4.0; reuse with credit to "Stratah (stratah.org)" and a note of any changes. Built 2026-10-03 from YAML in the repository. Source · Challenge a finding
`````

### 3.2 Layer 2: `media.yaml` (new optional file)

Only for what 1.4 shows cannot be carried by timeline events. A record of reports, never evidence.

Format and rules MR1 to MR7 are in the SCHEMA text (3.5). Worked example for FZ1073: the header, the points reports are compared on (`topics`), and three of the 42 records (the first CNN live-blog entry, with an in-place edit seen; Al Jazeera, whose URL keeps its first headline after a rewrite; CBS, retitled):

`````yaml
# media.yaml: who reported what, when, and how it changed (format: build/SCHEMA.md, rules MR1 to MR7).
# WORKED EXAMPLE for flydubai-fz1073: a subset of the researcher's media timeline of 2026-10-02 (scratchpad fz1073/media-timeline.md), converted to UTC by the
# researcher. Not a reviewed record. Confers no weight on any claim: a report is not evidence of what it reports, and copies of one origin count once.
subject: flydubai-fz1073
confers_weight: false
observed: 2026-10-02

topics:
  - {id: t-event-kind, label: "What kind of event: hijacking, altercation, assault, attack", claims: [fz1073-diverted-tabuk, fz1073-both-pilots-injured], resolution: open}
  - {id: t-copilot-nationality, label: "The co-pilot's nationality", claims: [fz1073-israel-says-omani, fz1073-omani-nationality-unconfirmed], resolution: open}
  - {id: t-captain-nationality, label: "The captain's nationality", claims: [fz1073-captain-wounds], resolution: resolved, resolved_by: fz1073-captain-wounds}
  - {id: t-landing-time, label: "When the aircraft landed at Tabuk", claims: [fz1073-landing-time], resolution: open}
  - {id: t-takeoff-clock, label: "CNN's departure time and its time-zone labels", claims: [fz1073-flight-times], resolution: corrected}
  - {id: t-descent-size, label: "How far and how fast the aircraft descended", claims: [fz1073-descent-magnitude], resolution: open}
  - {id: t-weapon, label: "What weapon was used", claims: [fz1073-weapon-not-established], resolution: open}
  - {id: t-extra-pilots, label: "Who the additional pilots were and who took the controls", claims: [fz1073-crew-details], resolution: open}
  - {id: t-pilot-rule, label: "Whether a rule bars Omani pilots from the Israel route", claims: [fz1073-omani-barred-rule], resolution: open}
  - {id: t-motive, label: "Motive and accusations by officials", claims: [fz1073-motive-statements, fz1073-motive-not-established], resolution: open}
  - {id: t-staged-claim, label: "The claim that the event was staged", claims: [fz1073-event-simulated], resolution: open}
  - {id: t-headcount, label: "How many people were aboard", claims: [fz1073-persons-on-board], resolution: open}

reports:
  - {id: m-001, outlet: "Times of Israel (live entry)", url: "https://www.timesofisrael.com/liveblog_entry/hijacking-ruled-out-as-flydubai-flight-to-tel-aviv-lands-at-saudi-airport/", kind: live_entry, access: summary, published: "2026-09-30T06:57:00Z", basis: displayed, origin: toi-live-0930-hijack-ruled-out, said_by: "Israeli security sources (unnamed)", says: [{topic: t-event-kind, value: "hijacking ruled out; altercation between the pilots"}], note: "Displayed 9:57 am, no zone; 06:57 matches Khaleej Times 10:57 UAE. Read as a tool summary only; no correction note confirmed either way."}
  - {id: m-002, source: src-flydubai-updates, kind: statement, access: read, published: "2026-09-30T07:30:00Z", basis: relayed, origin: flydubai-statement-1, said_by: "flydubai", says: [{topic: t-event-kind, value: "an incident while en route; landed safely at Tabuk"}], note: "Time from Khaleej Times (11:30 UAE). The airline's page carries no timestamps."}
  - {id: m-003, source: src-cnn-live, kind: live_entry, access: read, published: "2026-09-30T07:54:35Z", basis: metadata, origin: cnn-live-0930-first-entry, said_by: "unnamed sources; flight tracking data reviewed by CNN", says: [{topic: t-event-kind, value: "violent incident between two pilots"}, {topic: t-descent-size, value: "17,400 ft in under two minutes"}], changed: [{observed: "2026-09-30T10:49:44Z", what: "entry edited; what changed is not visible", how_known: "per-entry dateModified in the page"}]}
  - {id: m-004, outlet: "Al Jazeera English", url: "https://www.aljazeera.com/news/2026/9/30/flydubai-flight-to-israel-diverted-to-saudi-arabia-after-emergency-alert", kind: original, access: read, published: "2026-09-30T08:00:10Z", basis: metadata, origin: aj-0930-staff-afp-reuters, said_by: "Al Jazeera Staff, AFP, Reuters; Flightradar24", says: [{topic: t-descent-size, value: "34,000 ft at 05:21 to under 17,000 ft at 05:22", version: unknown}, {topic: t-event-kind, value: "one pilot stabbed the other (Israel's Prime Minister)", version: unknown}], changed: [{observed: "2026-09-30T19:49:48Z", what: "page rewritten; the URL keeps the first headline ('diverted to Saudi Arabia after emergency alert'), the current headline is about a pilot stabbing", how_known: "URL slug against current headline; page dateModified"}]}
  - {id: m-005, outlet: "CBS News", url: "https://www.cbsnews.com/news/tel-aviv-israel-flydubai-flight-saudi-arabia-diverted-pilots/", kind: original, access: read, published: "2026-09-30T07:59:00Z", basis: metadata, origin: cbs-0930-first-story, said_by: "CBS reporting; Israeli officials; Israel's Prime Minister", says: [{topic: t-event-kind, value: "current headline: co-pilot stabbed captain, tried to crash (Netanyahu says)", version: rewritten}], changed: [{observed: "2026-10-01T15:38:00Z", what: "retitled; the current headline describes events of 1 October, so the 07:59 stamp belongs to the first version", how_known: "headline against datePublished and dateModified"}]}
`````

The full file is Appendix F. It is a conversion of the session's research note on the media timeline (`scratchpad/fz1073/media-timeline.md`, times converted to UTC there) into 42 records and 12 topics. Spot-checked against that note (CNN 07:54:35, Al Jazeera 08:00:10, Euronews 08:16:18, NBC 08:56:44, Greek City Times 09:14:07). It is an illustration, not a reviewed record; reviewing it is the author's and the independent reviewer's job if this is adopted. 23 of its 42 records have no media event on the existing timeline at the same UTC time (matched by exact time; they include statements by the airline and the UAE attorney general, wire and fact-check items), because the timeline was drawn to show the event, not the coverage.

Generated from it (first appearance per point; the table is computed, not authored):

`````text
Where each point first appeared
Point | First seen (UTC) | First report and who it cites | Reports / origins | Status | 
What kind of event: hijacking, altercation, assault, attack | 2026-09-30 06:57Z | Times of Israel (live entry)
said by: Israeli security sources (unnamed) | 15 / 14 | open | 
The co-pilot's nationality | 2026-09-30 09:45Z | Walla (via AeroTime live entry)
said by: an Israeli security source (unnamed)
An earlier page (MiGFlug, 08:18Z) carries this point but was rewritten in place, so its first wording cannot be recovered. | 11 / 11 | open | 
The captain's nationality | 2026-09-30 09:14:07Z | Greek City Times
said by: Israeli media (Channel 7, Channel 12); an Israeli official to Reuters
An earlier page (MiGFlug, 08:18Z) carries this point but was rewritten in place, so its first wording cannot be recovered. | 3 / 3 | resolved | 
When the aircraft landed at Tabuk | 2026-10-01 18:31Z | Saudi Press Agency, Interior Ministry Issues Statement Detailing …
said by: Saudi Ministry of Interior (via the Saudi Press Agency)
An earlier page (CNN, What happened inside the Flydubai flight to …, 01:51Z) carries this point but was rewritten in place, so its first wording cannot be recovered. | 2 / 2 | open | 
CNN's departure time and its time-zone labels | 2026-10-01 01:51:23Z | CNN, What happened inside the Flydubai flight to Israel? What we know …
said by: Israel's Prime Minister, Israeli officials, the Saudi interior ministry, passengers
The only reports carrying it were rewritten in place: first wording not recoverable. | 1 / 1 | corrected | 
`````

Reading that table: "first seen" is the earliest report in *the record* that carries the point in its first wording; where the earliest page was rewritten in place the table says its first wording cannot be recovered. It is only as complete as the record, and says so ("Earlier items may exist in sources we could not open"). The "Reports / origins" column counts reports and distinct origins, so a wire text copied by ten outlets is one origin.

In-place changes the dossier lists (only what a URL slug against a current headline, a visible update note or page metadata shows):

`````text
Changes made to reports after publication (10 seen)
Only changes visible in the URL, a visible update note or page metadata are listed. Archived earlier versions could not be read, so what changed inside a page is often not known.
2026-09-30 10:49:44Z CNN live blog, October 1, 2026: Pilot suspected of Flydubai attack …: entry edited; what changed is not visible
2026-09-30 19:49:48Z Al Jazeera English: page rewritten; the URL keeps the first headline ('diverted to Saudi Arabia after emergency alert'), the current headline is about a pilot stabbing
2026-10-01 01:42Z NBC News: updated 9:42 PM EDT on 30 September
2026-10-01 07:34:44Z Euronews: headline changed from an 'alleged dispute between pilots' to 'Israel says pilot tried to crash flydubai plane during cockpit fight'
2026-10-01 15:38Z CBS News: retitled; the current headline describes events of 1 October, so the 07:59 stamp belongs to the first version
2026-10-01 18:50:12Z Arab News: modified
2026-10-01 21:54:39Z ABC News Verify, Fake news spreading online following Tel Aviv-bound …: updated; the page title (og:title) now differs from the on-page headline
2026-10-02 13:23:20Z CBS News, What we're learning about the FlyDubai co-pilot who …: last edit
2026-10-02 20:22:07Z MiGFlug: page carries 'Update, 30 September 2026, afternoon: The picture has changed sharply since this story was first published'; the nationality and weapon lines may belong to the update
2026-10-02 20:43:01Z CNN, What happened inside the Flydubai flight to Israel? What we know …: last edit; the 10:05 p.m. ET figure and the 9:54 a.m. touchdown were still on the page
How a claim spread: How the claim that the FZ1073 incident was staged by Israel spread
About flydubai-fz1073:fz1073-event-simulated. Spread is adoption, never evidence of the claim; where a step is dated by day only, the order inside the day is not known.
2026-09-30 (day) origin: A firs
`````

The dig's own transmission chains (how "staged" and fake items spread) follow in the same section, marked "Spread is adoption, never evidence of the claim". Nothing in `media.yaml` or the transmission record enters a claim's weight (MR1, X1, X3).

### 3.3 Layer 3: `story.yaml` (new optional file) and the story page

A story is the one part that cannot be generated: someone has to write the sentences. What can be generated, and checked, is everything about them.

**Format** (SCHEMA text in 3.5): `updates[]`, oldest first and append-only, each with `at` (UTC), a title, the headline as it stood then, a snapshot `claims_at_update`, and paragraphs of sentences. A sentence has an `id`, `text`, a `mode`, and `claims` (one or more claim ids of this subject; each can carry its own mode). The three modes:

- `attributes`: reports who said it ("Israel's Prime Minister said on 1 October that ..."). Needs `attributed_to`, which the text must contain. Allowed on any claim except a searched gap.
- `open`: says plainly something is not known or not confirmed. Allowed on any claim; required for a searched gap.
- `states`: the project speaks in its own voice. Allowed only when the claim is a project **judgment** (`statement_kind: judgment`), established or refuted, at moderate or high confidence, with `anchor_checked: primary`. A claim that records what a source says (`statement_kind: reported`) can never be `states`. On a refuted claim the sentence must deny the claim's `refutes_target` (`denies_target: true`), and the page prints that target beside the sentence.

A sentence that replaces an earlier one carries `supersedes`, `change` (updated, narrowed, corrected, withdrawn) and `why`. The old sentence is never edited or removed.

**Worked example, FZ1073.** The names register and the last of four updates (full file, Appendix E). The first three updates are the story as it might have run on 2 October, including a real correction (CNN's departure time, L-17). The fourth carries two real corrections from the log (L-26 items 2 and 3):

`````yaml
# story.yaml: the running story for a News Review entry (format: build/SCHEMA.md, rules SR1 to SR12).
# WORKED EXAMPLE for flydubai-fz1073, written for the proposal. Update times are illustrative (the project log carries dates, not times);
# the correction in u-003 reproduces a real one (log L-03(a), corrected in L-17); u-004 reproduces L-26 items 2 and 3 (the Saudi text read at source). Not published text.
subject: flydubai-fz1073

names:                       # SR9: every person, place, organisation and nationality the story uses. No person is named in this story.
  people: []
  places: [Dubai, Tel Aviv, Tabuk, Saudi Arabia, Israel, Oman]
  organisations: [Flydubai, UAE, AirNav Radar, CNN, Al Jazeera, Saudi]
  demonyms: [Israeli, Omani, Saudi, English]
  other: [FZ1073, UTC, ET, GMT, ADS-B, Attorney-General, Prime Minister, October, September, Islamist]   # Islamist: a word inside a quotation

updates:
`````
`````yaml
  - id: u-004
    at: "2026-10-02T21:00:00Z"
    title: "Saudi statement read at source; landing time and head count unsettled"
    headline:
      id: h-004
      text: "Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; motive, weapon, landing open"
      mode: attributes
      attributed_to: "Saudi ministry"
      claims: [fz1073-both-pilots-injured, {id: fz1073-motive-not-established, mode: open}, {id: fz1073-weapon-not-established, mode: open}, {id: fz1073-landing-time, mode: open}]
    claims_at_update:
      fz1073-both-pilots-injured: established/high
      fz1073-landing-time: contested/low
      fz1073-persons-on-board: contested/low
      fz1073-motive-not-established: searched_gap/low
      fz1073-weapon-not-established: searched_gap/low
      fz1073-uae-investigation: established/high
      fz1073-event-simulated: searched_gap/low
    paragraphs:
      - sentences:
          - id: s-013
            supersedes: s-003
            change: corrected
            why: "The earlier sentence quoted the Saudi statement as rendered by CNN and Al Jazeera ('revealed an assault ...'). The agency's own English, read on 2 October, says 'an altercation occurred in which the co-pilot assaulted the captain' (log L-26, item 2)."
            mode: attributes
            attributed_to: "The Saudi interior ministry"
            text: 'The Saudi interior ministry''s own English text says its preliminary investigations "revealed that an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals"; it does not say how, with what, or why.'
            claims: [fz1073-both-pilots-injured, {id: fz1073-weapon-not-established, mode: open}]
          - id: s-014
            supersedes: s-009
            change: corrected
            why: "The earlier sentence gave 06:45 UTC as the Saudi ministry's landing time. That is a rendering by Al Jazeera; the agency's text says '9:45 a.m.' with no time zone, so 06:45 UTC assumes Saudi time, UTC+3 (log L-26, item 3)."
            mode: open
            text: "The Saudi interior ministry's text says the aircraft landed at 9:45 a.m. and gives no time zone; AirNav Radar and Al Jazeera give about 06:58 UTC, and the landing time is not settled."
            claims: [fz1073-landing-time]
          - id: s-015
            mode: open
            text: "The number of people aboard is not settled: the Saudi interior ministry's text gives 174 passengers and an eight-member crew, and the airline's chief executive says 172 passengers and crew."
            claims: [fz1073-persons-on-board]
      - sentences:
          - id: s-016
            mode: attributes
            attributed_to: "The UAE Attorney-General"
            text: 'The UAE Attorney-General ordered an investigation on 1 October into the circumstances and causes, including "any possible connection to terrorist activity or intent, and whether it involved prior planning or direction".'
            claims: [fz1073-uae-investigation]
          - id: s-017
            mode: open
            text: "No evidence has been found that anyone simulated the event, but the records read are statements and reports, not raw tracker, recorder or medical data, so the question stays open."
            claims: [fz1073-event-simulated]
`````

Update times are illustrative: the log carries dates, not times, and the story format needs times. If this is adopted, an update's time is the time the author commits it; the dig log still carries the date.

**What the page shows.** Head, banner and "not known yet" first (a reader landing on the page sees the position and what is unsettled before anything else):

`````text
Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; motive, weapon, landing openNews Review · story · live
Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; motive, weapon, landing open
Last updated 2 Oct 2026 21:00 UTC · 4 updates · 17 sentences, each tied to a claim · 3 correction(s) · Evidence dossier
How to read this. This is a running story, written from the claims in the News Review entry. Every sentence names the claim it rests on and shows how sure the claim is. A sentence that says what someone said is not a finding; a sentence that says something is not known is not a hint. When a fact changes, the old sentence stays on the page, marked, and a dated update replaces it.
What is not known yet
Whether the co-pilot is an Omani national, and whether he holds another nationality, is not confirmed by any authority that is not Israeli. [searched gap, low]
As of 2 October no investigation finding, recorder result, preliminary report, charge or court record has been published. [searched gap, low]
No investigating authority has established a motive, an affiliation or any direction by a third party. [searched gap, low]
How far and how fast the aircraft descended is not settled: reports give figures from 14,000 ft in under 30 seconds to 17,400 ft in just under two minutes. [searched gap, low]
The Saudi interior ministry's text says the aircraft landed at 9:45 a.m. and gives no time zone; AirNav Radar and Al Jazeera give about 06:58 UTC, and the landing time is not settled. [contested, low]
The number of people aboard is not settled: the Saudi interior ministry's text gives 174 passengers and an eight-member crew, and the airline's chief executive says 172 passengers and crew. [contested, low]
No evidence has been found that anyone simulated the event, but the records read are statements and reports, not raw tracker, recorder or medical data, so the question stays open. [searched gap, low]
`````

The story so far keeps every sentence. A replaced sentence stays, struck through, with a "changed" mark, the date, the reason and a link to its replacement. Raw HTML of the first correction, as built:

`````html
<p class="sent chg" id="s-003"><del>The Saudi interior ministry says its preliminary investigations &quot;revealed an assault on the captain by the co-pilot, resulting in various injuries to both&quot;.</del> <span class="flag">changed: corrected</span> <span class="small">2 Oct 2026 21:00 UTC: The earlier sentence quoted the Saudi statement as rendered by CNN and Al Jazeera (&#x27;revealed an assault ...&#x27;). The agency&#x27;s own English, read on 2 October, says &#x27;an altercation occurred in which the co-pilot assaulted the captain&#x27; (log L-26, item 2). <a href="#s-013">See the new sentence</a>.</span></p>
`````

The correction log on the story page: every `corrected` or `withdrawn` sentence, then the dig's own log entries that open with CORRECTION or REDACTION, whole up to 300 characters with a link to the full entry (not cut by the regular expression of 1.2):

`````text
Corrections
Visible and permanent. A correction is a new sentence; the old one stays on the page, struck through, with the reason. Corrections to the underlying record are in the project log.
2 Oct 2026 18:30 UTC · corrected: The earlier sentence called CNN's 6:05 a.m. a different time from the trackers'. CNN's other times are on the UTC+3 clock, so 6:05 a.m. is 03:05 UTC; only CNN's ET figure is wrong (log L-17).
Replaces s-011: CNN gave the departure as 6:05 a.m. local time, which differs from the trackers' 03:05 UTC.
2 Oct 2026 21:00 UTC · corrected: The earlier sentence quoted the Saudi statement as rendered by CNN and Al Jazeera ('revealed an assault ...'). The agency's own English, read on 2 October, says 'an altercation occurred in which the co-pilot assaulted the captain' (log L-26, item 2).
Replaces s-003: The Saudi interior ministry says its preliminary investigations "revealed an assault on the captain by the co-pilot, resulting in various injuries to both".
2 Oct 2026 21:00 UTC · corrected: The earlier sentence gave 06:45 UTC as the Saudi ministry's landing time. That is a rendering by Al Jazeera; the agency's text says '9:45 a.m.' with no time zone, so 06:45 UTC assumes Saudi time, UTC+3 (log L-26, item 3).
Replaces s-009: The Saudi interior ministry and Tabuk airport say the aircraft landed at 06:45 UTC (9:45 a.m. local); AirNav Radar's blog says it landed safely at Tabuk, with its last ADS-B message at about 06:58 UTC.
2026-10-02 · log L-17 (correction): CORRECTIONS TO EARLIER ENTRIES AND TO THE TIMELINE (new entry; the earlier text stays). (1) L-03(a) said CNN's departure time ('6:05 a.m. local time (10:05 p.m. ET)') 'appears to be an error or a mix of time zones'. Re-read: CNN's other times (distress call 8:31, touchdown 9:54) are on UTC+3; 6:05 … Full entry
2026-10-02 · log L-18 (correction): CORRECTIONS TO L-15 (new entry). (1) Masks: L-15 said oxygen masks drop when cabin pressure altitude rises above about 14,000 ft and 'not when the aircraft descends'. That is general knowledge and was not taken from a source read in this dig. The Conversation (read) says early passenger accounts … Full entry
2026-10-02 · log L-24 (redaction): REDACTION (owner decision, 2026-10-02; the one exception to the append-only rule, made openly). Entry L-15 and the review record named a private passenger whom CNN quoted as a witness. Our guardrail (docs/NEWS_REVIEW.md) is not to name private individuals who authorities have not named, and the log … Full entry
2026-10-02 · log L-26 (correction): CORRECTIONS OF EARLIER CONTENT (new entry; earlier entries stay)
`````

The evidence ledger (one row per sentence and cited claim) is at the foot of the page. It shows the sentence, its mode, the claim, the claim's state and confidence, source checked, evidence class, and the sources the claim's anchor lists, linked into the dossier when the dossier is public. A superseded sentence keeps its row, marked "superseded by". Rows show the claim's *current* state; the state when the sentence was written is `claims_at_update`, and a difference raises the "claim has changed since" flag (SR6).

**Live-event guardrails, by mechanism** (docs/NEWS_REVIEW.md):

| Guardrail | Mechanism |
|---|---|
| 1. Do not name a suspect or a private individual; never speculate about religion, ethnicity or beliefs | SR9: every capitalised word of a sentence must be in the story's `names` register. A person needs `role`, `named_by` (a manifest source that is an authority) and at least two `also_named_by`, and `private: true` is an error. The FZ1073 story names no person. The register is a tripwire, not a classifier (9, risk R2) |
| 2. An accusation is not a finding | An accused-of sentence is `attributes` with `accusation: true`, which the page tags "accusation, not a finding". `accusation` on any other mode is an error (SR3). FZ1073 `s-008` ("Israel's Prime Minister said on 1 October that the co-pilot 'underwent Islamist radical indoctrination'") is the example |
| 3. A discrepancy is not evidence of fabrication; "staged" is a claim to test | SR7 blocks loaded words (terror, jihadist, radical, hijack, suicide, false flag, staged, fabricated, manufactured) in our own voice. A sentence on a claim that is a searched gap can only be `open`. The simulated-event question appears as "No evidence has been found that anyone simulated the event, but the records read are statements and reports ... so the question stays open" (`s-017`, mode `open`) |
| 4. Early reporting is often wrong; log every fact with source and time; later changes are new entries | `at` is UTC and must not precede the update above (SR2); updates are append-only (SR11); a change is a new sentence that supersedes (SR5), with a visible "changed" mark |
| 5. Wire copies that copy one another count once | The story states no count of outlets, reports or posts (SR7); the dossier counts *origins*, not reports, and the media record carries `origin` and `derives_from` (MR4) |

**How the story avoids hype.** Headline 70 to 95 characters (SR8, same as the dig headline), no percentage anywhere (SR7, SCHEMA N23), no count of outlets, no hype word (shocking, horrifying, bombshell, heroic, miracle and the like) outside a quotation, a loaded word only inside a quotation and attributed. The headline cites claims and uses the same modes: FZ1073's latest headline ("Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; motive, weapon, landing open", 93 characters) attributes the one finding to the ministry and calls the rest open.

**How it stays honest when facts change.** The author appends a new update; the old text stays; `claims_at_update` snapshots every cited claim as it stood. If a claim moves (for example `fz1073-both-pilots-injured` went from established/moderate to established/high after the Saudi text was read at source), a sentence written against the old state is flagged on the page ("claim has changed since") and by an SR6 warning until a new update re-affirms or supersedes it. In the first run on the current tip, the earlier prototype's story drew exactly that warning for `s-003`; u-004 answers it.

**How the "academic rigor" standards map** to what is on the page: every sentence has a claim id (SR1); the ledger shows state, confidence, `anchor_checked` and evidence class and links the sources (3.3); the dossier gives each source's origin, access (read or not), independence, authenticity and strength, date checked, stored copy and hash, and publication status (3.1); the story page cannot say more than the claim (SR3); corrections are visible and permanent (SR5, SR11, correction log); what is open is stated at the top (the "not known yet" list is every unsuperseded `open` sentence). The independent reviewer controls publication of each update (SR12, below).

### 3.4 Print, export and PDF: static pages, no data downloads

- **Dossier as a static page.** `dossier_html()` returns one HTML string; `build_site.py` writes it to `/digs/<slug>/dossier/index.html` (`dossier: public`, `<meta name="robots" content="noindex">`, not in the sitemap) or to `private/dossier/<slug>/index.html` (`dossier: private`). `private/` is in `.gitignore` (`git check-ignore -v private/dossier/x/index.html` confirms) and is outside the `site/` folder `deploy.yml` uploads, so it is never deployed. The owner opens the private page locally or uploads it themselves.
- **PDF-friendly CSS.** `PRINT_CSS` (in `dossier.py`, Appendix B) sets `@page` A4 with margins and a footer "Evidence dossier, page N of M", hides navigation and footer in print, removes the page background, keeps table rows and source blocks from splitting, repeats table headers, starts the major sections on a new page, and prints the address of external links after the link text. A browser's Print to PDF gives a case file; a reader can do it, and the build writes no PDF (D3).
- **The PDF I made is for checking only.** `gen.py --pdf` uses `weasyprint` (installed in the scratchpad; not a dependency of the build) to render the dossier at 132 pages, A4. I viewed page 1 and the statements-against-material table (page 41, rechecked after the fix: one cell, "Statement", still wraps mid-word) to catch layout faults: the first version had columns a few characters wide, which led to the `colgroup` widths in the code. It is not published or kept in the repository.
- **No data file is copied or linked.** `dossier.py` links only to anchors inside the page and to third-party addresses cited by our sources. The test `test_no_data_download_and_no_legal_conclusion_words` fails the build if the dossier or story links a `.yaml`, `.json`, `.csv` or `.pdf` of ours.
- **Names in addresses.** One manifest source's address (an Emirates 24|7 page, `src-gcaa-emirates247`) contains the captain's name in its URL path. The project's naming policy (log L-30: victims are not named) says the name remains only "where it cannot be removed: URL slugs". The existing published dig page and the Atlas already carry it. For the dossier D6 adds one optional manifest field, `address_withheld: <reason>`: a public dossier prints the host and the reason instead of the path; a private dossier prints the full address, because a lawyer needs it to retrieve the page. The proposal does not change any published page; the FZ1073 author would add the one line (diff in 3.6).

### 3.5 The SCHEMA text

Exactly what would be added to `build/SCHEMA.md` (a fenced diff against `051778c`):

`````diff
diff --git a/build/SCHEMA.md b/build/SCHEMA.md
index 9b9339c..2c42f09 100644
--- a/build/SCHEMA.md
+++ b/build/SCHEMA.md
@@ -368,3 +368,89 @@ CORRECTION in the log entry (`build_site.py` picks entries by that word); if the
 finding, follow the gate's revision loop (new log entry, revision round, independent check,
 visible correction). The validator does not enforce this paragraph. Recording a retraction turns the validator red until the claims carry
 `flagged_sources` and `source_notices` (intended).
+
+## Stories, media records and the evidence dossier (added under docs/proposals/news-story-and-dossier-formats.md)
+
+Three things for a News Review entry (`build/news.yaml`), all optional. A dig without `story.yaml` and `media.yaml` is unchanged, and no claim state, weight or confidence is touched. **Nothing here adds a data download**: pages are static HTML, and no new page links to a `.yaml`, `.json`, `.csv` or `.pdf` file of ours (addresses of cited third-party sources are shown as given).
+
+### The evidence dossier (generated, no new data)
+`build/tools/dossier.py` renders a printable page from the files a dig already has (`claims.yaml`, `sources/MANIFEST.yaml`, `timeline.yaml`, `transmission.yaml`, `log.yaml`, `review.yaml`, and the publication-status fields of docs/proposals/publication-status.md) and, when present, `media.yaml`. It adds no fact and no text of its own beyond fixed labels. Sections, in order: position; contents; fact register (per claim: statement, state, confidence, source checked, anchor, each cited source with access, authenticity, origin and stored-copy status, whether the primary record is still needed, what would change it); statements against material (timeline); conflicts; media timeline (with the dig's own transmission record); what could not be verified; primary records to obtain; source register (address, kind, access read or not, authenticity, publication status, tests, gaps, date checked, stored copy and its sha256 computed at build, which claims cite it); the log in full; file fingerprints (sha256 of each data file used).
+- **D1** The dossier states no legal conclusion and no liability, intent or guilt. Its fixed labels contain no word from a legal-conclusion list (tested). An accusation is shown only as the claim's own text, attributed.
+- **D2** It names no suspect and no private individual. It prints what the claim files print; the entry's guardrails (docs/NEWS_REVIEW.md) apply to those files first.
+- **D3** It is a page, not a file: it links to no data file of ours, and the build writes no PDF. Print and "save as PDF" are the reader's browser's job (print stylesheet in `dossier.py`).
+- **D4** Our ratings are shown as ratings ("confidence", "evidence 4 of 5"), never as a standard of proof, and the page says so.
+- **D5** `news.yaml` sets `dossier: public` (written to `/digs/<slug>/dossier/`, `noindex`, not in the sitemap) or `dossier: private` (written to `private/dossier/<slug>/`, which is git-ignored and never deployed). Absent: not built. The owner chooses; the build never chooses `public` itself.
+- **D6** A manifest entry may carry `address_withheld: <reason>` (a non-empty string; the entry needs a `url`). A public dossier then prints the host and the reason instead of the path (for an address whose path carries a name the project's naming policy does not print); a private dossier prints the full address. Conformance checks the reason is present. It is the only new field on an existing file.
+- A source is flagged "primary record needed" for a claim when the claim's `anchor_checked` is not `primary`, a cited source was not read, the claim is a searched gap, or it rests on an absence anchor. "Copies held in the repository" is a separate line (a stored copy is preservation, not reading).
+
+### `media.yaml`: who reported what, when, and how it changed
+`build/subjects/<subject>/media.yaml`. A record of reports, never evidence: `confers_weight: false` (same firewall as `transmission.yaml`, X1 and X3), and no claim cites it in its anchors.
+```yaml
+subject: flydubai-fz1073
+confers_weight: false
+observed: 2026-10-02
+topics:                       # the points reports are compared on
+  - {id: t-copilot-nationality, label: "The co-pilot's nationality", claims: [fz1073-israel-says-omani], resolution: open}   # open | resolved | corrected
+reports:
+  - id: m-012
+    source: src-cnn-live      # a manifest id, OR `url` + `outlet` (exactly one)
+    kind: live_entry          # original | wire | aggregator | live_entry | fact_check | statement | broadcast
+    access: read              # read | summary (a tool summary only) | relayed (seen only through another outlet) | not_opened
+    published: "2026-09-30T11:24:56Z"      # UTC
+    basis: metadata           # metadata | displayed | relayed | computed | zone_unverified
+    origin: cnn-live-0930-omani-entry      # the underlying record; copies of one origin count once
+    derives_from: reuters-0930             # optional: the origin this one draws on
+    said_by: "two Israeli officials (unnamed)"   # who is quoted or cited; "own reporting" if none
+    says:
+      - {topic: t-copilot-nationality, value: "Omani; the co-pilot, allegedly the attacker", version: first}   # version: first | rewritten | unknown
+    changed:                  # in-place changes seen after publication
+      - {observed: "2026-10-01T15:38:00Z", what: "retitled", how_known: "headline against datePublished and dateModified"}
+    note: "..."
+    withdrawn: "reason"       # optional: retire a wrong entry; it stays, struck
+```
+- **MR1** `confers_weight: false`. **MR2** every `says.topic` is a declared topic; a topic that is `resolved` names the claim that resolves it (`resolved_by`); `version` is first, rewritten or unknown. **MR3** a report gives exactly one of `source` (must be in the manifest) or `url` with `outlet`; `kind`, `access` and `basis` are from the lists; `published` is UTC. **MR4** every report has an `origin`; `derives_from` names the origin of another report here. **MR5** every report has `said_by`. **MR6** every `changed` entry has `observed`, `what` and `how_known`. **MR7** a report id on the base ref may not be removed; a wrong entry is retired with `withdrawn: <reason>`.
+- A page time is the time of a story, not of the statement it reports (docs/NEWS_REVIEW.md, guardrail 4). `basis` says how the time was obtained; `zone_unverified` means the page shows a time with no zone and the conversion is an assumption stated in `note`.
+- First appearance of a point is computed, not authored: the earliest report that carries it in its first version. Where the earliest page was rewritten in place, the dossier says its first wording cannot be recovered.
+
+### `story.yaml`: the running story
+```yaml
+subject: flydubai-fz1073
+names:                         # SR9: every person, place, organisation and nationality the story uses
+  people: []                   # a person needs: role, named_by (a manifest id of an authority), also_named_by (two or more manifest ids); never a private individual
+  places: [Dubai, Tabuk]
+  organisations: [Flydubai]
+  demonyms: [Saudi]
+  other: [FZ1073, UTC]
+updates:                       # append-only, oldest first
+  - id: u-001
+    at: "2026-10-02T12:00:00Z" # UTC, not before the update above
+    title: "What is reported so far"
+    headline: {id: h-001, text: "...70 to 95 characters...", mode: attributes, attributed_to: "airline and UAE",
+               claims: [fz1073-diverted-tabuk, {id: fz1073-motive-not-established, mode: open}]}
+    claims_at_update: {fz1073-diverted-tabuk: established/high}    # state/confidence of every cited claim when written
+    paragraphs:
+      - sentences:
+          - id: s-001
+            mode: attributes                    # states | attributes | open
+            attributed_to: "Flydubai and the UAE foreign ministry"   # the text must contain it
+            text: 'Flydubai and the UAE foreign ministry say ...'
+            claims: [fz1073-diverted-tabuk]     # or {id, mode} to say something different about one claim
+            accusation: true                    # optional: shown as "accusation, not a finding"; must be `attributes`
+            denies_target: true                 # only for `states` on a refuted claim: the sentence denies the claim's refutes_target
+            supersedes: s-012                   # optional: replaces an earlier sentence
+            change: corrected                   # updated | narrowed | corrected | withdrawn (needed with supersedes)
+            why: "one sentence: what changed"   # needed with supersedes
+```
+- **SR1** every sentence and headline cites at least one claim id of this subject. No sentence stands without a claim.
+- **SR2** update ids and sentence ids are unique; `at` is UTC and not before the previous update; every update has a title, a headline and no empty paragraph.
+- **SR3** a sentence cannot be stronger than its claim. For each cited claim the sentence's mode must be allowed: `open` always; `attributes` unless the claim is a searched gap; `states` (the project speaks in its own voice) only when the claim is a `judgment`, `established` or `refuted`, at `moderate` or `high` confidence, with `anchor_checked: primary`. A claim that records what a source says (`statement_kind: reported`) can only be attributed. `states` on a refuted claim needs `denies_target: true`: the sentence denies what the claim's `refutes_target` says, and the page prints that target beside the sentence so a reader can check it (some digs write a refuted claim's `statement` as the myth, others as the finding; `refutes_target` is the one field that always names the myth). An `accusation` is `attributes`. With several claims, the weakest governs.
+- **SR4** the text matches its mode: `attributes` contains `attributed_to`; `states` contains no attribution word (says, according to, reportedly, alleged, claims); `open` says plainly that something is not known, not established or not confirmed.
+- **SR5** `supersedes` names an earlier sentence once, is dated after it, and carries `change` and `why`. `change` without `supersedes` is an error.
+- **SR6** every sentence not superseded, and the headline of the latest update, is compared with its claim's current `state/confidence` against `claims_at_update`; a difference is a warning, and the page flags it. (Earlier headlines are history and are not compared.) Owner choice: make it an error.
+- **SR7** no percentage, no count of outlets, reports or posts (repetition carries no weight; name the origin instead), and no hype word anywhere; loaded words (terror, jihadist, radical, hijack, suicide, staged and similar) only inside a quotation, never in our voice. Quotations are not otherwise exempt.
+- **SR8** every headline is 70 to 95 characters.
+- **SR9** every capitalised word is in `names` (a sentence-opening word from a short list is exempt). A person needs `role`, `named_by` and at least two `also_named_by`; `private: true` is an error.
+- **SR10** a story needs a `log.yaml`.
+- **SR11** against the base ref, an update or sentence may not be removed or edited; a change is a new update. The one exception is N26: an update or sentence id that a NEW log entry names in `redacts` (personal data, the owner's decision) may be edited or removed, and only that id.
+- **SR12** the independent reviewer, not the author, writes `story_through: <update id>` in `review.yaml` (docs/PUBLISH_GATE.md). The site builds the story page only up to and including that update; with no `story_through` it builds none. An update after it is held back (a warning says so), not deleted. A `story_through` that names no update is an error.
+- Page (`/news/<slug>/`): the latest headline; what is not known yet (the `open` sentences); the story so far, with a tag on each sentence (claim state and confidence); superseded sentences struck through and marked "changed" with the date, the reason and a link to the new one; the updates list with the headline then; the corrections (every `corrected` or `withdrawn` sentence, plus the dig's log entries that open with CORRECTION or REDACTION, in full up to 300 characters, with a link to the whole entry); the evidence ledger (per sentence: mode, claim, state, confidence, source checked, evidence class, sources); the names register.
`````

### 3.6 The validator

The checks are a new pure module, `build/tools/story_rules.py` (Appendix C), called from `build/conformance.py` for each subject and for the history check. They run only on a subject that has `story.yaml`, `media.yaml` or a manifest `address_withheld`; a subject with none of these is not touched. `conformance.py` changes (a fenced diff, with the `news.yaml` and `build_site.py` changes in 3.7):

`````diff
diff --git a/build/conformance.py b/build/conformance.py
index 8e0c5d7..1c3c7bb 100644
--- a/build/conformance.py
+++ b/build/conformance.py
@@ -24,6 +24,8 @@ import sys
 import yaml
 
 ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
+sys.path.insert(0, os.path.join(ROOT, "build", "tools"))
+import story_rules
 SUBJECTS = os.path.join(ROOT, "build", "subjects")
 
 STATES = {"established", "proposed", "contested", "refuted", "searched_gap"}
@@ -225,7 +227,7 @@ def load_sources(sdir):
 
 
 # Files in a subject folder that record work or review rather than cite sources as evidence.
-PS_SKIP_FILES = {"log.yaml", "review.yaml", "sources.yaml"}
+PS_SKIP_FILES = {"log.yaml", "review.yaml", "sources.yaml", "media.yaml", "story.yaml"}  # media.yaml records what was reported, story.yaml cites claims only
 PS_ACK_KEYS = ("flagged_sources", "source_notices")
 
 
@@ -372,6 +374,11 @@ def check_subject(r, sdir):
             check_anchor_format(r, subject, c, sdir)
 
         check_publication(r, subject, sdir, claims, d)
+        _se, _sw = story_rules.check_story_files(sdir, ids, set(load_sources(sdir)), load)
+        for m_ in _se:
+            r.err(subject, m_)
+        for m_ in _sw:
+            r.warn(subject, m_)
 
         vd = d.get("assessment")
         if vd:
@@ -611,6 +618,22 @@ def check_history(r, base):
                 redacted = any(lid in (x.get("redacts") or []) and x.get("id") not in old_entries for x in new_entries.values())
                 if not redacted:
                     r.err(rel, f"log entry `{lid}` was edited (rule 6: corrections are new entries)")
+    for spath in glob.glob(os.path.join(SUBJECTS, "*", "story.yaml")):
+        rel = os.path.relpath(spath, ROOT)
+        old = git_show(base, rel)
+        if old is not None:
+            _lg = os.path.join(os.path.dirname(spath), "log.yaml")   # N26: an id a NEW log entry names in `redacts` may be edited
+            _old_lg = git_show(base, os.path.relpath(_lg, ROOT))
+            _old_ids = {x.get("id") for x in (yaml.safe_load(_old_lg) or {}).get("log", [])} if _old_lg else set()
+            _red = {i for x in (load(_lg) or {}).get("log", []) if x.get("id") not in _old_ids for i in (x.get("redacts") or [])} if os.path.exists(_lg) else set()
+            for m_ in story_rules.check_story_history(yaml.safe_load(old), load(spath), _red):
+                r.err(rel, m_)
+    for mpath in glob.glob(os.path.join(SUBJECTS, "*", "media.yaml")):
+        rel = os.path.relpath(mpath, ROOT)
+        old = git_show(base, rel)
+        if old is not None:
+            for m_ in story_rules.check_media_history(yaml.safe_load(old), load(mpath)):
+                r.err(rel, m_)
     for cpath in glob.glob(os.path.join(SUBJECTS, "*", "claims.yaml")):
         rel = os.path.relpath(cpath, ROOT)
         old = git_show(base, rel)
diff --git a/build/news.yaml b/build/news.yaml
index b4116e5..1c56be8 100644
--- a/build/news.yaml
+++ b/build/news.yaml
@@ -13,3 +13,5 @@ entries:
   - subject: flydubai-fz1073
     status: live
     as_of: 2026-10-02
+    story: true          # builds /news/<slug>/ from story.yaml
+    dossier: private     # public: /digs/<slug>/dossier/ in the site; private: written to private/dossier/ only, never deployed
diff --git a/build/tools/build_site.py b/build/tools/build_site.py
index 0d425f9..19e54e3 100644
--- a/build/tools/build_site.py
+++ b/build/tools/build_site.py
@@ -85,6 +85,7 @@ sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
 import nodes as _nodes
 import dig_actions as _da
 import pubstatus as _ps
+import dossier as _dos
 NODES = _nodes.load_nodes()
 CUR = {"slug": "", "sub": "", "man": {}}
 ASSESS = {}
@@ -184,6 +185,10 @@ for _s in CFG["publish"]:
     _st = (yaml.safe_load(open(_rp)) or {}).get("status") if os.path.exists(_rp) else None
     if _st not in ("passed", "passed_with_open_items", "grandfathered"):
         sys.exit(f"Refusing to publish `{_s}`: its review.yaml is missing or not passed (status: {_st}). See docs/PUBLISH_GATE.md.")
+_STORY = {}
+_NEWS_E = {e["subject"]: e for e in (yaml.safe_load(open(os.path.join(ROOT, "build", "news.yaml"), encoding="utf-8")).get("entries") or [])}
+_PRINT = f"<style>{_dos.PRINT_CSS}</style>"
+_commit = lambda: (__import__("subprocess").run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown")
 digs, corrections, urls = [], [], ["/", "/digs/", "/atlas/", "/ideas/", "/news/", "/start/", "/method/", "/corrections/", "/about/"]
 for sub in CFG["publish"]:
     base = os.path.join(ROOT, "build", "subjects", sub)
@@ -262,6 +267,24 @@ for sub in CFG["publish"]:
         os.makedirs(os.path.join(OUT, "digs", slug, "timeline"), exist_ok=True)
         shutil.copy(os.path.join(base, "timeline.html"), os.path.join(OUT, "digs", slug, "timeline", "index.html"))
         shutil.copy(os.path.join(base, "timeline.yaml"), os.path.join(OUT, "digs", slug, "timeline", "timeline.yaml"))
+    # News Review entry that opts in (build/news.yaml `story: true`, `dossier: public | private`): evidence dossier and live story.
+    _ne = _NEWS_E.get(sub) or {}
+    if _ne.get("dossier") in ("public", "private") or _ne.get("story"):
+        _ctx = _dos.load_ctx(base, lambda p_: yaml.safe_load(open(p_, encoding="utf-8")), nodes=NODES, build_info={"date": TODAY, "commit": _commit(), "private": _ne.get("dossier") == "private"})
+        _pub = _ne.get("dossier") == "public"
+        if _ne.get("dossier") in ("public", "private"):
+            _dh = page("Evidence dossier: " + str(cl.get("title")), _dos.dossier_html(_ctx), "Evidence dossier generated from the project files. It states no legal conclusion.",
+                       f"/digs/{slug}/dossier/" if _pub else "", extra_head=_PRINT + '<meta name="robots" content="noindex">', depth=3)
+            if _pub:
+                write(f"digs/{slug}/dossier/index.html", _dh)   # noindex, so not in the sitemap
+            else:   # kept out of the deployed site: private/ is git-ignored and never uploaded
+                _pp = os.path.join(ROOT, "private", "dossier", slug, "index.html"); os.makedirs(os.path.dirname(_pp), exist_ok=True); open(_pp, "w", encoding="utf-8").write(_dh)
+        _ctx["story"] = _dos.reviewed_story(_ctx.get("story"), _ctx.get("review"))   # SR12: only updates the independent reviewer has passed
+        if _ne.get("story") and _ctx.get("story"):
+            _sh = page(_ctx["story"]["updates"][-1]["headline"]["text"], _dos.story_html(_ctx, dossier_href=f"../../digs/{slug}/dossier/" if _pub else None, log_corrections=_dos.log_correction_entries(_ctx)),
+                       "A running News Review story: every sentence cites a claim and shows its confidence; changes and corrections stay visible.", f"/news/{slug}/", extra_head=_PRINT, depth=2)
+            write(f"news/{slug}/index.html", _sh); urls.append(f"/news/{slug}/")
+            _STORY[sub] = slug
     digs.append((slug, head, cl.get("search_summary", ""), status))
     urls.append(f"/digs/{slug}/")
     if has_tl: urls.append(f"/digs/{slug}/timeline/")
@@ -313,7 +336,8 @@ for _e in _news.get("entries") or []:
     _d = next((x for x in digs if _cl and x[0] == (_cl.get("url_slug") or _e["subject"])), None)
     if not _d: continue
     _nrows += (f'<li><a href="../digs/{_d[0]}/"><b>{E(_d[1])}</b></a> <span class="pill">{E(_news["status_labels"].get(_e.get("status"), _e.get("status", "")))}</span>'
-               f'<br><span class="small">As of {E(_e.get("as_of", ""))}.</span> {E(" ".join(str(_d[2]).split()))}</li>')
+               f'<br><span class="small">As of {E(_e.get("as_of", ""))}.</span> {E(" ".join(str(_d[2]).split()))}'
+               + (f' <a href="{E(_STORY[_e["subject"]])}/">Read the live story</a>' if _e["subject"] in _STORY else "") + '</li>')
 if not _nrows: _nrows = '<li class="small">No review is published yet. Each one appears here only after an independent review.</li>'
 write("news/index.html", page("News Review", f'<p class="eyebrow">News Review</p><h1>Current stories, checked claim by claim</h1><p>{E(" ".join(str(_news["intro"]).split()))}</p><ul class="l">{_nrows}</ul>'
       f'<h2>How a review works</h2><ul><li>We pick the story; the public can suggest one.</li><li>Each claim is checked against sources we can open, with its confidence and limits shown.</li><li>A dated log records what was known when, and corrections are added, never overwritten.</li><li>A separate reviewer checks it before it goes live.</li></ul>'
`````

The key rules, as lines of the new file (excerpts; the whole file is Appendix C). Truth table of what a sentence may do with a claim:

`````diff
--- /dev/null
+++ b/build/tools/story_rules.py (new file; excerpt of lines 30 to 42)
@@ -0,0 +30,13 @@
+def allowed_modes(c):
+    """The strongest thing a sentence may do with this claim (SR3). Own-voice `states` is allowed only for the project's
+    own judgments (statement_kind judgment), established or refuted, at moderate or high confidence, primary anchor read.
+    A claim that records what a source said (statement_kind reported) can only be attributed; a gap can only be called open."""
+    st, conf, kind = c.get("state"), c.get("confidence"), c.get("statement_kind")
+    chk = c.get("anchor_checked")
+    chk = "no" if chk is False else chk
+    if st == "searched_gap":
+        return {"open"}
+    modes = {"open", "attributes"}
+    if st in ("established", "refuted") and conf in ("high", "moderate") and kind == "judgment" and chk == "primary":
+        modes.add("states")
+    return modes
`````

SR3, the "no sentence stronger than its claim" check, and SR7:

`````diff
--- /dev/null
+++ b/build/tools/story_rules.py (new file; excerpt of lines 161 to 178)
@@ -0,0 +161,18 @@
+        any_open = False
+        for cid, m in cites:
+            c = claims_by_id.get(cid)
+            if c is None:
+                E.append(f"SR1 {where}: cites `{cid}`, which is not a claim in this subject")
+                continue
+            if m not in MODES:
+                E.append(f"SR3 {where}: mode for `{cid}` must be one of {', '.join(MODES)}")
+                continue
+            if m == "open":
+                any_open = True
+            if m == "states" and (c.get("state") == "refuted") != (s.get("denies_target") is True):
+                E.append(f"SR3 {where}: a `states` sentence on a refuted claim must deny the claim's `refutes_target` (`denies_target: true`); `denies_target` is for refuted claims only")
+            if m not in allowed_modes(c):
+                E.append(f"SR3 {where}: says `{m}` on `{cid}`, which is {claim_state_key(c)} ({c.get('statement_kind')}) and allows only "
+                         f"{'/'.join(sorted(allowed_modes(c)))}: a sentence cannot be stronger than its claim")
+        if s.get("accusation") is True and mode != "attributes":
+            E.append(f"SR3 {where}: an `accusation` sentence must be mode `attributes`: an accusation is not a finding")
`````
`````diff
--- /dev/null
+++ b/build/tools/story_rules.py (new file; excerpt of lines 190 to 201)
@@ -0,0 +190,12 @@
+        # SR7 style
+        bare = _quote_stripped(text)
+        if "%" in text or re.search(r"per ?cent", text, re.I):
+            E.append(f"SR7 {where}: no percentages (SCHEMA N23)")
+        for w in HYPE:
+            if re.search(rf"\b{re.escape(w)}\b", bare, re.I):
+                E.append(f"SR7 {where}: hype word `{w}` outside a quotation")
+        for w in LOADED:
+            if re.search(rf"\b{re.escape(w)}", bare, re.I):
+                E.append(f"SR7 {where}: loaded word `{w}` only inside a quotation with attribution, never in our voice")
+        if re.search(r"\b(\d[\d,]*|two|three|four|five|six|seven|eight|nine|ten|many|several|dozens?|hundreds?|thousands?|multiple)\s+(news\s+)?(outlets|media|reports|sources|publications|posts|accounts|articles)\b", bare, re.I):
+            E.append(f"SR7 {where}: a count of outlets, reports or posts: repetition carries no weight (docs/GOVERNANCE.md); name the origin instead")
`````

The manifest line the FZ1073 author would add (D6; the only change to an existing FZ1073 file; I made it in the scratch copy only):

`````diff
diff --git a/build/subjects/flydubai-fz1073/sources/MANIFEST.yaml b/build/subjects/flydubai-fz1073/sources/MANIFEST.yaml
index 70af775..a9a1cd0 100644
--- a/build/subjects/flydubai-fz1073/sources/MANIFEST.yaml
+++ b/build/subjects/flydubai-fz1073/sources/MANIFEST.yaml
@@ -52,6 +52,7 @@ sources:
   title: Emirates 24|7, GCAA commends courage of the captain and crew of flydubai flight FZ1073 (the published headline and URL slug name the
     captain; carrying a UAE General Civil Aviation Authority statement, WAM picture credit; 2 Oct 2026)
   url: https://www.emirates247.com/uae/<path abbreviated here: it contains the victim's name>
+  address_withheld: "the path contains the name of a victim of the incident, which the project's naming policy (log L-30) does not print"
   document_class: secondary (an outlet's copy of an official statement)
   read: yes, directly
   authenticity:
`````

**The validator against broken input.** `bad_story_demo.py` takes the FZ1073 story as written (0 errors, 0 warnings against the current claims) and breaks it eight ways. Output:

`````text
as written: 0 errors, 0 warnings

[1 stronger than its claim: our own voice on a reported claim]
   SR3 u-004/s-016: says `states` on `fz1073-uae-investigation`, which is established/high (reported) and allows only attributes/open: a sentence cannot be stronger than its claim

[2 cites a claim that does not exist, and a sentence with no claim]
   SR1 u-004/s-014: cites `fz1073-made-up`, which is not a claim in this subject
   SR1 u-004/s-015: a sentence must cite at least one claim id (no sentence stands without a claim)

[3 a gap spoken as fact, attributed]
   SR3 u-004/s-017: says `attributes` on `fz1073-event-simulated`, which is searched_gap/low (search_result) and allows only open: a sentence cannot be stronger than its claim

[4 hype, a percentage and a loaded word in our voice]
   SR7 u-004/s-015: no percentages (SCHEMA N23)
   SR7 u-004/s-015: hype word `shocking` outside a quotation
   SR7 u-004/s-015: loaded word `terror` only inside a quotation with attribution, never in our voice
   SR7 u-004/s-015: loaded word `radical` only inside a quotation with attribution, never in our voice

[5 a person named who no authority named]
   SR9 u-004/s-015: `John` is not in `names` (register every person, place, organisation and nationality the story uses)
   SR9 u-004/s-015: `Smith` is not in `names` (register every person, place, organisation and nationality the story uses)
   SR6 update `u-004`: `claims_at_update` has no entry for `fz1073-omani-nationality-unconfirmed`

[6 headline too short]
   SR8 update `u-004` headline is 25 characters; it must be 70 to 95
   SR4 u-004/h-004: the text must name who said it (`attributed_to`: Saudi ministry)
   SR4 u-004/h-004: an `open` sentence must say plainly that something is not known or not established
   SR9 u-004/h-004: `Pilots` is not in `names` (register every person, place, organisation and nationality the story uses)

[7 accusation not attributed]
   SR3 u-004/s-016: an `accusation` sentence must be mode `attributes`: an accusation is not a finding
   SR4 u-004/s-016: an `open` sentence must say plainly that something is not known or not established

[8 SR11: edit an earlier sentence in place, checked against the base copy]
   SR11 sentence `s-001` was edited (supersede it in a new update; the old text stays)
`````

SR11 end to end through `conformance.py --base` (scratch commit of the proposed files, then edits):

`````text
--- 0. baseline: the proposed files committed, nothing edited
15 subjects and 107 shared nodes checked: 0 errors, 95 warnings
--- 1. edit an earlier sentence in place
ERROR    build/subjects/flydubai-fz1073/story.yaml: SR11 sentence `s-001` was edited (supersede it in a new update; the old text stays)
15 subjects and 107 shared nodes checked: 1 errors, 95 warnings
--- 2. the same edit, with a NEW log entry that names s-001 in redacts (N26)
15 subjects and 107 shared nodes checked: 0 errors, 95 warnings
--- 3. rename the last update (its removal is an error)
ERROR    flydubai-fz1073: SR12 review.yaml `story_through` names `u-004`, which is not an update in story.yaml
ERROR    build/subjects/flydubai-fz1073/story.yaml: SR11 update `u-004` was removed (updates are append-only)
ERROR    build/subjects/flydubai-fz1073/story.yaml: SR11 sentence `h-004` was removed (supersede it in a new update)
ERROR    build/subjects/flydubai-fz1073/story.yaml: SR11 sentence `s-013` was removed (supersede it in a new update)
--- 4. append a new update u-005 (accepted)
WARNING  flydubai-fz1073: SR12 updates after `u-004` are held back from the site until the independent reviewer passes them (last update: `u-005`)
15 subjects and 107 shared nodes checked: 0 errors, 96 warnings
`````

(Case 1 is an in-place edit of an earlier sentence: an error. Case 2 is the same edit with a new log entry that names the sentence in `redacts`, the N26 exception for personal data: accepted. Case 3 renames the last update: its removal and the removal of its sentences are errors. Case 4 appends an update: accepted, with a warning that it is held back from the site until the independent reviewer passes it.)

**How a claim's state moves a sentence's limit.** The strongest voice a sentence can have with each claim, counted over the dig-format subjects at `051778c` (`modes.txt`):

`````text
subject                  claims open-only  attribute+ states
apollo-landings               9        1           8     0
casket-letters                9        1           8     0
congress-promise-vote         9        2           7     0
eikon-basilike               11        2           8     1
flydubai-fz1073              39       18          21     0
gulf-of-tonkin               21        3          15     3
incandescent-lamp            39        9          26     4
mcafee-and-surfside          11        1           5     5
proto-indo-european           9        1           8     0
teti-pyramid-texts           49        3          46     0
`````

For FZ1073 no claim allows `states`: every claim there is a report of what someone said or a search result. The live story therefore never speaks in the project's own voice about what happened; it can only attribute and say what is open. That follows from the claims as the independent review passed them, not from a rule about this topic.

### 3.7 `build_site.py` changes

Described, then sketched by the diff in 3.6.

1. **Imports** `dossier.py` (new, Appendix B). No existing function changes.
2. **`build/news.yaml`** gains two optional keys per entry: `story: true` (build `/news/<slug>/` from `story.yaml`) and `dossier: public | private` (absent: no dossier). Both are the owner's switches; the build never defaults to `public`.
3. **Per entry that opts in**: load the subject context (`dossier.load_ctx`), build the dossier page with `page(...)` (so it has the site chrome and `<meta name="robots" content="noindex">`), write it to the public path or to `private/dossier/<slug>/`; apply `reviewed_story()` (SR12: only updates up to the reviewer's `story_through`; none if absent) and write `/news/<slug>/index.html`; add the URL to the sitemap list for the story only.
4. **News page:** a "Read the live story" link on the entry when a story page exists.
5. **Not changed:** the dig page, the timeline page, the corrections page, the Atlas, `llms.txt` (the dossier is `noindex` and not listed), and the existing copy of `claims.yaml`, `MANIFEST.yaml`, `review.yaml`, `timeline.yaml` (see 1.6).

Rendering contracts (functions in `dossier.py`): `dossier_html(ctx)` for the dossier (11 numbered sections, section 3.1); `media_timeline_html(ctx)` for the media section (first-appearance table, SVG strip of reports by point and time, reports in time order, changes, withdrawn entries, transmission chains); `story_html(ctx, dossier_href, log_corrections)` for the story page (heading and "as of", banner, "not known yet", story so far with tags and changed marks, updates list newest first, corrections, evidence ledger, names register, rules). All are pure functions of loaded YAML: they decide no claim state, add no fact and write no data file. Output is deterministic (tested), apart from the build date and commit shown in the dossier.

### 3.8 The long-form investigative report (not built; what would be added)

The owner wants this "later". I recommend not designing it now, for two reasons I can state from the prototype: the unit of rigor is the *sentence tied to a claim*, and the story format already gives that; and the first thing a long report needs is the dossier's source register and conflicts view, which exist after this change. When it is wanted, the smallest addition is a `report.yaml` of sections whose paragraphs reuse the sentence format of `story.yaml` unchanged (same SR rules), with longer prose, headings and figures, and a build that renders the same ledger. Writing that format now would be speculation; it would be its own proposal.

### 3.9 Tests

`build/tools/test_story_dossier.py` (Appendix D, 36 tests, 0.2 s, synthetic subjects in a temp folder, no real dig touched). Groups: `StoryRules` (SR1 to SR9, SR11 including the N26 redaction exception, SR12, drift, sentence modes by claim kind, accusation, hype and count tripwires), `MediaRules` and `MediaHistoryAndWithdrawal` (MR1 to MR7), `Neutrality` (the same pipeline on a politically charged and a technical synthetic subject gives the same rules, structure and sections), `Rendering` (changed marks, whole corrections not cut at a full stop, no data download and no legal-conclusion word in the fixed labels, determinism, withheld address public versus private, a missing media file says so, flags for primary record and hash), and `PublicationStatusInteraction` (a retracted source named in `media.yaml` is not a PS3 hit; the dossier shows a retraction and says "not looked up" for a source nobody looked up). Run output:

`````text
test_mr7_history (__main__.MediaHistoryAndWithdrawal.test_mr7_history) ... ok
ok
test_mr1_confers_weight (__main__.MediaRules.test_mr1_confers_weight) ... ok
test_mr2_topics (__main__.MediaRules.test_mr2_topics) ... ok
test_mr3_report_shape (__main__.MediaRules.test_mr3_report_shape) ... ok
test_mr4_origin (__main__.MediaRules.test_mr4_origin) ... ok
test_mr5_6_said_by_and_changes (__main__.MediaRules.test_mr5_6_said_by_and_changes) ... ok
test_valid (__main__.MediaRules.test_valid) ... ok
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
  m = yaml.safe_load(open(os.path.join(d, "sources", "MANIFEST.yaml")))
ok
  m = yaml.safe_load(open(mp))
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
  m = yaml.safe_load(open(mp))
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
  open(os.path.join(self.d, "sources", "a.txt"), "w").write("text")
  m = yaml.safe_load(open(os.path.join(self.d, "sources", "MANIFEST.yaml")))
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
ok
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
  return hashlib.sha256(open(path, "rb").read()).hexdigest()
ok
ok
ok
ok
ok
test_a_dig_without_the_files_is_unchanged (__main__.StoryRules.test_a_dig_without_the_files_is_unchanged) ... ok
test_sr11_history_is_append_only (__main__.StoryRules.test_sr11_history_is_append_only) ... ok
test_sr1_unknown_and_missing_claim (__main__.StoryRules.test_sr1_unknown_and_missing_claim) ... ok
test_sr2_update_order_and_ids (__main__.StoryRules.test_sr2_update_order_and_ids) ... ok
test_sr3_accusation_must_be_attributed (__main__.StoryRules.test_sr3_accusation_must_be_attributed) ... ok
test_sr3_attribution_on_gap_and_states_on_reported (__main__.StoryRules.test_sr3_attribution_on_gap_and_states_on_reported) ... ok
test_sr3_states_allowed_only_for_our_own_judgment (__main__.StoryRules.test_sr3_states_allowed_only_for_our_own_judgment) ... ok
test_sr3_states_on_a_refuted_claim_must_negate (__main__.StoryRules.test_sr3_states_on_a_refuted_claim_must_negate) ... ok
test_sr4_text_matches_mode (__main__.StoryRules.test_sr4_text_matches_mode) ... ok
test_sr5_supersession (__main__.StoryRules.test_sr5_supersession) ... ok
test_sr6_drift_is_flagged_until_a_new_update_answers_it (__main__.StoryRules.test_sr6_drift_is_flagged_until_a_new_update_answers_it) ... ok
test_sr7_no_count_of_outlets (__main__.StoryRules.test_sr7_no_count_of_outlets) ... ok
test_sr7_style (__main__.StoryRules.test_sr7_style) ... ok
test_sr8_headline_length (__main__.StoryRules.test_sr8_headline_length) ... ok
test_sr9_names (__main__.StoryRules.test_sr9_names) ... ok
test_valid (__main__.StoryRules.test_valid) ... ok

----------------------------------------------------------------------
Ran 36 tests in 0.246s

OK
`````

## 4. What it does not change

- **No claim state, weight, confidence, anchor or evidence class changes.** The generator reads them; the story cites them; nothing writes them. SR3 only restricts what a *sentence* may say.
- **The publish gate is unchanged and is respected, not bypassed.** A subject appears only if it is in `build/site.yaml` `publish` and its `review.yaml` has passed (docs/PUBLISH_GATE.md). The story page is built only as far as the independent reviewer's `story_through` (SR12), so a new update is not published until it is reviewed, as NEWS_REVIEW.md already requires for each significant update. The author never writes `story_through`.
- **No finding changes without a logged review.** Nothing here edits an existing log entry, claim, manifest entry or review (except the one optional `address_withheld` line an author may add through the normal PR path, which changes only how an address is printed in a new page).
- **No new data download.** Section 3.4. No PDF, CSV, JSON or YAML written or linked by any new page; the existing downloads are outside this proposal (1.6, O5).
- **No change to what the existing pages say.** I built the whole site twice on 2026-10-03, from `051778c` and from `051778c` plus this proposal's files, and compared the two trees with `diff -rq` (`diff_sites.txt`). Every dig page, timeline page, the corrections page and the Atlas are byte-identical. Five files differ: the News page (the added "Read the live story" link), `sitemap.xml` (the story URL), the new `/news/<slug>/` page, and the FZ1073 copies of `MANIFEST.yaml` and `review.yaml` (each carries the one scratch line added to it). Those two YAML copies are the existing downloads of 1.6, not a new one.
- **Counts, reactions and repetition still carry no weight** (docs/GOVERNANCE.md). A report is not evidence of what it reports; `media.yaml` and the transmission record cannot be cited as evidence (checked, section 2 item 8).
- **Wikipedia is still never an anchor.** The dossier shows anchors as they are; `media.yaml` is not an anchor.

## 5. Impact: all 15 subjects, validator before and after

Before is `051778c` as built; after is `051778c` plus the files of this proposal in a scratch worktree, including the FZ1073 `story.yaml`, `media.yaml` and the one manifest line. Only FZ1073 has the new files:

`````text
before (051778c): 15 subjects and 107 shared nodes checked: 0 errors, 95 warnings
after  (051778c + this proposal's files): 15 subjects and 107 shared nodes checked: 0 errors, 95 warnings
subject                     errors  warnings |  errors  warnings  unchanged
apollo-landings                  0         5 |       0         5  yes
casket-letters                   0         4 |       0         4  yes
chemtrails                       0         0 |       0         0  yes
congress-promise-vote            0         0 |       0         0  yes
dyatlov-pass                     0         0 |       0         0  yes
eikon-basilike                   0         2 |       0         2  yes
flood-myths-worldwide            0         0 |       0         0  yes
flydubai-fz1073                  0        10 |       0        10  yes
gulf-of-tonkin                   0         2 |       0         2  yes
incandescent-lamp                0         3 |       0         3  yes
mcafee-and-surfside              0         3 |       0         3  yes
proto-indo-european              0        42 |       0        42  yes
teti-pyramid-texts               0        23 |       0        23  yes
votes-2009-present               0         0 |       0         0  yes
votes-johnson-tonkin             0         0 |       0         0  yes
`````

- **14 subjects are not touched in any way:** no `story.yaml`, `media.yaml` or `address_withheld`, so the new checks do not run and the numbers are identical (errors and warnings per subject).
- **FZ1073** has the new files and the same 0 errors and 10 warnings as before; the story added none (SR6 clean, SR12 satisfied by `story_through: u-004`, which in the real repo the independent reviewer would write).
- **Migration for each dig: none.** A dig does not need `media.yaml` or `story.yaml`; adding them is the author's choice, through the normal review. `dossier: private|public` and `story: true` are set per entry in `news.yaml` by the owner.
- **Existing tests:** `test_publication_status.py` 21 of 21 pass.
- **The dossier generator on all 15 subjects** (`table2.py`). Ten subjects have a `claims.yaml` and get a dossier from existing data with no new file; five (chemtrails, dyatlov-pass, flood-myths-worldwide, votes-2009-present, votes-johnson-tonkin) are not in dig format (no `claims.yaml`) and are skipped without error. `needPR` is the number of claims flagged "primary record needed"; `bytes` is the size of the dossier HTML body (the full page with the site chrome is about 6 KB more). FZ1073's row includes `media.yaml`.

`````text
subject                  claims sources    tl   log  trn  needPR    bytes time(s)
apollo-landings               9       0     -     9    -       9    19475 0.02
casket-letters                9       7   yes     9    -       9    52838 0.04
chemtrails                (no claims.yaml: not a dig-format subject, skipped)
congress-promise-vote         9       5   yes     9    -       3    32544 0.03
dyatlov-pass              (no claims.yaml: not a dig-format subject, skipped)
eikon-basilike               11       9   yes     5    -       5    45036 0.04
flood-myths-worldwide     (no claims.yaml: not a dig-format subject, skipped)
flydubai-fz1073              39      65   yes    33  yes      35   443179 0.32
gulf-of-tonkin               21      11   yes    25    -       5   104380 0.08
incandescent-lamp            39      44   yes    24  yes      18   240328 0.19
mcafee-and-surfside          11      10   yes    13    -       6    52393 0.05
proto-indo-european           9       0     -     1    -       9    14323 0.01
teti-pyramid-texts           49       7   yes     4    -      49    73185 0.07
votes-2009-present        (no claims.yaml: not a dig-format subject, skipped)
votes-johnson-tonkin      (no claims.yaml: not a dig-format subject, skipped)
`````

- **Which digs this could matter to:** the five published digs other than FZ1073 (Gulf of Tonkin, McAfee and Surfside, Eikon Basilike, Casket Letters, the lamp) could each be given a private dossier by changing one line of `news.yaml`; today `news.yaml` lists only FZ1073, and the proposal limits the dossier and the story to the entries listed there. The dossier on a non-live dig has no media record, and its section 6 says so.
- **Build time:** the dossier for FZ1073 takes 0.32 s. The whole site build took 4.15 and 4.16 s before and 4.49 and 4.44 s after (two runs each, with the FZ1073 dossier and story switched on).

## 6. Alternatives considered

### 6.1 Overall

| Alternative | Why not |
|---|---|
| **Do nothing** | A lawyer or reader cannot get provenance, the log, a first-appearance view or corrections in full (section 1); the live entry has no story layer, and the owner's request is unmet. The existing discipline is not at fault; the missing views are. |
| **Generate only (layer 1), no new files** | Gives the dossier, statements against material, conflicts, the unverified list, the source register and the log, with no schema change (so the proposal could stop there). It cannot give first-report time, in-place edits and origin per outlet (1.4), and it cannot give a story. I recommend layer 1 even if layers 2 and 3 are declined; it is the part that serves the lawyer. |
| **A separate site or repository for the story** | Splits the evidence from the story, so a sentence could cite a claim that has since changed with no check. SR3, SR6 and SR12 work because the story sits beside the claims and the validator reads both. A second site doubles the review surface. |
| **A PDF made by hand** | Not repeatable, not tied to a commit or to file hashes, not reviewable as a diff, and cannot be regenerated when a claim changes. A PDF is also a data file that this repository's owner does not want published. Here the PDF is the reader's print of a generated page. |
| **GitHub Discussions or issues as the live thread** | The public can already suggest and challenge through the issue forms. Posts there are counts and reactions, which carry no weight; they have no claim ids, no `claims_at_update`, no append-only guarantee and no independent review gate; a live event's correction would sit in a thread. They are a place to *suggest*, not to *report*. |
| **Write the story into `claims.yaml` or the assessment** | `claims.yaml` holds findings and is edited in place with logged review; a story needs an append-only history of what was said when. Mixing them would put history into a file whose job is the current state. |
| **Have a language model write the story prose from the claims** | The prose has to be a human or reviewed-agent editorial act; the format checks it but does not write it. Generating prose would let a template choose which claims to feature and how. SR3 still applies to any author, human or agent. |
| **A free-text "live blog" with no claim ids** | This is what outlets do and what News Review exists to avoid: early reporting on a live event is often wrong, and a sentence that cites nothing cannot be checked. |

### 6.2 Specific: `media.yaml` or fields on timeline events

An alternative to layer 2: add optional keys to `kind: media` timeline events (`origin`, `derives_from`, `said_by`, `says: [{topic, value, version}]`, `changed: [...]`, `access`, `basis`), and compute everything from the timeline.

For: no new file; one record per report; the existing timeline renderer and its rules (T1 to T7) already apply; a report that is on the timeline is not entered twice.

Against, and why I chose a new file: (a) 23 of the 42 records I wrote have no media event at the same time on the timeline (statements, wire and fact-check items), and putting them there would change the chart, which was drawn to show the event, not the coverage; (b) a report has one publication moment and several later edits, and a timeline event is one moment: either an edit becomes a second event (and the chart fills with edits) or it is nested data that the chart ignores; (c) `topics` (the points reports are compared on) span reports and belong to no event; (d) `timeline.yaml` is read by `render_timeline.py` and `nodes.py`, and its `sources` namespace is its own (the dossier has to join it to the manifest by URL), so extending it touches more existing code; (e) a `media.yaml` that does not exist leaves every other dig untouched with no schema change to a file all of them have.

It is a genuine trade-off; O3 asks the owner.

### 6.3 Specific: public dossier or private

A public dossier is more open and lets anyone check a claim against its provenance; it also publishes a 132-page document containing the whole log and all source notes, and whatever a source address or a stored text contains. A private dossier gives the owner the case file now without a publication decision. The code supports both with one line of `news.yaml`; the recommendation is `private` until the owner has read it (O2).

## 7. Neutrality check

The rules read only claim fields (`state`, `statement_kind`, `confidence`, `anchor_checked`, `refutes_target`), the text of a sentence, and the story's own register. They have no per-topic, per-side or per-outcome input. I ran the same pipeline on three digs that differ in direction and kind.

| Dig | Kind and direction | `states` allowed on | Result |
|---|---|---|---|
| `flydubai-fz1073` | politically charged, live, unsettled; every claim reports what someone said or is a search result | 0 of 39 claims | Story can only attribute or say "not known"; headline attributes the Saudi text and calls the rest open |
| `gulf-of-tonkin` | politically charged, historical, settled; its headline claim is *refuted* | 3 of 21 claims | Story states in our voice that the second attack did not take place and shows `denies:` the refutes_target |
| `incandescent-lamp` | technical, historical, mixed (17 established, 5 refuted, 4 contested, 4 proposed, 9 searched gaps) | 4 of 39 | Story states two refutations, calls two contested points open |

Tonkin story page as generated (the `[state, confidence]` tag and the `denies:` target are printed for the reader to compare):

`````text
Gulf of Tonkin: the second attack reported on 4 August 1964 did not happen, the record showsNews Review · story
Gulf of Tonkin: the second attack reported on 4 August 1964 did not happen, the record shows
Last updated 2 Oct 2026 12:00 UTC · 1 updates · 5 sentences, each tied to a claim · 0 correction(s) · Evidence dossier
How to read this. This is a running story, written from the claims in the News Review entry. Every sentence names the claim it rests on and shows how sure the claim is. A sentence that says what someone said is not a finding; a sentence that says something is not known is not a hint. When a fact changes, the old sentence stays on the page, marked, and a dated update replaces it.
What is not known yet
No document read so far shows an order to provoke the 2 August clash by sending the Maddox in as bait. [searched gap, low]
The original decrypted Vietnamese text of the key intercept cited for 4 August cannot be located. [searched gap, moderate]
The story so far
2 Oct 2026 12:00 UTC · What the record shows
North Vietnamese torpedo boats attacked USS Maddox on 2 August 1964; the destroyer and supporting aircraft returned fire. [established, high]
The second attack reported on 4 August 1964 did not take place. [refuted, high] denies: A second North Vietnamese attack took place on 4 August 1964
Signals intelligence about 4 August was presented to senior decision-makers in a way that left out almost all the material showing no attack. [established, moderate]
No document read so far shows an order to provoke the 2 August clash by sending the Maddox in as bait. [searched gap, low]
The original decrypted Vietnamese text of the key intercept cited for 4 August cannot be located. [searched gap, moderate]

[Evidence ledger, first rows]
s-001
North Vietnamese torpedo boats attacked USS Maddox on 2 August 1964 … | states | tonkin-aug2-maddox-engaged | established, high | primary | primary_text | nodes: tonkin-1964-08-02-maddox-fires-three-warning-rounds-north-vietnamese | 
s-002
The second attack reported on 4 August 1964 did not take place. | states | tonkin-aug4-attack-occurred | refuted, high | primary | primary_text | nodes: tonkin-1964-08-04-second-attack-reported-then-refuted tonkin-1964-08-04-herrick-s-doubt-message-sent tonkin-1964-08-04-report-12-boat-reports-an-enemy-aircraft tonkin-1964-08-04-report-13-we-shot-at-two-enemy +1 | 
s-003
Signals intelligence about 4 August was presented to senior … | states | tonkin-sigint-selectively-presented | established, moderate | primary | interpretive | nodes: tonkin-1964-08-08-cia-cover-note-sends-bundy-the-selected | 
s-004
No document read so far shows an order to provoke the 2 August clash … | open | tonkin-bait-order | searched gap, low | secondary | primary_text | | 
s-005
The original decrypted Vietnamese text of the key intercept cited for … | open | tonkin-or ...
`````

Lamp story page, the same format on a technical subject:

`````text
Edison did not invent the bulb alone: carbon lamps were patented by 1845; Edison v Swan is openNews Review · story
Edison did not invent the bulb alone: carbon lamps were patented by 1845; Edison v Swan is open
Last updated 2 Oct 2026 12:00 UTC · 1 updates · 4 sentences, each tied to a claim · 0 correction(s) · Evidence dossier
How to read this. This is a running story, written from the claims in the News Review entry. Every sentence names the claim it rests on and shows how sure the claim is. A sentence that says what someone said is not a finding; a sentence that says something is not known is not a hint. When a fact changes, the old sentence stays on the page, marked, and a dated update replaces it.
What is not known yet
Whether Swan, not Edison, should be credited with the incandescent lamp is not settled. [contested, moderate]
Who first made, and who first sold, a lamp practical for ordinary use is not settled by anything read so far. [contested, low]
The story so far
2 Oct 2026 12:00 UTC · What the record shows
Edison was not the first or only inventor of the incandescent lamp. [refuted, high] denies: Thomas Edison invented the light bulb (as its first or only inventor)
Lodygin was not the first to patent an electric light in an enclosed globe. [refuted, high] denies: Lodygin was the first inventor of the incandescent lamp (the first to describe or patent it)
Whether Swan, not Edison, should be credited with the incandescent lamp is not settled. [contested, moderate]
Who first made, and who first sold, a lamp practical for ordinary use is not settled by anything read so far. [contested, low]

[Evidence ledger, first rows]
s-001
Edison was not the first or only inventor of the incandescent lamp. | states | lamp-edison-sole-inventor | refuted, high | primary | primary_text | abridgments-1859 chemnews-1879 us181613 47f454 52f300 54f678 +1 nodes: lamp-1841-08-21-de-moleyns-patent-9053 lamp-1845-11-04-king-starr-patent-10919 lamp-1878-12-swan-rod-lamp-newcastle-chemical-society lamp-1891-47f454-wallace-upholds-edison-lamp-patent | 
s-002
Lodygin was not the first to patent an electric light in an enclosed … | states | lamp-lodygin-first-claim | refuted, high | primary | primary_text | abridgments-1859 nodes: lamp-1841-08-21-de-moleyns-patent-9053 lamp-1845-11-04-king-starr-patent-10919 | 
s-003
Whether Swan, not Edison, should be credited with the incandescent … | open | lamp-swan-before-edison | contested, moderate | primary | primary_text | chemnews-1879 chemnews-1880 edison-papers-doc1831 47f454 us223898 nodes: lamp-1878-12-swan-rod-lamp-newcastle-chemical-society lamp-1879-02-03-swan-shows-lamp-lit-and-phil lamp-1879-10-22-batchelor-cotton-thread-lamp | 
s-004
Who first made, and who first sold, a lamp ...
`````

The Tonkin and lamp `story.yaml` files are Appendices G and H. Both validate with 0 errors in the scratch copy (`conf-three.txt`: the only new output is the SR12 notice, because no reviewer line exists for these scratch stories). The unit test `Neutrality` runs one pipeline on a politically charged and a technical synthetic subject and compares the rules triggered, the page structure and the sections.

What this check does and does not show, so the assessor does not have to infer it:

- It shows the rules treat refuted, contested, settled and live claims by the same logic, and that no rule has a topic parameter.
- It also exposed one inconsistency in existing data that the story rule had to respect: the dig files use `statement` for a refuted claim in two ways. In Tonkin the `statement` is the claim *refuted* ("North Vietnamese torpedo boats attacked ... a second time"); in the lamp dig it is the *finding* ("Edison did not invent the incandescent lamp from nothing ..."). `refutes_target` is the one field that always names the myth. SR3 therefore asks a `states` sentence on a refuted claim to deny the `refutes_target`, and the page prints that target beside the sentence (this fixed a wrong first version of the rule that assumed the `statement` was the thing denied). The inconsistency is not fixed by this proposal; it is mentioned because a different dig could expose it again.
- It does not show that the *choice of sentences* is neutral; that is editorial, and the independent reviewer's job. The format makes the choice visible (every sentence has a ledger row) but cannot make it fair.
- The loaded-word list (SR7) is a short, owner-maintainable list. I removed "mossad" from my first version because an organisation's name is not a loaded word, and kept words that assign motive or guilt whichever side uses them (terror, jihadist, radical, hijack, suicide, false flag, staged, fabricated, manufactured). A list drawn from one event will be lopsided; see R2.

## 8. What the dossier and story must, and must not, contain

### 8.1 What a lawyer sees

A lawyer opens the (private or public) dossier and finds, in this order: what the document is and is not; the position in one page; for every claim its chain of evidence and a flag "primary record needed" or "primary text read"; who said what and when against material; conflicts without judgment; the media timeline; **what we could not verify**; the primary records to obtain; **provenance per source** (origin, access read or not, independence by origin, authenticity status and strength, date checked, hash where a copy is stored, publication status or "not looked up", tests, gaps, next step, who cites it); the log in full; and the hashes of the files the page came from.

### 8.2 What it must not contain (rules D1 to D6, SR7 to SR9)

- No legal conclusion, and nothing about anyone's liability, intent, guilt or what a court would find. The fixed labels contain no word from a legal-conclusion list (tested). Our ratings are printed as ratings ("confidence high; evidence 4 of 5"), and the page says they are "not a legal standard of proof" (D4).
- No suspect, private individual, victim or minor named *by the generator*; the story's names register forces each name to be justified (SR9). The dossier prints the claim files as they stand, so the entry's guardrails apply to those files first; the dossier does not repair a name that is in them. (A name found in a published *address* is handled by D6; a name inside a log entry is handled by N26 redaction, as in L-24.)
- No accusation without attribution; no loaded word in our voice; no percentage; no count of outlets or posts as weight; no hype.
- No new data download; no PDF in the build.
- No speculation as a finding: a searched gap can only be `open`; an absence anchor stays capped at provisional (existing rule, shown on the card).

### 8.3 What the dossier says it cannot do

Every dossier carries a fixed box at the top: it is a record of what is claimed, by whom, when and on what evidence; it adds no fact; it is not legal advice; it states no legal conclusion; our ratings are editorial and are not a legal standard of proof; it names no one itself.

## 9. Risks

**R1. Live-event harm.** A live story can be quoted out of context, can name the wrong person, can be read as an accusation. Mitigations: the guardrails above, SR12 (the independent reviewer passes each update before it is public), `denies:` and `accusation, not a finding` tags, no person named by the generator. Residual: an update the reviewer passes in error is public until a correction; the correction mechanism (SR5, SR11, the correction log) is the remedy, and is faster than before because it is a new sentence rather than an edit of a finding.

**R2. Naming.** SR9 is a capitalised-word register check: it catches an unregistered "Smith" and not an initial, a nickname, a lower-cased name, a name inside an image caption or a person described so precisely that they are identifiable ("the co-pilot, an Omani who joined eight months ago"). That last case is a real exposure that no mechanical check can close: the FZ1073 claims already contain such descriptions (nationality, tenure) attributed to officials. The story repeats them only attributed and only where the claim records them; a human reviewer has to judge identifiability. The loaded-word list is a tripwire and can be evaded by a synonym.

**R3. Defamation risk.** A dossier gathered for a lawyer lists accusations by officials with names of the accusers and their words. It is deliberately a record of who said what, with attribution (D1), not of whether it is true; but a public dossier is a publication, and an attributed accusation can still be actionable in some jurisdictions. That is a reason to default to `private` (O2) and to have counsel review before any public dossier of a live event. I am not able to give a legal opinion and this proposal does not pretend to.

**R4. Provenance gaps shown plainly may embarrass the project.** The dossier tells the reader that 14 sources were not read, 4 are stored, and 59 of 65 have no per-source date. That is the point; but it will be read. It also exposes errors fast (the Saudi statement was first marked "not read" and was later read: L-26 item 1).

**R5. Volume.** The FZ1073 dossier is 132 A4 pages and the story page 34 KB. A reader will not read 132 pages; the position page and the "what we could not verify" list are what an actual reader gets to. The `media.yaml` record and the story are hand work for an author (42 records and 4 updates took one session); a live event can outrun the author. The format does not make that faster; it makes sloppiness visible.

**R6. Maintenance and drift.** The story is written against claims that will move. SR6 warns on drift; I proposed a warning, not an error, because a claim can legitimately move and the site should not refuse to build. O4 offers an error. The story can still lag the claims; the page shows "claim has changed since" meanwhile.

**R7. The prototype is not production code.** `dossier.py` (about 600 lines) is a first implementation, written in one session, with 36 tests. It will need review by someone who did not write it, and a design pass on the CSS (print layout was checked on two pages only). `weasyprint` was used only to check print layout.

**R8. Media record fidelity.** `first seen` is only as complete as `media.yaml`; "first wording not recoverable" is stated where it applies; the archived-version blocks (Wayback content is blocked in this environment, L-25) mean most in-place changes are unknown. A lawyer must not read "first seen" as "first published anywhere".

**R9. Two checks I could not make.** I did not run the story through a human reviewer; and I did not test on a second live event (there is none). The neutrality test is on historical digs and synthetic subjects for that reason.

## 10. Owner choices (separate from the standards)

These are decisions for the owner after the assessment; none is needed to meet the seven standards.

- **O1. Which layers.** (a) Layer 1 only (dossier from existing data, no schema change except D6 and `news.yaml` keys); (b) layers 1 and 2; (c) all three. My recommendation: (a) at least; (c) if the owner wants the live story.
- **O2. Dossier public or private.** Recommended: `private` for now. The build supports either per entry.
- **O3. `media.yaml` or fields on timeline events** (6.2). Recommended: `media.yaml`.
- **O4. SR6 as a warning or an error.** Recommended: warning, with the owner able to raise it.
- **O5. The existing YAML downloads** (1.6): leave, or remove the links and the copies; and whether `deploy.yml` should refuse `*.pdf` as well. Both are outside this proposal; `.github/` is owner-only.
- **O6. Who writes updates and who passes them.** The author agent writes updates; an independent reviewer writes `story_through` (SR12). Alternative: the owner passes updates. The format supports either; PUBLISH_GATE.md says the reviewer.
- **O7. The loaded-word and hype lists.** They are lists in `story_rules.py`; a change is a proposal like any rule. The owner may want the lists in a data file.
- **O8. Whether the log itself should be published on the dig page** (L-24 says it is; the build does not). The dossier prints it in full; whether the *dig page* should is a separate question.
- **O9. The `news.yaml` keys** (`story`, `dossier`) as the owner's switches. Alternative: put them in each subject's folder. I used `news.yaml` because it is already the owner's list of entries.
- **O10. Long-form report** (3.8): commission a separate proposal when wanted.

## 11. What was not done, and limits

- No pull request, no merge, nothing applied to the repository except this file. The files in the appendices are not in `build/`; they are in the session scratchpad (`story/lib/` and `story/wtT/`, a scratch worktree at `051778c` plus the proposal's files) and are reproduced here from those exact files (fingerprints in Appendix L). Anyone applying this has to add them in the same commit as the SCHEMA text and the validator.
- The FZ1073 `story.yaml` is a worked example, not published text, and its times are illustrative. The `media.yaml` is an unreviewed conversion of a research note.
- The dossier's section 4 prints timeline events as the timeline gives them; I did not audit the 91 events.
- One thing I could not verify: whether a legal reviewer finds the dossier's layout useful. The owner's description of what a lawyer needs was the spec; no lawyer saw it.
- A long-form report format is not designed (3.8).

## 12. If it is approved: the order of work

1. Owner decides O1 to O5 on the assessed proposal; the decision and reason are logged on the PR.
2. One commit on a `process/news-story-and-dossier-formats` branch adds `build/tools/dossier.py`, `build/tools/story_rules.py`, the tests, the `conformance.py` and `build_site.py` hooks, the `build/SCHEMA.md` section and the two `news.yaml` keys, with the validator updated in the same change (docs/SCHEMA_PROPOSALS.md, process step 4). Owner merges; no agent does.
3. A separate PR on the FZ1073 branch adds `story.yaml`, `media.yaml` and the `address_withheld` line, reviewed by an independent agent who writes `story_through`.
4. The owner opens the private dossier from a local build (`python3 build/tools/build_site.py`; the page is in `private/dossier/<slug>/`).

## Appendix A: `gen.py`, the prototype generator

Run as `python3 gen.py --repo <worktree> --subject <slug> --out <dir> [--story f] [--media f] [--bare] [--pdf]`. It reads the subject folder only and writes `<out>/<slug>/dossier/index.html` and, when a story exists and has passed `story_through`, `<out>/<slug>/index.html`. It reuses `build_site.py`'s `page()` and CSS so the output looks like the site. It writes no data file; `--pdf` (weasyprint) is for checking print layout only and is not part of the proposed build. `run_all.sh` runs it for FZ1073, a "bare" run (existing data only), and the Tonkin and lamp neutrality runs.

`````python
#!/usr/bin/env python3
"""Prototype generator: dossier + media timeline + live story page for one subject, from the subject folder.
    python3 gen.py --repo WT --subject flydubai-fz1073 --out OUT [--story story.yaml] [--media media.yaml] [--pdf]
Reads only. Writes OUT/<subject>/dossier/index.html and, when a story exists, OUT/<subject>/index.html. No data file is copied or linked."""
import argparse, ast, os, subprocess, sys, datetime, yaml
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "lib"))   # prototype copies of dossier.py and story_rules.py

ap = argparse.ArgumentParser()
ap.add_argument("--repo", required=True); ap.add_argument("--subject", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--story"); ap.add_argument("--media"); ap.add_argument("--pdf", action="store_true"); ap.add_argument("--bare", action="store_true", help="ignore story.yaml and media.yaml: what the existing data alone gives")
a = ap.parse_args()
sys.path.insert(0, os.path.join(a.repo, "build", "tools"))
import dossier as D   # the prototype copy in lib/ (the same file as build/tools/dossier.py in the scratch worktree)
src = open(os.path.join(a.repo, "build", "tools", "build_site.py"), encoding="utf-8").read()
css = src.split('CSS = """', 1)[1].split('"""', 1)[0]
tree = ast.parse(src)
page_src = next(ast.get_source_segment(src, n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "page")
import html as _h
CFG = yaml.safe_load(open(os.path.join(a.repo, "build", "site.yaml")))
ns = {"E": lambda s: _h.escape(str(s if s is not None else "")), "CFG": CFG, "TODAY": datetime.date.today().isoformat(), "CSS": css + D.PRINT_CSS}
exec(page_src, ns); page = ns["page"]
import nodes as N
loader = lambda p: yaml.safe_load(open(p, encoding="utf-8"))
sdir = os.path.join(a.repo, "build", "subjects", a.subject)
if not os.path.exists(os.path.join(sdir, "claims.yaml")):
    print("skipped: no claims.yaml (not a dig-format subject)"); sys.exit(0)
commit = subprocess.run(["git", "-C", a.repo, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
ctx = D.load_ctx(sdir, loader, a.story, a.media, nodes=N.load_nodes(), build_info={"date": datetime.date.today().isoformat(), "commit": commit})
if a.bare: ctx["story"] = ctx["media"] = None
if ctx["story"]:
    rv = D.reviewed_story(ctx["story"], ctx["review"])   # SR12, as the real build does
    if rv is None:
        print("note: review.yaml has no story_through, so the real build would publish no story; shown here for the proposal only")
    else:
        ctx["story"] = rv
title = ctx["claims_doc"].get("title") or a.subject
out = os.path.join(a.out, a.subject)
os.makedirs(os.path.join(out, "dossier"), exist_ok=True)
d_html = page("Evidence dossier: " + title, D.dossier_html(ctx), "Evidence dossier generated from the project files. No legal conclusions.", depth=0)
open(os.path.join(out, "dossier", "index.html"), "w", encoding="utf-8").write(d_html)
print("dossier", len(d_html), "bytes")
if ctx["story"]:
    s_html = page(ctx["story"]["updates"][-1]["headline"]["text"], D.story_html(ctx, log_corrections=D.log_correction_entries(ctx)), "A running story with an evidence ledger.", depth=0)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(s_html)
    print("story", len(s_html), "bytes")
if a.pdf:
    import weasyprint
    weasyprint.HTML(os.path.join(out, "dossier", "index.html")).write_pdf(os.path.join(out, "dossier.pdf"))
    print("pdf written (not for publication)")
`````

## Appendix B: `build/tools/dossier.py` (new)

Prototype file as run. The CSS is `PRINT_CSS`; the three entry points are `dossier_html`, `media_timeline_html` and `story_html`.

`````python
"""Evidence dossier, media timeline and live story page, generated from a subject folder. Pure functions: they take loaded
data and return HTML strings. They never decide a claim state, add a fact or write a data file.
Proposed in docs/proposals/news-story-and-dossier-formats.md. Used by build/tools/build_site.py (or the prototype gen.py)."""
import html, os, re, hashlib, datetime, json
import pubstatus as PS   # publication status (retracted, corrected sources) is shown exactly as on the dig page

E = lambda s: html.escape(str(s if s is not None else ""))
SQ = lambda s: " ".join(str(s if s is not None else "").split())


def SH(s, n):
    """Shorten at a word boundary, with an ellipsis; never mid-word."""
    s = SQ(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0].rstrip(",;:") + " …"
STATE_ORDER = {"established": 0, "refuted": 1, "contested": 2, "proposed": 3, "searched_gap": 4}
KIND_CODE = {"original": "O", "wire": "W", "aggregator": "A", "live_entry": "L", "fact_check": "F", "statement": "P", "broadcast": "B"}
KIND_WORD = {"original": "original report", "wire": "wire copy", "aggregator": "roundup", "live_entry": "live-blog entry", "fact_check": "fact-check",
             "statement": "statement by the speaker", "broadcast": "broadcast"}
ACCESS_WORD = {"read": "read in full here", "summary": "seen only as a tool summary", "relayed": "known only through another outlet's copy", "not_opened": "not opened"}
BASIS_WORD = {"metadata": "page metadata", "displayed": "time shown on the page", "relayed": "time given by another outlet", "computed": "computed by us",
              "zone_unverified": "time zone of the page not verified"}
REQUIRED_NOTE = "Our ratings are editorial and are not a legal standard of proof."

PRINT_CSS = """
.dossier h2{margin-top:1.6em}.dossier table{width:100%;border-collapse:collapse;font-size:14px;margin:8px 0}.dossier th,.dossier td{border:1px solid var(--line);padding:5px 7px;vertical-align:top;text-align:left}
.dossier td,.dossier th{overflow-wrap:anywhere}.dossier table.media{table-layout:fixed}.dossier .url{font:9px/1.3 'IBM Plex Mono',monospace;color:var(--mute);display:block}
.dossier th{background:var(--sand2);font:11.5px 'IBM Plex Mono',monospace;text-transform:uppercase;letter-spacing:.04em}.dossier .src{break-inside:avoid}ul.l.tight li{padding:2px 0;border-top:0}ul.l.tight{margin:2px 0}
.kv{display:grid;grid-template-columns:170px 1fr;gap:2px 12px;font-size:14px;margin:6px 0}.kv b{font:11.5px 'IBM Plex Mono',monospace;color:var(--mute);text-transform:uppercase;font-weight:400}
.flag{display:inline-block;font:11.5px 'IBM Plex Mono',monospace;border:1px solid var(--coral);color:var(--coral);border-radius:4px;padding:0 6px}.ok{border-color:var(--teal);color:var(--teal)}
.scope{border:2px solid var(--ink);padding:10px 16px;margin:14px 0;font-size:15px}.chg{border-left:4px solid var(--amber);padding-left:10px;color:var(--mute)}
.corr{border-left:4px solid var(--coral);padding-left:10px}del{color:var(--mute)}.tag{font:11px 'IBM Plex Mono',monospace;color:var(--mute);white-space:nowrap}
.sent{margin:.35em 0}.sent .tag{margin-left:4px}svg.strip text{font:10px 'IBM Plex Mono',monospace;fill:var(--mute)}
@page{size:A4;margin:16mm 14mm 18mm;@bottom-center{content:"Evidence dossier, page " counter(page) " of " counter(pages);font:8pt sans-serif;color:#555}}
@media print{nav,footer,.noprint{display:none!important}body{background:#fff;color:#000;font-size:10.5pt;line-height:1.45}.w{max-width:none;padding:0}
.src,tr,.scope{break-inside:avoid}.dossier .claim{padding:8px 12px;margin:8px 0}h2{break-after:avoid;break-before:auto}h2.newpage{break-before:page}thead{display:table-header-group}
a{color:#000;text-decoration:none}a[href^="http"]::after{content:" <" attr(href) ">";font-size:7.5pt;word-break:break-all;color:#333}.dossier table a[href^="http"]::after{content:none}.dossier table{font-size:9pt}svg.strip{max-width:100%}}
"""


def sha256_file(path):
    try:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError:
        return None


def load_ctx(sdir, loader, story_path=None, media_path=None, nodes=None, build_info=None):
    def opt(name, override=None):
        p = override or os.path.join(sdir, name)
        return loader(p) if os.path.exists(p) else None
    cl = loader(os.path.join(sdir, "claims.yaml")) or {}
    man_doc = opt("sources/MANIFEST.yaml") or {}
    ctx = {"sdir": sdir, "claims_doc": cl, "claims": cl.get("claims") or [], "man_doc": man_doc,
           "man": {s.get("id"): s for s in man_doc.get("sources") or [] if isinstance(s, dict)},
           "timeline": opt("timeline.yaml"), "trans": opt("transmission.yaml"), "log": (opt("log.yaml") or {}).get("log") or [],
           "review": opt("review.yaml") or {}, "story": opt("story.yaml", story_path), "media": opt("media.yaml", media_path),
           "nodes": nodes or {}, "info": build_info or {}}
    ctx["by"] = {c.get("id"): c for c in ctx["claims"]}
    ctx["cited_by"] = {}
    for c in ctx["claims"]:
        for sid in (c.get("anchor") or {}).get("sources") or []:
            ctx["cited_by"].setdefault(sid, []).append(c["id"])
    return ctx


# ---------- small helpers ----------
def access_of(s):
    r = SQ(s.get("read")).lower()
    if r.startswith("no"):
        return "not read", False
    if r.startswith("yes") and ("only" in r or "part" in r):
        return "read in part (" + SQ(s.get("read"))[SQ(s.get("read")).find("("):].strip("()") + ")" if "(" in SQ(s.get("read")) else "read in part", True
    if r.startswith("yes"):
        return "read in full", True
    return SQ(s.get("read")) or "not recorded", False


def auth_of(s):
    a = s.get("authenticity") or {}
    st = a.get("status") if isinstance(a, dict) else a
    if st == "not_applicable":
        return "not applicable (a news report)"
    if st == "unchecked":
        return "not checked"
    if st in ("authenticated", "disputed", "forged"):
        return f'{st}, strength {a.get("strength", "n/a")}'
    return str(st)


def origin_map(media):
    """source id -> set of origins; origin -> derives_from root."""
    sm, parent = {}, {}
    for r in (media or {}).get("reports") or []:
        parent.setdefault(r["origin"], r.get("derives_from"))
        if r.get("derives_from"):
            parent[r["origin"]] = r["derives_from"]
        if r.get("source"):
            sm.setdefault(r["source"], set()).add(r["origin"])
    def root(o):
        seen = set()
        while parent.get(o) and o not in seen:
            seen.add(o); o = parent[o]
        return o
    return sm, root


def addr(ctx, s):
    """A source address as printed. `address_withheld: <reason>` on a manifest entry (SCHEMA D6) prints the host only, in a public dossier:
    for an address whose path carries a name the project does not print. A private dossier prints the full address (a lawyer needs it)."""
    u = s.get("url", "") or ""
    if s.get("address_withheld") and not ctx["info"].get("private"):
        return re.sub(r"^(https?://[^/]+).*$", r"\1", u) + "/ (path withheld: " + SQ(s["address_withheld"]) + ")"
    return u


def primary_needs(ctx, c):
    """Why a reader may need the primary record for this claim. Empty list = a stored, authenticated primary text was read."""
    why = []
    chk = c.get("anchor_checked")
    chk = "no" if chk is False else chk
    if chk != "primary":
        why.append(f"the anchor was not read at primary level (source checked: {chk})")
    srcs = (c.get("anchor") or {}).get("sources") or []
    unread = [s for s in srcs if s in ctx["man"] and access_of(ctx["man"][s])[0] == "not read"]
    if unread:
        why.append("cites sources not read: " + ", ".join(unread))
    if c.get("absence_anchor"):
        why.append("rests on a search that found nothing (absence of a record is not a record of absence)")
    if c.get("state") == "searched_gap":
        why.append("a searched gap: the record that would settle it has not been obtained")
    return why


# ---------- dossier ----------
def _src_line(ctx, sid, origins, root):
    s = ctx["man"].get(sid)
    if not s:
        return f"<li>{E(sid)} (not in the manifest)</li>"
    acc, _ = access_of(s)
    org = ""
    if sid in origins:
        org = "; origin " + ", ".join(sorted({root(o) for o in origins[sid]}))
    stored = "; stored copy" if s.get("stored_as") else ""
    return f'<li><a href="#{E(sid)}">{E(sid)}</a> <span class="small">{E(acc)}; authenticity {E(auth_of(s))}{E(org)}{stored}</span></li>'


def claim_card(ctx, c, origins, root):
    chk = c.get("anchor_checked"); chk = "no" if chk is False else chk
    an = c.get("anchor") or {}
    srcs = an.get("sources") or []
    need = primary_needs(ctx, c)
    h = (f'<div class="claim" id="{E(c["id"])}"><p><b>{E(c["id"])}</b> <span class="pill s-{E(c.get("state"))}">{E(str(c.get("state")).replace("_", " "))}</span> '
         f'<span class="small">{E(c.get("statement_kind", ""))}</span></p><p>{E(SQ(c.get("statement")))}</p>')
    h += (f'<div class="kv"><b>Our rating</b><span>confidence {E(c.get("confidence"))}; evidence {E(c.get("evidential_weight"))} of 5; '
          f'public belief {E(c.get("adoption_weight"))} of 5; evidence class {E(c.get("evidence_class"))}; source checked: {E(chk)}</span>'
          f'<b>Anchor</b><span>{E(an.get("type"))}: {E(SQ(an.get("description")))}</span></div>')
    if srcs:
        distinct = ""
        if origins:
            nrec = sum(1 for s in srcs if s in origins)
            distinct = f" Origin recorded (media record) for {nrec} of {len(srcs)}; none is inferred. One origin is counted once however many outlets copy it, and a live blog can hold several."
        h += (f'<p class="small" style="margin-bottom:0"><b>Cited sources ({len(srcs)}).</b>{E(distinct)}</p><ul class="l tight">'
              + "".join(_src_line(ctx, s, origins, root) for s in srcs) + "</ul>")
    nl = an.get("nodes") or []
    if nl:
        h += '<p class="small"><b>Evidence nodes:</b> ' + "; ".join(
            f'{E(x.get("node") if isinstance(x, dict) else x)} ({E(SH(ctx["nodes"].get(x.get("node") if isinstance(x, dict) else x, {}).get("label", ""), 80))})' for x in nl) + "</p>"
    if c.get("exception"):
        h += f'<p class="small"><b>Exception recorded for this rating:</b> {E(SQ(c["exception"]))}</p>'
    held = sum(1 for s in srcs if ctx["man"].get(s, {}).get("stored_as"))
    keep = f' Copies held in the repository: {held} of {len(srcs)} cited source(s); for the others the reader must retrieve the record from its address, and a page can change.' if srcs else ""
    h += PS.claim_notice_html(c, ctx["man"])
    h += (('<p><span class="flag">primary record needed</span> ' + E("; ".join(need)) + "</p>") if need else '<p><span class="flag ok">primary text read</span></p>') + (f'<p class="small">{E(keep)}</p>' if keep else "")
    h += f'<p class="small"><b>Would change if:</b> {E(SQ(c.get("would_change_if")))}' + (f' <b>Next step:</b> {E(SQ(c["next_step"]))}' if c.get("next_step") else "") + "</p></div>"
    return h


def statements_and_material(ctx):
    tl = ctx["timeline"]
    if not tl:
        return "<p>No timeline is held for this subject.</p>"
    lanes = {k: v.get("label", k) for k, v in (tl.get("lanes") or {}).items()}
    tsrc = tl.get("sources") or {}
    url2id = {s.get("url"): sid for sid, s in ctx["man"].items() if s.get("url")}   # timeline source ids are their own namespace; the URL joins them to the manifest
    rows = []
    for ev in tl.get("events") or []:
        nd = ctx["nodes"].get(ev.get("node")) if ev.get("node") else None
        t = ev.get("time") or (str(nd.get("time")) if nd else "")
        label = ev.get("label") or (nd.get("label") if nd else ev.get("id"))
        kind = ev.get("kind") or (nd.get("type") if nd else "")
        track = {"official": "Statement", "data": "Material", "witness": "Witness account", "media": "Report"}.get(kind, kind or "Record")
        srcs = ev.get("sources") or []
        def _tl(s):
            if s not in tsrc:
                return E(s)
            mid = url2id.get(tsrc[s]["url"])
            return f'<a href="#{E(mid)}">{E(SQ(tsrc[s]["title"]))}</a>' if mid else f'<a href="{E(tsrc[s]["url"])}">{E(SQ(tsrc[s]["title"]))}</a>'
        links = "; ".join(_tl(s) for s in srcs)
        if not links and nd:
            links = "shared node " + E(ev.get("node")) + ": " + "; ".join(f'<a href="{E(x["url"])}">{E(SQ(x["title"]))}</a>' if x.get("url") else E(SQ(x.get("title"))) for x in (nd.get("sources") or []))
        alt = f'<br><span class="small">second time: {E(ev["alt_time"])}: {E(SQ(ev.get("alt_note")))}</span>' if ev.get("alt_time") else ""
        rows.append((t, f'<tr><td>{E(t.replace("T", " ").replace(":00Z", "Z") if isinstance(t, str) else t)}<br><span class="small">{E(ev.get("precision", ""))}</span></td><td>{E(track)}</td><td>{E(lanes.get(ev.get("lane"), ev.get("lane")))}</td>'
                     f'<td>{E(SQ(label))}{alt}</td><td>{E(ev.get("status", ""))}</td><td class="small">{links}</td></tr>'))
    rows.sort(key=lambda x: str(x[0]))
    return ('<p class="small">Event times as stated by the sources (UTC). A statement is shown beside the material it can be checked against; a statement is adoption-class until material backs it (docs/NEWS_REVIEW.md).</p>'
            '<table class="media"><colgroup><col style="width:13%"><col style="width:10%"><col style="width:14%"><col style="width:27%"><col style="width:10%"><col style="width:26%"></colgroup><thead><tr><th>When (UTC)</th><th>Track</th><th>Who</th><th>What</th><th>Status</th><th>Source</th></tr></thead><tbody>' + "".join(r for _, r in rows) + "</tbody></table>")


def conflicts_section(ctx):
    out = ""
    tl = ctx["timeline"] or {}
    dis = [e for e in tl.get("events") or [] if e.get("status") == "disputed" or e.get("alt_time")]
    if dis:
        out += "<h3>Disputed or double-timed events (timeline)</h3><ul>" + "".join(
            f'<li><b>{E(e.get("label") or e.get("id"))}</b> ({E(e.get("time"))}){(" second time " + E(e["alt_time"]) + ": " + E(SQ(e.get("alt_note")))) if e.get("alt_time") else ""} {E(SH(e.get("detail"), 400))}</li>' for e in dis) + "</ul>"
    cont = [c for c in ctx["claims"] if c.get("state") == "contested" or c.get("disputed_by")]
    if cont:
        out += "<h3>Contested claims</h3><ul>" + "".join(f'<li><a href="#{E(c["id"])}">{E(c["id"])}</a>: ' + "; ".join(f'{E(d.get("who"))}: {E(SQ(d.get("position")))}' for d in c.get("disputed_by") or []) + "</li>" for c in cont) + "</ul>"
    m = ctx["media"]
    if m:
        topics = {t["id"]: t for t in m.get("topics") or []}
        sm, root = origin_map(m)
        rows = ""
        for tid, t in topics.items():
            vals = {}
            for r in sorted((x for x in m["reports"] if not x.get("withdrawn")), key=lambda r: r["published"]):
                for s in r.get("says") or []:
                    if s["topic"] == tid:
                        v = vals.setdefault(s["value"], {"n": 0, "o": set(), "first": r["published"], "who": r.get("said_by")})
                        v["n"] += 1; v["o"].add(root(r["origin"]))
            if len(vals) >= 2:
                rows += (f'<tr><td><b>{E(t["label"])}</b><br><span class="small">{E(t["resolution"])}</span></td><td><ul class="l">' + "".join(
                    f'<li>{E(SH(v, 170))}<br><span class="small">first {E(d["first"].replace("T", " ").replace(":00Z", "Z"))}; {d["n"]} report(s), {len(d["o"])} origin(s); said by {E(SH(d["who"], 80))}</span></li>' for v, d in vals.items()) + "</ul></td></tr>")
        out += ('<h3>How each point was worded (media record)</h3><p class="small">Only points reported in two or more wordings or figures are listed. The dossier does not judge which wordings conflict: '
                'a difference may be a different slice of one event, a clock, a rewording or an early error. A difference between reports is something to resolve; it is not evidence of fabrication (docs/NEWS_REVIEW.md, guardrail 3). The same wire text counts once.</p><table><thead><tr><th>Point</th><th>Wordings in order of first appearance, with how many origins carry each</th></tr></thead><tbody>' + rows + "</tbody></table>")
    return out or "<p>No conflicts are recorded in the timeline or the claims.</p>"


def transmission_html(ctx):
    """The dig's own transmission record (transmission.yaml): how a claim spread, step by step. Spread is adoption, never evidence (X1, X3)."""
    tr = ctx["trans"]
    out = ""
    for ch in (tr or {}).get("chains") or []:
        out += (f'<h3>How a claim spread: {E(ch.get("title") or ch.get("id") or ch.get("about"))}</h3><p class="small">About {E(ch.get("about"))}. Spread is adoption, never evidence of the claim; '
                'where a step is dated by day only, the order inside the day is not known.</p><ol>' + "".join(
                    f'<li><b>{E(e.get("date"))}</b> ({E(e.get("precision"))}) {E(e.get("step"))}: {E(SQ(e.get("carrier")))}. <span class="small">Source {E(e.get("source"))}, read: {"yes" if e.get("read") in (True, "yes") else "no"}. {E(SQ(e.get("note")))}</span></li>'
                    for e in ch.get("events") or []) + "</ol>")
    return out


def media_timeline_html(ctx, with_strip=True):
    m = ctx["media"]
    tl = ctx["timeline"]
    out = ""
    if not m:
        out += ('<p class="small">No per-outlet media record is held for this subject (no <code>media.yaml</code>). What exists is shown below: the statements and material from the timeline, '
                'the transmission chain if there is one, and any "what was reported when" entry in the log. First appearance, in-place edits and spread by outlet cannot be shown without that record.</p>')
        return out + transmission_html(ctx)
    reps = sorted((r for r in m["reports"] if not r.get("withdrawn")), key=lambda r: r["published"])
    topics = {t["id"]: t for t in m["topics"]}
    sm, root = origin_map(m)
    # A: first appearance
    rows = ""
    for tid, t in topics.items():
        hits = [(r, s) for r in reps for s in r.get("says") or [] if s["topic"] == tid]
        if not hits:
            continue
        sure = [(r, s) for r, s in hits if s.get("version", "first" if not r.get("changed") else "unknown") == "first"]
        r0, s0 = (sure or hits)[0]
        earliest_any = hits[0][0]
        note = ""
        if sure and earliest_any is not r0 and earliest_any["published"] < r0["published"]:
            note = f'<br>An earlier page ({E(SH(earliest_any.get("outlet") or ctx["man"].get(earliest_any.get("source"), {}).get("title", ""), 50))}, {E(earliest_any["published"][11:16])}Z) carries this point but was rewritten in place, so its first wording cannot be recovered.'
        elif not sure:
            note = "<br>The only reports carrying it were rewritten in place: first wording not recoverable."
        origins = {root(r["origin"]) for r, _ in hits}
        who0 = r0.get("outlet") or ctx["man"].get(r0.get("source"), {}).get("title", r0.get("source"))
        rows += (f'<tr><td><b>{E(t["label"])}</b></td><td>{E(r0["published"].replace("T", " ").replace(":00Z", "Z"))}</td><td>{E(SH(who0, 70))}<br><span class="small">said by: {E(SH(r0.get("said_by"), 90))}</span>{note}</td>'
                 f'<td>{len(hits)} / {len(origins)}</td><td>{E(t["resolution"])}</td></tr>')
    out += ('<h3>Where each point first appeared</h3><table><colgroup><col style="width:22%"><col style="width:13%"><col style="width:42%"><col style="width:10%"><col style="width:13%"></colgroup><thead><tr><th>Point</th><th>First seen (UTC)</th><th>First report and who it cites</th><th>Reports / origins</th><th>Status</th></tr></thead><tbody>'
            + rows + '</tbody></table><p class="small">First seen = the earliest report we could open or see relayed with a time. Earlier items may exist in sources we could not open. A page time is the time of the story or entry, not of the statement.</p>')
    if with_strip and reps:
        out += strip_svg(reps, topics, root)
    # B: chronological
    out += '<h3>Reports in time order</h3><table class="media"><colgroup><col style="width:9%"><col style="width:23%"><col style="width:8%"><col style="width:9%"><col style="width:15%"><col style="width:36%"></colgroup><thead><tr><th>UTC</th><th>Outlet</th><th>Type</th><th>Opened</th><th>Said by</th><th>Said</th></tr></thead><tbody>'
    day = None
    for r in reps:
        d = r["published"][:10]
        if d != day:
            out += f'<tr><td colspan="6"><b>{d}</b></td></tr>'; day = d
        who = r.get("outlet") or ctx["man"].get(r.get("source"), {}).get("title", r.get("source"))
        link = r.get("url") or (addr(ctx, ctx["man"][r["source"]]) if r.get("source") in ctx["man"] else "")
        says = "".join(f'<li>{E(ctx_topic(topics, s["topic"]))}: {E(SQ(s["value"]))}{(" <span class=tag>[" + s["version"] + " version]</span>") if s.get("version") and s["version"] != "first" else ""}</li>' for s in r.get("says") or [])
        chg = "".join(f'<div class="chg">Changed after publication ({E(c["observed"].replace("T", " ").replace(":00Z", "Z"))}): {E(SQ(c["what"]))} <span class="tag">known from: {E(c["how_known"])}</span></div>' for c in r.get("changed") or [])
        urlhtml = ('<span class="url">' + E(link) + '</span>') if link else ""
        note = f'<div class="small">{E(SQ(r.get("note")))}</div>' if r.get("note") else ""
        out += (f'<tr id="{E(r["id"])}"><td>{E(r["published"][11:16])}Z<br><span class="small">{E(BASIS_WORD[r["basis"]])}</span></td><td>{E(SH(who, 80))}{urlhtml}<span class="small">{E(r["id"])} · origin {E(r["origin"])}'
                f'{(" · from " + E(r["derives_from"])) if r.get("derives_from") else ""}</span></td><td>{E(KIND_CODE[r["kind"]])}<br><span class="small">{E(KIND_WORD[r["kind"]])}</span></td><td>{E(ACCESS_WORD[r["access"]])}</td>'
                f'<td>{E(SH(r.get("said_by"), 100))}</td><td><ul class="l" style="margin:0">{says}</ul>{chg}{note}</td></tr>')
    out += "</tbody></table>"
    # C: in place changes
    ch = [(r, c) for r in reps for c in r.get("changed") or []]
    wd = [r for r in m["reports"] if r.get("withdrawn")]
    if wd:
        out += f'<h3>Report entries withdrawn from this record ({len(wd)})</h3><ul>' + "".join(f'<li>{E(r["id"])}: {E(SQ(r.get("withdrawn")))}</li>' for r in wd) + "</ul>"
    out += f'<h3>Changes made to reports after publication ({len(ch)} seen)</h3><p class="small">Only changes visible in the URL, a visible update note or page metadata are listed. Archived earlier versions could not be read, so what changed inside a page is often not known.</p><ul>'
    out += "".join(f'<li><b>{E(c["observed"].replace("T", " ").replace(":00Z", "Z"))}</b> {E(SH(r.get("outlet") or ctx["man"].get(r.get("source"), {}).get("title", r.get("source")), 70))}: {E(SQ(c["what"]))}</li>' for r, c in sorted(ch, key=lambda x: x[1]["observed"])) + "</ul>"
    return out + transmission_html(ctx)


def ctx_topic(topics, tid):
    return topics.get(tid, {}).get("label", tid)


def strip_svg(reps, topics, root):
    t0 = datetime.datetime(2026, 9, 30, 0, 0) if not reps else datetime.datetime.strptime(reps[0]["published"][:10], "%Y-%m-%d")
    t1 = datetime.datetime.strptime(reps[-1]["published"][:10], "%Y-%m-%d") + datetime.timedelta(days=1)
    W, L, rowh = 880, 250, 22
    span = (t1 - t0).total_seconds()
    tids = [t for t in topics if any(s["topic"] == t for r in reps for s in r.get("says") or [])]
    H = 28 + rowh * len(tids) + 14
    col = {"P": "#0F6E56", "O": "#1A1814", "W": "#8B6914", "A": "#6f6962", "L": "#4a7fb5", "F": "#993C1D", "B": "#555"}
    s = f'<svg class="strip" viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Reports by point and time, UTC"><title>Reports by point and time (UTC). Ring = first report of the point.</title>'
    d = t0
    while d <= t1:
        x = L + (d - t0).total_seconds() / span * (W - L - 10)
        s += f'<line x1="{x:.1f}" y1="14" x2="{x:.1f}" y2="{H-10}" stroke="#999" stroke-width=".5"/><text x="{x+2:.1f}" y="10">{d.strftime("%d %b")}</text>'
        d += datetime.timedelta(days=1)
    for i, tid in enumerate(tids):
        y = 28 + i * rowh + 8
        s += f'<text x="4" y="{y+3}">{E(SH(topics[tid]["label"], 46))}</text><line x1="{L}" y1="{y}" x2="{W-10}" y2="{y}" stroke="#ccc" stroke-width=".5"/>'
        first = True
        for r in reps:
            if any(x["topic"] == tid for x in r.get("says") or []):
                tt = datetime.datetime.strptime(r["published"], "%Y-%m-%dT%H:%M:%SZ")
                x = L + (tt - t0).total_seconds() / span * (W - L - 10)
                s += f'<circle cx="{x:.1f}" cy="{y}" r="3.2" fill="{col[KIND_CODE[r["kind"]]]}"><title>{E(r["published"])} {E(r.get("outlet") or r.get("source"))} ({KIND_CODE[r["kind"]]})</title></circle>'
                if first:
                    s += f'<circle cx="{x:.1f}" cy="{y}" r="6.5" fill="none" stroke="#993C1D" stroke-width="1.2"/>'; first = False
    s += "</svg>"
    key = " ".join(f'<span class="tag">{k} {v}</span>' for k, v in [("O", "original"), ("W", "wire"), ("A", "roundup"), ("L", "live entry"), ("F", "fact-check"), ("P", "statement")])
    return f'<p class="small">Each dot is one report that carries the point; the ringed dot is the first. {key}</p>' + s


def source_register(ctx):
    sm, root = origin_map(ctx["media"])
    out = ""
    ret = ctx["man_doc"].get("retrieved")
    for sid, s in ctx["man"].items():
        acc, _ = access_of(s)
        a = s.get("authenticity") or {}
        stored = s.get("stored_as")
        sha = sha256_file(os.path.join(ctx["sdir"], stored)) if stored else None
        org = ", ".join(sorted({root(o) for o in sm.get(sid, [])})) or "not recorded"
        cited = ctx["cited_by"].get(sid, [])
        out += (f'<div class="src claim" id="{E(sid)}"><p><b>{E(sid)}</b> {E(SQ(s.get("title")))}</p><div class="kv">'
                f'<b>Address</b><span>{E(addr(ctx, s))}</span><b>Kind of document</b><span>{E(SQ(s.get("document_class")))}</span>'
                f'<b>Access</b><span>{E(acc)} ({"opened here" if acc.startswith("read") else "not opened here"})</span>'
                f'<b>Authenticity</b><span>{E(auth_of(s))}</span>'
                f'<b>Origin</b><span>{E(org)} (copies of one origin count once; recorded only where a media record exists)</span>'
                f'<b>Retrieved or checked</b><span>{E(str(a.get("checked")) + " (date of the authenticity check)" if a.get("checked") else (str(ret) + " (one date for the whole manifest; no per-source date)" if ret else "not recorded"))}</span>'
                f'<b>Stored copy</b><span>{(E(stored) + "; sha256 " + sha + " (computed at build from the stored file)") if sha else "none stored"}</span>')
        pub = PS.pub_of(ctx["man"], sid)
        out += ('<b>Publication status</b><span>' + E(str(pub["status"]).replace("_", " ")) + (" " + E(pub.get("date")) if pub.get("date") else "") + (" (looked up " + E(pub["checked"]) + ")" if pub.get("checked") else "")
                + ((" " + E(SQ(pub.get("reason")))) if pub.get("reason") else "") + "</span>") if pub else '<b>Publication status</b><span>not looked up (silence here does not mean the source is free of a retraction or correction)</span>'
        if isinstance(a, dict) and a.get("provenance"):
            out += f'<b>Provenance</b><span>{E(SQ(a["provenance"]))}</span>'
        if isinstance(a, dict) and a.get("tests"):
            out += f'<b>Tests run</b><span>{E("; ".join(SQ(t) for t in a["tests"]))}</span>'
        if isinstance(a, dict) and a.get("tested_by"):
            out += f'<b>Tested by</b><span>{E(SQ(a["tested_by"]))}</span>'
        gaps = a.get("gaps") if isinstance(a, dict) else None
        if gaps:
            out += f'<b>Gaps</b><span>{E("; ".join(SQ(g) for g in gaps))}</span>'
        nxt = a.get("next_step") if isinstance(a, dict) else None
        if nxt:
            out += f'<b>Next step</b><span>{E(SQ(nxt))}</span>'
        if s.get("basis"):
            out += f'<b>Basis</b><span>{E(SQ(s["basis"]))}</span>'
        out += f'<b>Cited by</b><span>{(", ".join(f"<a href=#{E(c)}>{E(c)}</a>" for c in cited)) or "no claim"}</span></div></div>'
    return out


def unverified_section(ctx):
    out = ""
    gaps = [c for c in ctx["claims"] if c.get("state") == "searched_gap"]
    out += f"<h3>Open questions: searched gaps ({len(gaps)})</h3><ul>" + "".join(
        f'<li><a href="#{E(c["id"])}">{E(c["id"])}</a> ({E(c.get("confidence"))}): {E(SH(c.get("statement"), 260))}{(" <i>Next step:</i> " + E(SH(c["next_step"], 200))) if c.get("next_step") else ""}</li>' for c in gaps) + "</ul>"
    below = [c for c in ctx["claims"] if c.get("state") in ("established", "refuted") and (("no" if c.get("anchor_checked") is False else c.get("anchor_checked")) != "primary")]
    out += f"<h3>Established or refuted, but not read at primary level ({len(below)})</h3><ul>" + "".join(
        f'<li><a href="#{E(c["id"])}">{E(c["id"])}</a> (checked: {E("no" if c.get("anchor_checked") is False else c.get("anchor_checked"))}, {E(c.get("confidence"))}): {E(SH(c.get("exception"), 240))}</li>' for c in below) + "</ul>"
    unread = [s for s in ctx["man"].values() if access_of(s)[0] == "not read"]
    out += f"<h3>Sources listed but not read ({len(unread)})</h3><ul>" + "".join(f'<li><a href="#{E(s["id"])}">{E(s["id"])}</a>: {E(SQ(s.get("title")))} <span class="small">{E(SH((s.get("authenticity") or {}).get("basis") or s.get("basis") or "", 200))}</span></li>' for s in unread) + "</ul>"
    unchecked = [s for s in ctx["man"].values() if (s.get("authenticity") or {}).get("status") == "unchecked" and access_of(s)[1]]
    out += f"<h3>Read, but authenticity not checked ({len(unchecked)})</h3><ul>" + "".join(f'<li><a href="#{E(s["id"])}">{E(s["id"])}</a>: {E(SH(s.get("title"), 120))}</li>' for s in unchecked) + "</ul>"
    if ctx["media"]:
        bad = [r for r in ctx["media"].get("reports") or [] if r.get("source") in ctx["man"] and access_of(ctx["man"][r["source"]])[0] == "not read" and r.get("access") == "read"]
        if bad:
            out += ("<h3>Files that disagree (for the author to resolve)</h3><ul>" + "".join(
                f'<li>The media record ({E(r["id"])}) says <a href="#{E(r["source"])}">{E(r["source"])}</a> was read; the manifest says it was not.</li>' for r in bad) + "</ul>")
    items = (ctx["review"].get("open_items") or [])
    if items:
        out += "<h3>Open items recorded by the independent reviewer</h3><ol>" + "".join(f"<li>{E(SQ(i))}</li>" for i in items) + "</ol>"
    return out


def primary_records_list(ctx):
    """Sources a reader would need to obtain: every source listed but not read, and every primary-class or dataset source with no stored copy."""
    rows = ""
    for sid, s in ctx["man"].items():
        acc = access_of(s)[0]
        primary_class = SQ(s.get("document_class")).lower().startswith(("primary", "dataset"))
        if acc == "not read" or (primary_class and not s.get("stored_as")):
            cs = ctx["cited_by"].get(sid, [])
            rows += (f'<tr><td><a href="#{E(sid)}">{E(sid)}</a></td><td>{E(SH(s.get("title"), 100))}</td><td>{E(acc)}</td>'
                     f'<td>{E(", ".join(cs)) if cs else "no claim anchor lists it"}</td></tr>')
    return ('<p>Records a reader relying on a claim would need to obtain: sources listed but not read here, and primary-class sources with no stored copy. This lists records, not people.</p>'
            '<table><thead><tr><th>Source</th><th>Title</th><th>Access</th><th>Claims resting on it</th></tr></thead><tbody>' + rows + "</tbody></table>")


def log_section(ctx):
    out = '<p class="small">The log is append-only: an entry is never edited, except to remove personal data under SCHEMA N26 (then a new entry says so). Corrections are new entries.</p>'
    for e in ctx["log"]:
        out += f'<div class="claim" id="{E(e["id"])}"><p><b>{E(e["id"])}</b> <span class="small">{E(e.get("date"))}</span>{(" · redacts " + E(", ".join(e["redacts"]))) if e.get("redacts") else ""}</p><p>{E(SQ(e.get("entry")))}</p></div>'
    return out


def dossier_html(ctx):
    cl, info = ctx["claims_doc"], ctx["info"]
    asm = cl.get("assessment") or {}
    sm, root = origin_map(ctx["media"])
    basis = asm.get("basis") or []
    order = sorted(ctx["claims"], key=lambda c: (0 if c["id"] in basis else 1, STATE_ORDER.get(c.get("state"), 9)))
    n = {}
    for c in ctx["claims"]:
        n[c.get("state")] = n.get(c.get("state"), 0) + 1
    unread = sum(1 for s in ctx["man"].values() if access_of(s)[0] == "not read")
    need = sum(1 for c in ctx["claims"] if primary_needs(ctx, c))
    body = (f'<div class="dossier"><p class="eyebrow">Evidence dossier · {E(cl.get("event_status", ""))} · as of {E(cl.get("as_of", info.get("date", "")))}</p><h1>{E(cl.get("title"))}</h1>'
            '<div class="scope"><b>What this document is.</b> A record of what is claimed, by whom, when, on what evidence, and what has not been verified. It is generated from the project files; it adds no fact.<br>'
            '<b>What it is not.</b> It is not legal advice and states no legal conclusion. It says nothing about anyone\'s liability, intent or guilt. An accusation is shown as an accusation, attributed to who made it. ' + E(REQUIRED_NOTE) +
            '<br><b>Names.</b> The dossier names no one itself: it prints what the project files print, and the entry\'s guardrails (docs/NEWS_REVIEW.md) apply to those files first.</div>'
            + PS.notices_html(cl, ctx["man"]) +
            f'<h2>1. Position in one page</h2><p><b>{E(SQ(asm.get("question")))}</b></p><p>{E(SQ(asm.get("headline")))}</p><ul>' + "".join(f"<li>{E(k)}</li>" for k in asm.get("key_points") or []) + "</ul>"
            f'<div class="kv"><b>Claims</b><span>{len(ctx["claims"])}: ' + ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in sorted(n.items(), key=lambda kv: STATE_ORDER.get(kv[0], 9))) + '</span>'
            f'<b>Sources</b><span>{len(ctx["man"])} listed; {unread} not read here; {sum(1 for s in ctx["man"].values() if s.get("stored_as"))} stored in full or in part</span>'
            f'<b>Primary record needed</b><span>{need} of {len(ctx["claims"])} claims</span>'
            f'<b>Independent review</b><span>{E(ctx["review"].get("status", "none"))}, {E(ctx["review"].get("reviewed_on", ""))}</span>'
            f'<b>Generated</b><span>{E(info.get("date", ""))} from commit {E(info.get("commit", "unknown"))}</span></div>'
            '<h2>2. Contents</h2><ol class="small"><li>Position</li><li>Contents</li><li>Fact register: chain of evidence for each claim</li><li>Who said what, and when: statements against material</li><li>Conflicts and discrepancies</li>'
            '<li>Media timeline: who reported what, when, and how it changed</li><li>What we could not verify</li><li>Primary records to obtain</li><li>Source register: provenance</li><li>Log: what was known when</li><li>Method, limits and file fingerprints</li></ol>'
            '<h2 class="newpage">3. Fact register: chain of evidence for each claim</h2><p class="small">Ordered with the claims behind the headline assessment first. "Source checked" says whether the document itself was opened and read (primary), agreed across secondary sources, or not checked.</p>'
            + "".join(claim_card(ctx, c, sm, root) for c in order)
            + '<h2 class="newpage">4. Who said what, and when: statements against material</h2>' + statements_and_material(ctx)
            + '<h2 class="newpage">5. Conflicts and discrepancies</h2>' + conflicts_section(ctx)
            + '<h2 class="newpage">6. Media timeline: who reported what, when, and how it changed</h2>' + media_timeline_html(ctx)
            + '<h2 class="newpage">7. What we could not verify</h2>' + unverified_section(ctx)
            + '<h2>8. Primary records to obtain</h2>' + primary_records_list(ctx)
            + '<h2 class="newpage">9. Source register: provenance</h2>' + source_register(ctx)
            + '<h2 class="newpage">10. Log: what was known when</h2>' + log_section(ctx)
            + '<h2>11. Method, limits and file fingerprints</h2><ul><li>Times are UTC unless a line says otherwise. A page time is the time of a story, not of the statement it reports.</li>'
            '<li>Copied wire reports count once. A report is not evidence of what it reports; spread is adoption (docs/NEWS_REVIEW.md).</li>'
            '<li>Hashes below fingerprint the data files this document was generated from, so a later reader can show which version was used.</li></ul>'
            '<table><thead><tr><th>File</th><th>sha256</th></tr></thead><tbody>' + "".join(
                f'<tr><td>{E(f)}</td><td class="small">{E(sha256_file(os.path.join(ctx["sdir"], f)) or "absent")}</td></tr>' for f in ("claims.yaml", "sources/MANIFEST.yaml", "timeline.yaml", "transmission.yaml", "log.yaml", "media.yaml", "story.yaml")
                if os.path.exists(os.path.join(ctx["sdir"], f))) + "</tbody></table></div>")
    return body


# ---------- live story ----------
def reviewed_story(story, review):
    """The story as far as the independent reviewer has passed it (SR12): updates up to and including `story_through` in review.yaml.
    None when the reviewer has named no update: an unreviewed story is never published. Later updates are held back, not deleted."""
    through = (review or {}).get("story_through")
    ups = (story or {}).get("updates") or []
    ids = [u.get("id") for u in ups]
    if not story or through not in ids:
        return None
    return dict(story, updates=ups[: ids.index(through) + 1])



def _sentence_rows(story):
    """(update, paragraph index, sentence) for every body sentence, and the supersession map."""
    rows, sup = [], {}
    for u in story.get("updates") or []:
        for pi, p in enumerate(u.get("paragraphs") or []):
            for s in p.get("sentences") or []:
                rows.append((u, pi, s))
                if s.get("supersedes"):
                    sup[s["supersedes"]] = s
    return rows, sup


def _cites(s):
    return [(x["id"], x.get("mode") or s["mode"]) if isinstance(x, dict) else (x, s["mode"]) for x in s.get("claims") or []]


def _lnk(ctx, frag, text):
    """A link into the dossier when the dossier is published; plain text when it is kept private."""
    dh = ctx.get("dh")
    return f'<a href="{dh}#{E(frag)}">{text}</a>' if dh else text


def tag_for(ctx, s):
    parts = []
    for cid, m in _cites(s):
        c = ctx["by"].get(cid)
        if c:
            parts.append(_lnk(ctx, cid, f'{E(c["state"].replace("_", " "))}, {E(c["confidence"])}'))
    return '<span class="tag">[' + "; ".join(parts) + ']</span>'


def fmt_at(at):
    return datetime.datetime.strptime(at, "%Y-%m-%dT%H:%M:%SZ").strftime("%-d %b %Y %H:%M UTC")


def story_html(ctx, dossier_href="dossier/", log_corrections=None):
    """dossier_href=None when the dossier is not published: the story then carries no link into it."""
    ctx = dict(ctx, dh=dossier_href)
    st, cl = ctx["story"], ctx["claims_doc"]
    ups = st["updates"]
    last = ups[-1]
    rows, sup = _sentence_rows(st)
    live = [(u, pi, s) for u, pi, s in rows if s["id"] not in sup]
    allsent = {s["id"]: (u, s) for u, _, s in rows}
    h = (f'<p class="eyebrow">News Review · story{(" · " + E(cl["event_status"])) if cl.get("event_status") else ""}</p><h1>{E(last["headline"]["text"])}</h1>'
         f'<p class="small">Last updated <b>{E(fmt_at(last["at"]))}</b> · {len(ups)} updates · {len(rows)} sentences, each tied to a claim · <a href="#corrections">{sum(1 for _, _, s in rows if s.get("change") in ("corrected", "withdrawn"))} correction(s)</a> · '
         + (f'<a href="{dossier_href}">Evidence dossier</a>' if dossier_href else "no dossier link (kept private)") + '</p>'
         '<div class="banner"><b>How to read this.</b> This is a running story, written from the claims in the News Review entry. Every sentence names the claim it rests on and shows how sure the claim is. '
         'A sentence that says what someone said is not a finding; a sentence that says something is not known is not a hint. When a fact changes, the old sentence stays on the page, marked, and a dated update replaces it.</div>')
    # not known yet
    unk = [s for _, _, s in live if s["mode"] == "open"]
    h += '<h2>What is not known yet</h2><ul>' + "".join(f'<li>{E(s["text"])} {tag_for(ctx, s)}</li>' for s in unk) + "</ul>"
    # story so far
    h += '<h2>The story so far</h2>'
    cur_u = None
    for u, pi, s in rows:
        if u["id"] != cur_u:
            cur_u = u["id"]
            h += f'<p class="eyebrow" style="margin:1.4em 0 .2em"><a href="#{E(u["id"])}">{E(fmt_at(u["at"]))}</a> · {E(u["title"])}</p>'
        if s["id"] in sup:
            n = sup[s["id"]]
            nu = allsent[n["id"]][0]
            kind = n["change"]
            h += (f'<p class="sent chg" id="{E(s["id"])}"><del>{E(s["text"])}</del> <span class="flag">{E("changed: " + kind)}</span> '
                  f'<span class="small">{E(fmt_at(nu["at"]))}: {E(n["why"])} <a href="#{E(n["id"])}">See the new sentence</a>.</span></p>')
        else:
            extra = ""
            if s.get("supersedes"):
                extra = f' <span class="flag">{E("changed: " + s["change"])}</span> <span class="small">replaces <a href="#{E(s["supersedes"])}">{E(s["supersedes"])}</a></span>'
            if s.get("accusation"):
                extra += ' <span class="flag">accusation, not a finding</span>'
            if s.get("denies_target"):
                tg = "; ".join(SQ(ctx["by"][cid].get("refutes_target")) for cid, _ in _cites(s) if cid in ctx["by"] and ctx["by"][cid].get("state") == "refuted")
                extra += f' <span class="flag">denies: {E(tg)}</span>'
            cls = "sent corr" if s.get("change") in ("corrected", "withdrawn") else "sent"
            h += f'<p class="{cls}" id="{E(s["id"])}">{E(s["text"])} {tag_for(ctx, s)}{extra}</p>'
    # updates list
    h += '<h2>Updates</h2><ul class="l">'
    for u in reversed(ups):
        new = [s["id"] for uu, _, s in rows if uu["id"] == u["id"]]
        chg = [s for uu, _, s in rows if uu["id"] == u["id"] and s.get("supersedes")]
        h += (f'<li id="{E(u["id"])}"><b>{E(fmt_at(u["at"]))}</b> · {E(u["title"])}<br><span class="small">Headline then: {E(u["headline"]["text"])}<br>'
              f'{len(new)} sentence(s) added: {E(", ".join(new))}.' + ((" Changes: " + E(", ".join(f"{s['id']} replaces {s['supersedes']} ({s['change']})" for s in chg)) + ".") if chg else "") + "</span></li>")
    h += "</ul>"
    # corrections
    corr = [(u, s) for u, _, s in rows if s.get("change") in ("corrected", "withdrawn")]
    h += '<h2 id="corrections">Corrections</h2><p class="small">Visible and permanent. A correction is a new sentence; the old one stays on the page, struck through, with the reason. Corrections to the underlying record are in the project log.</p>'
    if corr:
        h += "<ul class=\"l\">" + "".join(
            f'<li><b>{E(fmt_at(u["at"]))}</b> · {E(s["change"])}: {E(s["why"])}<br><span class="small">Replaces <a href="#{E(s["supersedes"])}">{E(s["supersedes"])}</a>: <del>{E(allsent[s["supersedes"]][1]["text"])}</del></span></li>' for u, s in corr) + "</ul>"
    else:
        h += "<p>No correction to this story so far.</p>"
    for e in log_corrections or []:
        h += f'<p class="small"><b>{E(e["date"])} · log {E(e["id"])}</b> ({E(e["kind"])}): {E(e["text"])} {_lnk(ctx, e["id"], "Full entry")}</p>'
    # ledger
    h += ('<h2>Evidence ledger</h2><p class="small">One line per sentence. "Says" is what the sentence does with the claim: <i>attributes</i> (reports who said it), <i>open</i> (says it is not known) or <i>states</i> (our own conclusion, allowed only for our own judgments). '
          'A sentence cannot say more than its claim allows.</p><table><thead><tr><th>Sentence</th><th>Says</th><th>Claim</th><th>State, confidence</th><th>Source checked</th><th>Evidence class</th><th>Sources</th></tr></thead><tbody>')
    for u, _, s in rows:
        cs = _cites(s)
        for i, (cid, m) in enumerate(cs):
            c = ctx["by"][cid]
            chk = "no" if c.get("anchor_checked") is False else c.get("anchor_checked")
            srcs = (c.get("anchor") or {}).get("sources") or []
            links = " ".join(_lnk(ctx, x, E(x.replace("src-", ""))) for x in srcs[:6]) + (f" +{len(srcs) - 6}" if len(srcs) > 6 else "")
            nl = [(x.get("node") if isinstance(x, dict) else x) for x in (c.get("anchor") or {}).get("nodes") or []]
            if nl:   # a claim anchored on shared nodes shows them, so the ledger is never empty for a node-based dig
                links += (" " if links else "") + "nodes: " + " ".join(_lnk(ctx, x, E(x)) for x in nl[:4]) + (f" +{len(nl) - 4}" if len(nl) > 4 else "")
            now = f"{c['state']}/{c['confidence']}"
            drift = ""
            snap = u.get("claims_at_update", {}).get(cid)
            if snap and snap != now and s["id"] not in sup:
                drift = ' <span class="flag">claim has changed since</span>'
            h += (f'<tr><td>{(E(s["id"]) + "<br><span class=small>" + E(SH(s["text"], 70)) + "</span>" + ((" <span class=flag>superseded by " + E(sup[s["id"]]["id"]) + "</span>") if s["id"] in sup else "")) if i == 0 else ""}</td><td>{E(m)}</td><td>{_lnk(ctx, cid, E(cid))}</td>'
                  f'<td>{E(c["state"].replace("_", " "))}, {E(c["confidence"])}{drift}</td><td>{E(chk)}</td><td>{E(c.get("evidence_class"))}</td><td class="small">{links}</td></tr>')
    h += "</tbody></table>"
    reg = st.get("names") or {}
    h += ('<h2>Names used in this story</h2><p class="small">Every person, place, organisation and nationality the story uses is registered. '
          + ("No person is named." if not reg.get("people") else "People named: " + ", ".join(E(p["name"]) for p in reg["people"]) + ".")
          + " Places: " + E(", ".join(reg.get("places") or [])) + ". Organisations: " + E(", ".join(reg.get("organisations") or [])) + ".</p>")
    h += (f'<h2>Rules this story follows</h2><ul class="small"><li>Headline 70 to 95 characters, no percentages, no loaded words in our voice.</li><li>We do not name a suspect or a private individual. Accusations are attributed.</li>'
          '<li>Wire copies count once. A discrepancy between reports is a discrepancy to resolve, not evidence of fabrication.</li><li>Nothing here is a legal conclusion. Source: docs/NEWS_REVIEW.md.</li></ul>')
    return h


def log_correction_entries(ctx):
    """Whole log entries that open with CORRECTION(S): used on the story page instead of cutting the text at the first full stop."""
    out = []
    for e in ctx["log"]:
        t = SQ(e.get("entry"))
        if re.match(r"(CORRECTIONS?|REDACTION)\b", t):
            cut = t[:300]
            cut = cut[:cut.rfind(" ")] + " …" if len(t) > 300 else t
            out.append({"id": e["id"], "date": e["date"], "kind": "redaction" if t.startswith("REDACTION") else "correction", "text": cut})
    return out
`````

## Appendix C: `build/tools/story_rules.py` (new)

Rules SR1 to SR12, MR1 to MR7, D6. Pure functions of loaded YAML; `conformance.py` calls `check_story_files`, `check_story_history` and `check_media_history`.

`````python
"""Rules SR1-SR11 (story.yaml) and MR1-MR7 (media.yaml). Pure functions: they take loaded YAML and return
(errors, warnings) as lists of strings. conformance.py calls check_story_files() for each subject.
Proposed in docs/proposals/news-story-and-dossier-formats.md; nothing here decides a claim state."""
import re, datetime

MODES = ("states", "attributes", "open")
CHANGES = ("updated", "narrowed", "corrected", "withdrawn")
KINDS = ("original", "wire", "aggregator", "live_entry", "fact_check", "statement", "broadcast")
ACCESS = ("read", "summary", "relayed", "not_opened")
BASIS = ("metadata", "displayed", "relayed", "computed", "zone_unverified")
RESOLUTION = ("open", "resolved", "corrected")
HYPE = ["shocking", "horrific", "horrifying", "terrifying", "chilling", "bombshell", "stunning", "explosive", "stunned", "mayhem",
        "nightmare", "heroic", "miracle", "hero", "devastating", "outrage", "outrageous", "slams", "blasts", "exposed", "scandal"]
LOADED = ["terror", "terrorist", "terrorism", "jihadist", "islamist", "radical", "radicalised", "radicalized", "extremist",
          "hijack", "hijacker", "hijacking", "suicide", "false flag", "staged", "fabricated", "manufactured"]
UNKNOWN_RE = re.compile(r"\b(not|no|never|none|unknown|unresolved|unsettled|unclear|undecided|open|cannot)\b", re.I)
OPENERS = set("""The A An In On At By No Neither Both As It This That There These Those He She They We Some Several Many All Any One Two Three
Four Another Its Their His Her For From With Without After Before During Until While When Where Who What Which If But And Or Nor So Yet Reports Whether How Why
Early Later Today Yesterday Officials Passengers Trackers Sources""".split())


def _quote_stripped(t):
    return re.sub(r'["“][^"”]*["”]', " ", t)


def claim_state_key(c):
    return f'{c.get("state")}/{c.get("confidence")}'


def allowed_modes(c):
    """The strongest thing a sentence may do with this claim (SR3). Own-voice `states` is allowed only for the project's
    own judgments (statement_kind judgment), established or refuted, at moderate or high confidence, primary anchor read.
    A claim that records what a source said (statement_kind reported) can only be attributed; a gap can only be called open."""
    st, conf, kind = c.get("state"), c.get("confidence"), c.get("statement_kind")
    chk = c.get("anchor_checked")
    chk = "no" if chk is False else chk
    if st == "searched_gap":
        return {"open"}
    modes = {"open", "attributes"}
    if st in ("established", "refuted") and conf in ("high", "moderate") and kind == "judgment" and chk == "primary":
        modes.add("states")
    return modes


def _cites(s):
    """Normalise a sentence's `claims` list to [(id, mode)]."""
    out = []
    for x in s.get("claims") or []:
        if isinstance(x, dict):
            out.append((x.get("id"), x.get("mode") or s.get("mode")))
        else:
            out.append((x, s.get("mode")))
    return out


def _sentences(story):
    """Every sentence of every update, headlines included (each update carries the headline as it stood then)."""
    for u in story.get("updates") or []:
        h = u.get("headline")
        if isinstance(h, dict):
            yield u.get("id"), dict(h, _headline=True)
        for p in u.get("paragraphs") or []:
            for s in p.get("sentences") or []:
                yield u.get("id"), s


def register_tokens(reg):
    toks = set()
    for k in ("places", "organisations", "demonyms", "other"):
        for v in (reg or {}).get(k) or []:
            toks.update(re.findall(r"[A-Za-z][A-Za-z'’\-]*", str(v)))
    for p in (reg or {}).get("people") or []:
        toks.update(re.findall(r"[A-Za-z][A-Za-z'’\-]*", str(p.get("name", ""))))
    return {t.replace("’s", "").replace("'s", "") for t in toks} | toks


def unregistered_names(text, reg):
    toks = register_tokens(reg)
    bad = []
    for sent in re.split(r"(?<=[.!?;:])\s+", text):
        words = re.findall(r"[A-Za-z][A-Za-z'’\-]*", sent)
        for i, w in enumerate(words):
            if not w[0].isupper():
                continue
            base = w.replace("’s", "").replace("'s", "")
            if i == 0 and base in OPENERS:
                continue
            if base in toks or w in toks:
                continue
            bad.append(w)
    return sorted(set(bad))


def check_story(story, claims_by_id, manifest_ids, claims_doc=None):
    """story.yaml against claims.yaml. Returns (errors, warnings)."""
    E, W = [], []
    if not isinstance(story, dict):
        return ["story.yaml is not a mapping"], W
    reg = story.get("names") or {}
    # SR9 people register: naming a person needs the guardrail basis
    for p in reg.get("people") or []:
        n = p.get("name", "?")
        if not p.get("role"):
            E.append(f"SR9 person `{n}` in names.people has no `role`")
        by = p.get("named_by")
        also = p.get("also_named_by") or []
        if by not in manifest_ids:
            E.append(f"SR9 person `{n}`: `named_by` must be a manifest source id of an authority naming them")
        if len([a for a in also if a in manifest_ids]) < 2:
            E.append(f"SR9 person `{n}`: needs `also_named_by` with at least two manifest ids (guardrail 1, docs/NEWS_REVIEW.md)")
        if p.get("private") is True:
            E.append(f"SR9 person `{n}` is marked private: private individuals are never named")
    seen_s, seen_u, last_at = set(), set(), None
    all_s = {}
    for uid, s in _sentences(story):
        all_s[s.get("id") or uid] = s
    # updates: order, ids
    for u in story.get("updates") or []:
        uid = u.get("id")
        if uid in seen_u:
            E.append(f"SR2 duplicate update id `{uid}`")
        seen_u.add(uid)
        at = u.get("at")
        try:
            t = datetime.datetime.strptime(str(at), "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            E.append(f"SR2 update `{uid}`: `at` must be UTC like 2026-10-02T12:00:00Z")
            t = None
        if t and last_at and t < last_at:
            E.append(f"SR2 update `{uid}` is dated before the update above it: updates are appended in time order")
        last_at = t or last_at
        if not u.get("title"):
            E.append(f"SR2 update `{uid}` has no `title`")
        h = u.get("headline")
        if not isinstance(h, dict) or not h.get("text"):
            E.append(f"SR8 update `{uid}` has no `headline` with `text`")
        else:
            L = len(" ".join(str(h["text"]).split()))
            if not 70 <= L <= 95:
                E.append(f"SR8 update `{uid}` headline is {L} characters; it must be 70 to 95")
        for p in u.get("paragraphs") or []:
            if not p.get("sentences"):
                E.append(f"SR2 update `{uid}` has an empty paragraph")
    superseded = {}
    for uid, s in _sentences(story):
        sid = s.get("id") or uid
        where = f"{uid}/{sid}"
        if sid in seen_s:
            E.append(f"SR2 duplicate sentence id `{sid}`")
        seen_s.add(sid)
        text = " ".join(str(s.get("text", "")).split())
        mode = s.get("mode")
        if not text:
            E.append(f"SR1 {where}: empty sentence")
        if mode not in MODES:
            E.append(f"SR3 {where}: `mode` must be one of {', '.join(MODES)}")
            continue
        cites = _cites(s)
        if not cites:
            E.append(f"SR1 {where}: a sentence must cite at least one claim id (no sentence stands without a claim)")
        any_open = False
        for cid, m in cites:
            c = claims_by_id.get(cid)
            if c is None:
                E.append(f"SR1 {where}: cites `{cid}`, which is not a claim in this subject")
                continue
            if m not in MODES:
                E.append(f"SR3 {where}: mode for `{cid}` must be one of {', '.join(MODES)}")
                continue
            if m == "open":
                any_open = True
            if m == "states" and (c.get("state") == "refuted") != (s.get("denies_target") is True):
                E.append(f"SR3 {where}: a `states` sentence on a refuted claim must deny the claim's `refutes_target` (`denies_target: true`); `denies_target` is for refuted claims only")
            if m not in allowed_modes(c):
                E.append(f"SR3 {where}: says `{m}` on `{cid}`, which is {claim_state_key(c)} ({c.get('statement_kind')}) and allows only "
                         f"{'/'.join(sorted(allowed_modes(c)))}: a sentence cannot be stronger than its claim")
        if s.get("accusation") is True and mode != "attributes":
            E.append(f"SR3 {where}: an `accusation` sentence must be mode `attributes`: an accusation is not a finding")
        # SR4 text must match mode
        if mode == "attributes":
            who = s.get("attributed_to")
            if not who:
                E.append(f"SR4 {where}: mode `attributes` needs `attributed_to`")
            elif str(who).lower() not in text.lower():
                E.append(f"SR4 {where}: the text must name who said it (`attributed_to`: {who})")
        if mode == "states" and re.search(r"\b(says?|said|according to|reportedly|alleged(ly)?|claims?|claimed)\b", text, re.I):
            E.append(f"SR4 {where}: mode `states` cannot carry an attribution word; use `attributes`")
        if (mode == "open" or any_open) and not UNKNOWN_RE.search(text):
            E.append(f"SR4 {where}: an `open` sentence must say plainly that something is not known or not established")
        # SR7 style
        bare = _quote_stripped(text)
        if "%" in text or re.search(r"per ?cent", text, re.I):
            E.append(f"SR7 {where}: no percentages (SCHEMA N23)")
        for w in HYPE:
            if re.search(rf"\b{re.escape(w)}\b", bare, re.I):
                E.append(f"SR7 {where}: hype word `{w}` outside a quotation")
        for w in LOADED:
            if re.search(rf"\b{re.escape(w)}", bare, re.I):
                E.append(f"SR7 {where}: loaded word `{w}` only inside a quotation with attribution, never in our voice")
        if re.search(r"\b(\d[\d,]*|two|three|four|five|six|seven|eight|nine|ten|many|several|dozens?|hundreds?|thousands?|multiple)\s+(news\s+)?(outlets|media|reports|sources|publications|posts|accounts|articles)\b", bare, re.I):
            E.append(f"SR7 {where}: a count of outlets, reports or posts: repetition carries no weight (docs/GOVERNANCE.md); name the origin instead")
        # SR9 names
        for n in unregistered_names(text, reg):
            E.append(f"SR9 {where}: `{n}` is not in `names` (register every person, place, organisation and nationality the story uses)")
        # SR5 supersedes
        sup = s.get("supersedes")
        if sup:
            if s.get("change") not in CHANGES:
                E.append(f"SR5 {where}: `supersedes` needs `change` (one of {', '.join(CHANGES)})")
            if not s.get("why"):
                E.append(f"SR5 {where}: `supersedes` needs `why` (what changed, in a sentence)")
            if sup not in all_s:
                E.append(f"SR5 {where}: supersedes unknown sentence `{sup}`")
            elif sup in superseded:
                E.append(f"SR5 {where}: `{sup}` is already superseded by `{superseded[sup]}`")
            else:
                superseded[sup] = sid
                if sup == sid:
                    E.append(f"SR5 {where}: a sentence cannot supersede itself")
        elif s.get("change"):
            E.append(f"SR5 {where}: `change` without `supersedes`")
    # SR6: a live sentence is written against a claim state; if the claim has moved, say so (warning; the page flags it)
    for u in story.get("updates") or []:
        snap = u.get("claims_at_update") or {}
        # earlier headlines are history; only the headline now on the page is compared with the claims
        head = [{"sentences": [u.get("headline") or {}]}] if u is (story.get("updates") or [None])[-1] else []
        for p in head + list(u.get("paragraphs") or []):
            for s in p.get("sentences") or []:
                if s.get("id") in superseded:
                    continue
                for cid, _ in _cites(s):
                    c = claims_by_id.get(cid)
                    if not c:
                        continue
                    if cid not in snap:
                        E.append(f"SR6 update `{u.get('id')}`: `claims_at_update` has no entry for `{cid}`")
                    elif snap[cid] != claim_state_key(c):
                        W.append(f"SR6 `{s.get('id')}` was written when `{cid}` was {snap[cid]}; it is now {claim_state_key(c)}: "
                                 "add a dated update that supersedes or re-affirms the sentence (the page flags it meanwhile)")
    for sid, by in superseded.items():
        sup_u = next((u for u in story.get("updates") or [] if any(x.get("id") == by for p in u.get("paragraphs") or [] for x in p.get("sentences") or [])), None)
        old_u = next((u for u in story.get("updates") or [] if any(x.get("id") == sid for p in u.get("paragraphs") or [] for x in p.get("sentences") or [])), None)
        if sup_u and old_u and sup_u.get("at") <= old_u.get("at") and sup_u is not old_u:
            E.append(f"SR5 `{by}` supersedes `{sid}` but is not dated after it")
    return E, W


def check_media(media, claims_by_id, manifest_ids):
    E, W = [], []
    if not isinstance(media, dict):
        return ["media.yaml is not a mapping"], W
    if media.get("confers_weight") is not False:
        E.append("MR1 media.yaml must set `confers_weight: false` (a report is not evidence of what it reports)")
    topics = {t.get("id"): t for t in media.get("topics") or []}
    for tid, t in topics.items():
        if t.get("resolution") not in RESOLUTION:
            E.append(f"MR2 topic `{tid}`: `resolution` must be one of {', '.join(RESOLUTION)}")
        if t.get("resolution") == "resolved" and t.get("resolved_by") not in claims_by_id:
            E.append(f"MR2 topic `{tid}`: `resolved` needs `resolved_by` naming a claim in this subject")
        for cid in t.get("claims") or []:
            if cid not in claims_by_id:
                E.append(f"MR2 topic `{tid}`: unknown claim `{cid}`")
    ids, origins = set(), {r.get("origin") for r in media.get("reports") or []}
    for r in media.get("reports") or []:
        rid = r.get("id")
        if rid in ids:
            E.append(f"MR3 duplicate report id `{rid}`")
        ids.add(rid)
        if bool(r.get("source")) == bool(r.get("url")):
            E.append(f"MR3 report `{rid}`: give exactly one of `source` (a manifest id) or `url`")
        if r.get("source") and r["source"] not in manifest_ids:
            E.append(f"MR3 report `{rid}`: `source` `{r['source']}` is not in the manifest")
        if r.get("url") and not r.get("outlet"):
            E.append(f"MR3 report `{rid}`: a report given by `url` needs `outlet`")
        for k, allowed in (("kind", KINDS), ("access", ACCESS), ("basis", BASIS)):
            if r.get(k) not in allowed:
                E.append(f"MR3 report `{rid}`: `{k}` must be one of {', '.join(allowed)}")
        try:
            datetime.datetime.strptime(str(r.get("published")), "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            E.append(f"MR3 report `{rid}`: `published` must be UTC like 2026-09-30T06:57:00Z")
        if not r.get("origin"):
            E.append(f"MR4 report `{rid}`: needs `origin` (the underlying record; copies of one wire story share it)")
        if r.get("derives_from") and r["derives_from"] not in origins:
            E.append(f"MR4 report `{rid}`: `derives_from` `{r['derives_from']}` is not the origin of any report here")
        if "withdrawn" in r and not str(r.get("withdrawn") or "").strip():
            E.append(f"MR7 report `{rid}`: `withdrawn` must say why (a wrong entry is retired, never deleted)")
        if not r.get("said_by"):
            E.append(f"MR5 report `{rid}`: needs `said_by` (who is quoted or cited; `own reporting` if none)")
        for s in r.get("says") or []:
            if s.get("topic") not in topics:
                E.append(f"MR2 report `{rid}`: unknown topic `{s.get('topic')}`")
            if not s.get("value"):
                E.append(f"MR2 report `{rid}`: a `says` entry needs `value`")
            if s.get("version", "first") not in ("first", "rewritten", "unknown"):
                E.append(f"MR2 report `{rid}`: `version` must be first, rewritten or unknown")
            if s.get("version") and not r.get("changed"):
                W.append(f"MR2 report `{rid}`: `version` is only useful on a report with `changed` entries")
        for ch in r.get("changed") or []:
            if not ch.get("observed") or not ch.get("what") or not ch.get("how_known"):
                E.append(f"MR6 report `{rid}`: each `changed` entry needs `observed`, `what` and `how_known`")
        blob = " ".join(str(x) for x in (r.get("said_by"), r.get("note"))) + " ".join(str(s.get("value")) for s in r.get("says") or [])
        if "%" in blob:
            W.append(f"MR5 report `{rid}`: contains a percentage; keep it only if it is a quoted figure")
    return E, W


def check_story_files(sdir, claims_by_id, manifest_ids, loader):
    """Called by conformance.check_subject. Absent files are fine (no change for any dig without them)."""
    import os
    E, W = [], []
    sp, mp = os.path.join(sdir, "story.yaml"), os.path.join(sdir, "media.yaml")
    man = os.path.join(sdir, "sources", "MANIFEST.yaml")
    if os.path.exists(man):   # D6: `address_withheld` on a manifest entry needs a reason and an address
        for s_ in (loader(man) or {}).get("sources") or []:
            if "address_withheld" in s_ and (not str(s_.get("address_withheld") or "").strip() or not s_.get("url")):
                E.append(f"D6 source `{s_.get('id')}`: `address_withheld` needs a reason and the source needs a `url`")
    if os.path.exists(mp):
        e, w = check_media(loader(mp), claims_by_id, manifest_ids)
        E += e; W += w
    if os.path.exists(sp):
        if not os.path.exists(os.path.join(sdir, "log.yaml")):
            E.append("SR10 a story needs a log.yaml (corrections and the record of what was known when live there)")
        story = loader(sp)
        e, w = check_story(story, claims_by_id, manifest_ids)
        E += e; W += w
        rp = os.path.join(sdir, "review.yaml")   # SR12: the reviewer, not the author, says how far the story has been reviewed
        through = ((loader(rp) or {}).get("story_through") if os.path.exists(rp) else None)
        ids = [u.get("id") for u in (story or {}).get("updates") or []]
        if through is not None and through not in ids:
            E.append(f"SR12 review.yaml `story_through` names `{through}`, which is not an update in story.yaml")
        elif through is None:
            W.append("SR12 review.yaml has no `story_through`: the story is not published until the independent reviewer names the last update they passed")
        elif ids and ids[-1] != through:
            W.append(f"SR12 updates after `{through}` are held back from the site until the independent reviewer passes them (last update: `{ids[-1]}`)")
    return E, W


def check_story_history(old_story, new_story, redacted=()):
    """SR11: updates and sentences are append-only against a git ref. Returns errors. `redacted` is the set of update or sentence ids that a
    NEW log entry names in `redacts` (N26): an edit or removal of those, and only those, is allowed (personal data, owner's decision)."""
    E = []
    red = set(redacted or ())
    def flat(st):
        d = {}
        for uid, s in _sentences(st or {}):
            d[(uid, s.get("id"))] = s
        return d
    old, new = flat(old_story), flat(new_story)
    old_u = {u.get("id"): u for u in (old_story or {}).get("updates") or []}
    new_u = {u.get("id"): u for u in (new_story or {}).get("updates") or []}
    for uid, u in old_u.items():
        if uid in red:
            continue
        if uid not in new_u:
            E.append(f"SR11 update `{uid}` was removed (updates are append-only)")
        elif {k: v for k, v in new_u[uid].items() if k not in ("paragraphs",)} != {k: v for k, v in u.items() if k not in ("paragraphs",)}:
            E.append(f"SR11 update `{uid}` was edited (add a new update instead)")
    for k, s in old.items():
        if k[1] in red or k[0] in red:
            continue
        if k not in new:
            E.append(f"SR11 sentence `{k[1]}` was removed (supersede it in a new update)")
        elif new[k] != s:
            E.append(f"SR11 sentence `{k[1]}` was edited (supersede it in a new update; the old text stays)")
    return E


def check_media_history(old_media, new_media):
    """MR7: a report id present on the base ref may not disappear; a wrong entry is retired with `withdrawn: <reason>`."""
    old = {r.get("id") for r in (old_media or {}).get("reports") or []}
    new = {r.get("id") for r in (new_media or {}).get("reports") or []}
    return [f"MR7 report `{i}` was removed; retire it with `withdrawn: <reason>`" for i in sorted(old - new, key=str)]
`````

## Appendix D: `build/tools/test_story_dossier.py` (new)

`````python
#!/usr/bin/env python3
"""Tests for story.yaml / media.yaml rules (SR1-SR11, MR1-MR6 in build/tools/story_rules.py), the dossier and story rendering
(build/tools/dossier.py) and their interaction with publication status (PS3).

    python3 build/tools/test_story_dossier.py

Uses synthetic subjects in a temporary folder; touches no real dig. Includes the neutrality test: the same story pipeline run on a
politically charged subject and a technical one gives the same structure, the same rule results and the same page sections."""
import copy, os, re, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import yaml
import conformance as cf
import story_rules as R
import dossier as D


def claims(kind="reported", state="established", conf="high", chk="primary", cid="c-1", stmt="X was said."):
    return {cid: {"id": cid, "state": state, "confidence": conf, "statement_kind": kind, "anchor_checked": chk, "statement": stmt,
                  "evidence_class": "primary_text", "evidential_weight": 4, "adoption_weight": 3, "would_change_if": "x",
                  "anchor": {"type": "official-statements", "description": "d", "sources": ["src-a"]}}}


def sentence(sid="s-1", text="The agency says the valve failed.", mode="attributes", cl=("c-1",), who="The agency", **kw):
    s = {"id": sid, "text": text, "mode": mode, "claims": list(cl)}
    if mode == "attributes":
        s["attributed_to"] = who
    s.update(kw)
    return s


def story(sentences=None, at="2026-10-02T12:00:00Z", head=None, snap=None, extra_updates=()):
    head = head or {"id": "h-1", "text": "The agency says the valve failed; the cause of the failure is not yet known to anyone", "mode": "attributes", "attributed_to": "The agency", "claims": ["c-1"]}
    u = {"id": "u-1", "at": at, "title": "First report", "headline": head, "claims_at_update": snap or {"c-1": "established/high"},
         "paragraphs": [{"sentences": sentences or [sentence()]}]}
    return {"subject": "s", "names": {"people": [], "places": [], "organisations": ["The agency"], "demonyms": [], "other": []}, "updates": [u, *extra_updates]}


def errs(st, by=None, man=("src-a",)):
    e, w = R.check_story(st, by or claims(), set(man))
    return e


def has(es, code, frag=""):
    return any(x.startswith(code) and frag in x for x in es)


class StoryRules(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(errs(story()), [])

    def test_sr1_unknown_and_missing_claim(self):
        self.assertTrue(has(errs(story([sentence(cl=("nope",))])), "SR1", "not a claim"))
        self.assertTrue(has(errs(story([sentence(cl=())])), "SR1", "at least one claim"))

    def test_sr3_attribution_on_gap_and_states_on_reported(self):
        by = claims(state="searched_gap", conf="low", chk=False, kind="search_result")
        self.assertTrue(has(errs(story([sentence()], snap={"c-1": "searched_gap/low"}), by), "SR3", "cannot be stronger"))
        self.assertTrue(has(errs(story([sentence(mode="states", text="The valve failed.")]), claims()), "SR3", "cannot be stronger"))

    def test_sr3_states_allowed_only_for_our_own_judgment(self):
        by = claims(kind="judgment", conf="moderate")
        st = story([sentence(mode="states", text="The valve failed.")], snap={"c-1": "established/moderate"})
        st["updates"][0]["headline"]["claims"] = ["c-1"]
        self.assertFalse(has(errs(st, by), "SR3", "s-1"))
        low = claims(kind="judgment", conf="low")
        self.assertTrue(has(errs(story([sentence(mode="states", text="The valve failed.")], snap={"c-1": "established/low"}), low), "SR3"))
        unread = claims(kind="judgment", conf="high", chk="secondary")
        self.assertTrue(has(errs(story([sentence(mode="states", text="The valve failed.")]), unread), "SR3"))

    def test_sr3_states_on_a_refuted_claim_must_negate(self):
        by = claims(kind="judgment", state="refuted", conf="high")
        snap = {"c-1": "refuted/high"}
        self.assertTrue(has(errs(story([sentence(mode="states", text="The valve failed.")], snap=snap), by), "SR3", "denies_target"))
        self.assertFalse(has(errs(story([sentence(mode="states", text="The valve did not fail.", denies_target=True)], snap=snap), by), "SR3", "s-1"))
        est = claims(kind="judgment", conf="high")
        self.assertTrue(has(errs(story([sentence(mode="states", text="The valve failed.", denies_target=True)]), est), "SR3", "refuted claims only"))

    def test_sr3_accusation_must_be_attributed(self):
        self.assertTrue(has(errs(story([sentence(mode="open", text="Whether it failed is not known.", accusation=True)])), "SR3", "accusation"))

    def test_sr4_text_matches_mode(self):
        self.assertTrue(has(errs(story([sentence(who="The ministry")])), "SR4", "name who said it"))
        self.assertTrue(has(errs(story([sentence(mode="open", text="The valve failed.")])), "SR4", "not known"))
        by = claims(kind="judgment", conf="moderate")
        self.assertTrue(has(errs(story([sentence(mode="states", text="The agency says the valve failed.")], snap={"c-1": "established/moderate"}), by), "SR4", "attribution word"))

    def test_sr7_style(self):
        for text, frag in [("The agency says 40% of valves failed.", "percent"), ("The agency says the failure was shocking.", "hype"),
                           ("The agency says the failure was a terrorist act.", "loaded")]:
            self.assertTrue(has(errs(story([sentence(text=text)])), "SR7", frag), text)
        ok = sentence(text='The agency says the minister called it a "terrorist act".')
        self.assertFalse(has(errs(story([ok])), "SR7"))

    def test_sr7_no_count_of_outlets(self):
        self.assertTrue(has(errs(story([sentence(text="Five outlets say the agency says the valve failed.")])), "SR7", "count of outlets"))
        self.assertTrue(has(errs(story([sentence(text="The agency says the valve failed, as 12 reports repeat.")])), "SR7", "count of outlets"))
        self.assertFalse(has(errs(story([sentence(text='The agency says "five reports agree" about the valve.')])), "SR7", "count of outlets"), "inside a quotation it is the speaker's figure")

    def test_sr8_headline_length(self):
        for n, bad in [(69, True), (70, False), (95, False), (96, True)]:
            h = {"id": "h-1", "text": ("The agency says the valve failed " + "x" * 100)[:n].rstrip(), "mode": "attributes", "attributed_to": "The agency", "claims": ["c-1"]}
            h["text"] = h["text"].ljust(n, "x")[:n]
            self.assertEqual(has(errs(story(head=h)), "SR8", "characters"), bad, n)

    def test_sr9_names(self):
        self.assertTrue(has(errs(story([sentence(text="The agency says Pat Quill broke the valve.")])), "SR9", "not in `names`"))
        st = story([sentence(text="The agency says Pat Quill broke the valve.")])
        st["names"]["people"] = [{"name": "Pat Quill", "role": "technician"}]
        self.assertTrue(has(errs(st), "SR9", "named_by"))
        st["names"]["people"] = [{"name": "Pat Quill", "role": "technician", "named_by": "src-a", "also_named_by": ["src-a", "src-b"]}]
        self.assertTrue(has(errs(st, man=("src-a",)), "SR9", "at least two"))
        st["names"]["people"][0]["also_named_by"] = ["src-b", "src-c"]
        self.assertEqual(errs(st, man=("src-a", "src-b", "src-c")), [])
        st["names"]["people"][0]["private"] = True
        self.assertTrue(has(errs(st, man=("src-a", "src-b", "src-c")), "SR9", "private"))

    def test_sr6_drift_is_flagged_until_a_new_update_answers_it(self):
        st = story()
        by = claims(conf="moderate")
        self.assertTrue(has(R.check_story(st, by, {"src-a"})[1], "SR6", "now established/moderate"))
        self.assertFalse(has(errs(st, by), "SR6"), "a warning, not an error: the claim may legitimately move; SR3 still blocks a sentence that outruns it")
        later = {"id": "u-2", "at": "2026-10-02T13:00:00Z", "title": "Claim downgraded", "claims_at_update": {"c-1": "established/moderate"},
                 "headline": {"id": "h-2", "text": "The agency says the valve failed; the cause of the failure is not yet known to anyone", "mode": "attributes", "attributed_to": "The agency", "claims": ["c-1"]},
                 "paragraphs": [{"sentences": [sentence("s-2", supersedes="s-1", change="narrowed", why="The claim is now rated moderate.")]}]}
        st2 = story(extra_updates=[later])
        st2["updates"][0]["headline"]["claims"] = ["c-1"]
        w = R.check_story(st2, by, {"src-a"})[1]
        self.assertFalse(has(w, "SR6", "`s-2`"))
        self.assertFalse(has(w, "SR6", "`h-1`"), "an earlier headline is history: only the headline now on the page is compared with the claims")
        st3 = story(extra_updates=[dict(later, paragraphs=[{"sentences": [sentence("s-2", supersedes="s-1", change="narrowed", why="The claim is now rated moderate.")]}],
                                         headline=dict(later["headline"], text="The agency says the valve failed; the cause of the failure is not yet known to anyone at all"), claims_at_update={"c-1": "established/high"})])
        self.assertTrue(has(R.check_story(st3, by, {"src-a"})[1], "SR6", "`h-2`"), "the latest headline is checked against the current claim")

    def test_sr5_supersession(self):
        self.assertTrue(has(errs(story([sentence(supersedes="s-9", change="corrected", why="w")])), "SR5", "unknown sentence"))
        self.assertTrue(has(errs(story([sentence(supersedes="s-1", change="corrected", why="w")])), "SR5", "itself"))
        self.assertTrue(has(errs(story([sentence("s-1"), sentence("s-2", supersedes="s-1")])), "SR5", "needs `change`"))
        self.assertTrue(has(errs(story([sentence("s-1"), sentence("s-2", supersedes="s-1", change="corrected")])), "SR5", "needs `why`"))
        self.assertTrue(has(errs(story([sentence("s-1", change="corrected")])), "SR5", "without `supersedes`"))

    def test_sr2_update_order_and_ids(self):
        later = story(at="2026-10-02T11:00:00Z")["updates"][0]
        later = dict(later, id="u-2", headline=dict(later["headline"], id="h-2"), paragraphs=[{"sentences": [sentence("s-2")]}])
        self.assertTrue(has(errs(story(extra_updates=[later])), "SR2", "time order"))
        self.assertTrue(has(errs(story(at="2026-10-02 12:00")), "SR2", "UTC"))

    def test_sr11_history_is_append_only(self):
        old = story()
        self.assertEqual(R.check_story_history(old, copy.deepcopy(old)), [])
        edited = copy.deepcopy(old); edited["updates"][0]["paragraphs"][0]["sentences"][0]["text"] = "Changed."
        self.assertTrue(has(R.check_story_history(old, edited), "SR11", "edited"))
        removed = copy.deepcopy(old); removed["updates"][0]["paragraphs"][0]["sentences"].clear()
        self.assertTrue(has(R.check_story_history(old, removed), "SR11", "removed"))
        gone = copy.deepcopy(old); gone["updates"] = []
        self.assertTrue(has(R.check_story_history(old, gone), "SR11", "update `u-1` was removed"))
        grown = copy.deepcopy(old)
        grown["updates"][0]["paragraphs"][0]["sentences"].append(sentence("s-2"))
        self.assertEqual(R.check_story_history(old, grown), [])

    def test_a_dig_without_the_files_is_unchanged(self):
        d = tempfile.mkdtemp()
        self.assertEqual(R.check_story_files(d, {}, set(), cf.load), ([], []))


def media(**kw):
    m = {"subject": "s", "confers_weight": False, "topics": [{"id": "t-1", "label": "A point", "claims": ["c-1"], "resolution": "open"}],
         "reports": [{"id": "m-1", "source": "src-a", "kind": "statement", "access": "read", "published": "2026-09-30T06:57:00Z", "basis": "metadata",
                      "origin": "o-1", "said_by": "the agency", "says": [{"topic": "t-1", "value": "it failed"}]}]}
    m.update(kw)
    return m


def merrs(m):
    return R.check_media(m, claims(), {"src-a"})[0]


class MediaRules(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(merrs(media()), [])

    def test_mr1_confers_weight(self):
        self.assertTrue(has(merrs(media(confers_weight=True)), "MR1"))
        m = media(); del m["confers_weight"]
        self.assertTrue(has(merrs(m), "MR1"))

    def test_mr2_topics(self):
        m = media(); m["reports"][0]["says"][0]["topic"] = "t-9"
        self.assertTrue(has(merrs(m), "MR2", "unknown topic"))
        m = media(); m["topics"][0]["resolution"] = "resolved"
        self.assertTrue(has(merrs(m), "MR2", "resolved_by"))
        m["topics"][0]["resolved_by"] = "c-1"
        self.assertEqual(merrs(m), [])

    def test_mr3_report_shape(self):
        m = media(); m["reports"][0]["url"] = "https://x.test"; m["reports"][0]["outlet"] = "X"
        self.assertTrue(has(merrs(m), "MR3", "exactly one"))
        m = media(); m["reports"][0]["published"] = "30 Sep"
        self.assertTrue(has(merrs(m), "MR3", "UTC"))
        m = media(); m["reports"][0]["source"] = "src-zz"
        self.assertTrue(has(merrs(m), "MR3", "not in the manifest"))

    def test_mr4_origin(self):
        m = media(); del m["reports"][0]["origin"]
        self.assertTrue(has(merrs(m), "MR4", "origin"))
        m = media(); m["reports"][0]["derives_from"] = "nowhere"
        self.assertTrue(has(merrs(m), "MR4", "derives_from"))

    def test_mr5_6_said_by_and_changes(self):
        m = media(); del m["reports"][0]["said_by"]
        self.assertTrue(has(merrs(m), "MR5"))
        m = media(); m["reports"][0]["changed"] = [{"observed": "2026-10-01T00:00:00Z", "what": "edited"}]
        self.assertTrue(has(merrs(m), "MR6", "how_known"))


class MediaHistoryAndWithdrawal(unittest.TestCase):
    def test_mr7_history(self):
        old = media()
        self.assertEqual(R.check_media_history(old, copy.deepcopy(old)), [])
        self.assertTrue(has(R.check_media_history(old, media(reports=[])), "MR7", "removed"))
        w = media(); w["reports"][0]["withdrawn"] = "  "
        self.assertTrue(has(merrs(w), "MR7", "why"))
        w["reports"][0]["withdrawn"] = "The page was a mirror of m-2."
        self.assertEqual(merrs(w), [])

    def test_withdrawn_report_is_listed_and_not_counted(self):
        d, st, cl = subject_dir("technical")
        m = media(); m["reports"][0]["withdrawn"] = "Duplicate of another entry."
        yaml.safe_dump(m, open(os.path.join(d, "media.yaml"), "w"))
        h = D.media_timeline_html(D.load_ctx(d, cf.load))
        self.assertIn("withdrawn from this record (1)", h)
        self.assertNotIn("it failed", h.split("withdrawn from this record")[0].split("Reports in time order")[-1])


def subject_dir(kind):
    """A synthetic subject. kind 'charged' = a political accusation; 'technical' = an engineering question. Same structure."""
    d = tempfile.mkdtemp()
    os.makedirs(os.path.join(d, "sources"))
    if kind == "charged":
        q, head_claim, org = "Did the senator take the donation?", "A donation of 50 thousand dollars reached the senator's campaign in March, according to the filing.", "The campaign office"
    else:
        q, head_claim, org = "Did the bolt fail below its rated torque?", "A bolt failed at 40 newton metres, according to the test lab report.", "The test lab"
    cl = {"title": q, "headline": q, "event_status": "live", "as_of": "2026-10-02", "assessment": {"question": q, "answer": "unsettled", "headline": "h", "text": "t", "basis": ["c-1"], "would_settle": "w", "key_points": ["a", "b", "c"]},
          "claims": [claims(stmt=head_claim)["c-1"], claims(cid="c-2", state="searched_gap", conf="low", chk=False, kind="search_result", stmt="Why it happened is not known.")["c-2"]]}
    cl["claims"][1]["next_step"] = "n"
    yaml.safe_dump(cl, open(os.path.join(d, "claims.yaml"), "w"))
    yaml.safe_dump({"sources": [{"id": "src-a", "title": "A record", "url": "https://example.test/a", "document_class": "primary_text", "read": "yes, directly",
                                 "authenticity": {"status": "authenticated", "strength": "moderate", "provenance": "p", "tests": ["t"]}}]}, open(os.path.join(d, "sources", "MANIFEST.yaml"), "w"))
    yaml.safe_dump({"log": [{"id": "L-1", "date": "2026-10-02", "entry": "CORRECTION: an earlier entry gave the wrong month. The month is March."}]}, open(os.path.join(d, "log.yaml"), "w"))
    st = {"subject": "s", "names": {"people": [], "places": [], "organisations": [org], "demonyms": [], "other": []},
          "updates": [{"id": "u-1", "at": "2026-10-02T12:00:00Z", "title": "First report", "claims_at_update": {"c-1": "established/high", "c-2": "searched_gap/low"},
                       "headline": {"id": "h-1", "text": f"{org} says the record is as filed; the reason is not yet known to anyone", "mode": "attributes", "attributed_to": org, "claims": ["c-1", {"id": "c-2", "mode": "open"}]},
                       "paragraphs": [{"sentences": [{"id": "s-1", "mode": "attributes", "attributed_to": org, "text": f"{org} says the record is as filed.", "claims": ["c-1"]},
                                                     {"id": "s-2", "mode": "open", "text": "Why it happened is not known.", "claims": ["c-2"]}]}]}]}
    yaml.safe_dump(st, open(os.path.join(d, "story.yaml"), "w"))
    return d, st, cl


class Neutrality(unittest.TestCase):
    def test_same_rules_same_structure(self):
        outs = {}
        for kind in ("charged", "technical"):
            d, st, cl = subject_dir(kind)
            by = {c["id"]: c for c in cl["claims"]}
            self.assertEqual(R.check_story(st, by, {"src-a"}), ([], []), kind)
            ctx = D.load_ctx(d, cf.load)
            dos, sto = D.dossier_html(ctx), D.story_html(ctx, log_corrections=D.log_correction_entries(ctx))
            outs[kind] = (re.findall(r"<h2[^>]*>(.*?)</h2>", dos), re.findall(r"<h2[^>]*>(.*?)</h2>", sto))
            # the same defect is caught the same way in both
            bad = copy.deepcopy(st); bad["updates"][0]["paragraphs"][0]["sentences"][1]["mode"] = "attributes"
            bad["updates"][0]["paragraphs"][0]["sentences"][1]["attributed_to"] = "Someone"
            self.assertTrue(has(R.check_story(bad, by, {"src-a"})[0], "SR3", "cannot be stronger"), kind)
        self.assertEqual(outs["charged"], outs["technical"])


class Rendering(unittest.TestCase):
    def setUp(self):
        self.d, self.st, self.cl = subject_dir("technical")
        s2 = self.st["updates"][0]
        u2 = {"id": "u-2", "at": "2026-10-02T15:00:00Z", "title": "Correction", "claims_at_update": {"c-1": "established/high"},
              "headline": dict(s2["headline"], id="h-2"), "paragraphs": [{"sentences": [{"id": "s-3", "supersedes": "s-1", "change": "corrected", "why": "The lab corrected the figure.",
                                                                                         "mode": "attributes", "attributed_to": "The test lab", "text": "The test lab says the record is as filed, corrected.", "claims": ["c-1"]}]}]}
        self.st["updates"].append(u2)
        self.st["updates"][0]["headline"]["claims"] = ["c-1", {"id": "c-2", "mode": "open"}]
        yaml.safe_dump(self.st, open(os.path.join(self.d, "story.yaml"), "w"))
        self.ctx = D.load_ctx(self.d, cf.load)

    def test_story_shows_changed_marks_and_correction(self):
        h = D.story_html(self.ctx, log_corrections=D.log_correction_entries(self.ctx))
        self.assertIn("<del>The test lab says the record is as filed.</del>", h)
        self.assertIn("changed: corrected", h)
        self.assertIn('id="corrections"', h)
        self.assertIn("The lab corrected the figure.", h)
        self.assertEqual(h.count("<h1>"), 1)

    def test_log_correction_is_whole_not_cut_at_a_full_stop(self):
        d, st, cl = subject_dir("technical")
        ctx = D.load_ctx(d, cf.load)
        e = D.log_correction_entries(ctx)[0]
        self.assertIn("The month is March.", e["text"])

    def test_no_data_download_and_no_legal_conclusion_words(self):
        dos = D.dossier_html(self.ctx)
        sto = D.story_html(self.ctx)
        for h in (dos, sto):
            self.assertIsNone(re.search(r'href="(?!https?://)[^"]*\.(yaml|yml|json|csv|pdf)"', h), "no link to a data file of ours; third-party source addresses are shown as given")
            self.assertNotRegex(h.lower(), r"download")
        fixed = re.sub(r"<[^>]+>", " ", re.sub(r'<div class="scope">.*?</div>', "", dos, flags=re.S))   # the scope box disclaims these words; it is the one place they appear
        for w in ("liable", "liability", "defam", "guilty", "unlawful", "illegal", "negligen", "culpab", "fraud"):
            self.assertNotIn(w, fixed.lower(), w)
        self.assertIn("not legal advice", dos)

    def test_dossier_flags_primary_record_and_hash(self):
        os.makedirs(os.path.join(self.d, "sources"), exist_ok=True)
        open(os.path.join(self.d, "sources", "a.txt"), "w").write("text")
        m = yaml.safe_load(open(os.path.join(self.d, "sources", "MANIFEST.yaml")))
        m["sources"][0]["stored_as"] = "sources/a.txt"
        yaml.safe_dump(m, open(os.path.join(self.d, "sources", "MANIFEST.yaml"), "w"))
        ctx = D.load_ctx(self.d, cf.load)
        dos = D.dossier_html(ctx)
        self.assertIn(D.sha256_file(os.path.join(self.d, "sources", "a.txt")), dos)
        self.assertIn("primary record needed", dos)   # c-2 is a searched gap
        self.assertIn("primary text read", dos)       # c-1 is primary

    def test_sr11_redaction_exception_only_for_a_named_id(self):
        old = copy.deepcopy(self.st); new = copy.deepcopy(self.st)
        new["updates"][0]["paragraphs"][0]["sentences"][0]["text"] = "[text redacted]"
        self.assertTrue(has(R.check_story_history(old, new), "SR11", "edited"))
        self.assertEqual(R.check_story_history(old, new, redacted={"s-1"}), [], "a new log entry names s-1 in `redacts`: N26")
        self.assertTrue(has(R.check_story_history(old, new, redacted={"s-9"}), "SR11", "edited"), "an unrelated id does not open the exception")

    def test_sr12_story_is_published_only_as_far_as_the_reviewer_passed_it(self):
        st = self.st
        self.assertIsNone(D.reviewed_story(st, {}), "no story_through: nothing is published")
        self.assertIsNone(D.reviewed_story(st, {"story_through": "u-9"}))
        r = D.reviewed_story(st, {"story_through": "u-1"})
        self.assertEqual([u["id"] for u in r["updates"]], ["u-1"], "the later update (the correction) is held back until it is passed")
        self.assertEqual(len(self.st["updates"]), 2, "held back, not deleted")
        yaml.safe_dump({"status": "passed", "story_through": "u-9"}, open(os.path.join(self.d, "review.yaml"), "w"))
        e, w = R.check_story_files(self.d, {"c-1": {}, "c-2": {}}, {"src-a"}, cf.load)
        self.assertTrue(has(e, "SR12", "names `u-9`") or any(x.startswith("SR12") and "u-9" in x for x in e))
        yaml.safe_dump({"status": "passed", "story_through": "u-1"}, open(os.path.join(self.d, "review.yaml"), "w"))
        e, w = R.check_story_files(self.d, {"c-1": {}, "c-2": {}}, {"src-a"}, cf.load)
        self.assertTrue(any("held back" in x for x in w))

    def test_d6_address_withheld_in_public_dossier_only(self):
        mp = os.path.join(self.d, "sources", "MANIFEST.yaml")
        m = yaml.safe_load(open(mp))
        m["sources"][0]["url"] = "https://example.org/news/captain-jane-doe-honoured/1"
        m["sources"][0]["address_withheld"] = "the path contains a victim's name"
        yaml.safe_dump(m, open(mp, "w"))
        pub = D.dossier_html(D.load_ctx(self.d, cf.load, build_info={"date": "x", "commit": "y"}))
        self.assertNotIn("jane-doe", pub)
        self.assertIn("path withheld", pub)
        priv = D.dossier_html(D.load_ctx(self.d, cf.load, build_info={"date": "x", "commit": "y", "private": True}))
        self.assertIn("jane-doe", priv, "a private dossier prints the full address: a lawyer needs it")
        m["sources"][0]["address_withheld"] = ""
        yaml.safe_dump(m, open(mp, "w"))
        e, _ = R.check_story_files(self.d, {"c-1": {}, "c-2": {}}, {"src-a"}, cf.load)
        self.assertTrue(has(e, "D6", "needs a reason"))

    def test_deterministic(self):
        a = D.dossier_html(D.load_ctx(self.d, cf.load, build_info={"date": "x", "commit": "y"}))
        b = D.dossier_html(D.load_ctx(self.d, cf.load, build_info={"date": "x", "commit": "y"}))
        self.assertEqual(a, b)

    def test_without_media_file_says_so(self):
        h = D.media_timeline_html(self.ctx)
        self.assertIn("No per-outlet media record is held", h)


class PublicationStatusInteraction(unittest.TestCase):
    def test_a_retracted_source_named_in_media_yaml_is_not_a_ps3_hit(self):
        d, st, cl = subject_dir("technical")
        m = yaml.safe_load(open(os.path.join(d, "sources", "MANIFEST.yaml")))
        m["sources"][0]["publication"] = {"status": "retracted", "date": "2026-01-01", "notice": "https://example.test/n"}
        yaml.safe_dump(m, open(os.path.join(d, "sources", "MANIFEST.yaml"), "w"))
        cl["claims"][0]["flagged_sources"] = ["src-a"]
        cl["source_notices"] = [{"source": "src-a", "notice": "retracted"}]
        yaml.safe_dump(cl, open(os.path.join(d, "claims.yaml"), "w"))
        yaml.safe_dump(media(), open(os.path.join(d, "media.yaml"), "w"))
        r = cf.Report()
        cf.check_publication(r, "s", d, cl["claims"], cl, nodes_dir=tempfile.mkdtemp())
        self.assertEqual([e for e in r.errors if "media.yaml" in e or "story.yaml" in e], [])

    def test_the_dossier_shows_a_retraction_and_says_when_a_source_was_not_looked_up(self):
        d, st, cl = subject_dir("technical")
        mp = os.path.join(d, "sources", "MANIFEST.yaml")
        m = yaml.safe_load(open(mp))
        m["sources"][0]["publication"] = {"status": "retracted", "date": "2026-01-01", "checked": "2026-10-02", "reason": "data fabricated"}
        m["sources"].append({"id": "src-b", "title": "Another record", "url": "https://example.test/b", "document_class": "primary_text", "read": "yes, directly",
                             "authenticity": {"status": "unchecked"}})
        yaml.safe_dump(m, open(mp, "w"))
        cl["claims"][0]["flagged_sources"] = ["src-a"]
        cl["source_notices"] = [{"source": "src-a", "notice": "This source was retracted."}]
        yaml.safe_dump(cl, open(os.path.join(d, "claims.yaml"), "w"))
        h = D.dossier_html(D.load_ctx(d, cf.load))
        self.assertIn("Retracted source", h)
        self.assertIn("This source was retracted.", h)
        self.assertIn("<b>Publication status</b><span>retracted 2026-01-01", h)
        self.assertIn("not looked up (silence here does not mean", h, "src-b has no publication block: silence is not shown as clean")


if __name__ == "__main__":
    unittest.main(verbosity=1)
`````

## Appendix E: `build/subjects/flydubai-fz1073/story.yaml` (worked example, new, not published text)

`````yaml
# story.yaml: the running story for a News Review entry (format: build/SCHEMA.md, rules SR1 to SR12).
# WORKED EXAMPLE for flydubai-fz1073, written for the proposal. Update times are illustrative (the project log carries dates, not times);
# the correction in u-003 reproduces a real one (log L-03(a), corrected in L-17); u-004 reproduces L-26 items 2 and 3 (the Saudi text read at source). Not published text.
subject: flydubai-fz1073

names:                       # SR9: every person, place, organisation and nationality the story uses. No person is named in this story.
  people: []
  places: [Dubai, Tel Aviv, Tabuk, Saudi Arabia, Israel, Oman]
  organisations: [Flydubai, UAE, AirNav Radar, CNN, Al Jazeera, Saudi]
  demonyms: [Israeli, Omani, Saudi, English]
  other: [FZ1073, UTC, ET, GMT, ADS-B, Attorney-General, Prime Minister, October, September, Islamist]   # Islamist: a word inside a quotation

updates:
  - id: u-001
    at: "2026-10-02T12:00:00Z"
    title: "What is reported so far"
    headline:
      id: h-001
      text: "Flydubai FZ1073: airline and UAE report an altercation in the flight deck; cause not yet known"
      mode: attributes
      attributed_to: "airline and UAE"
      claims: [fz1073-diverted-tabuk, {id: fz1073-motive-not-established, mode: open}]
    claims_at_update:
      fz1073-diverted-tabuk: established/high
      fz1073-crew-and-passengers-secured-aircraft: established/high
      fz1073-both-pilots-injured: established/moderate
      fz1073-israel-says-omani: established/moderate
      fz1073-omani-nationality-unconfirmed: searched_gap/low
      fz1073-no-findings-yet: searched_gap/low
      fz1073-motive-not-established: searched_gap/low
      fz1073-motive-statements: established/moderate
    paragraphs:
      - sentences:
          - id: s-001
            mode: attributes
            attributed_to: "Flydubai and the UAE foreign ministry"
            text: 'Flydubai and the UAE foreign ministry say flight FZ1073 from Dubai to Tel Aviv was diverted to Tabuk, Saudi Arabia, on 30 September after "an altercation" in the flight deck.'
            claims: [fz1073-diverted-tabuk]
          - id: s-002
            mode: attributes
            attributed_to: "The airline"
            text: "The airline says on-duty Flydubai crew travelling on the flight secured the aircraft and landed it, and that everyone aboard is safe."
            claims: [fz1073-crew-and-passengers-secured-aircraft, fz1073-diverted-tabuk]
          - id: s-003
            mode: attributes
            attributed_to: "The Saudi interior ministry"
            text: 'The Saudi interior ministry says its preliminary investigations "revealed an assault on the captain by the co-pilot, resulting in various injuries to both".'
            claims: [fz1073-both-pilots-injured]
      - sentences:
          - id: s-004
            mode: attributes
            attributed_to: "Israel's Prime Minister and an Israeli official"
            text: "Israel's Prime Minister and an Israeli official say the co-pilot is an Omani national; no UAE, Saudi, Flydubai or Omani authority had confirmed it on the record by 2 October."
            claims: [fz1073-israel-says-omani]
          - id: s-005
            mode: open
            text: "Whether the co-pilot is an Omani national, and whether he holds another nationality, is not confirmed by any authority that is not Israeli."
            claims: [fz1073-omani-nationality-unconfirmed]
      - sentences:
          - id: s-006
            mode: open
            text: "As of 2 October no investigation finding, recorder result, preliminary report, charge or court record has been published."
            claims: [fz1073-no-findings-yet]
          - id: s-007
            mode: open
            text: "No investigating authority has established a motive, an affiliation or any direction by a third party."
            claims: [fz1073-motive-not-established]
          - id: s-008
            mode: attributes
            accusation: true
            attributed_to: "Israel's Prime Minister"
            text: 'Israel''s Prime Minister said on 1 October that the co-pilot "underwent Islamist radical indoctrination"; the airline says the motive is unknown, and the UAE says it is examining all motives.'
            claims: [fz1073-motive-statements]

  - id: u-002
    at: "2026-10-02T15:00:00Z"
    title: "Landing time and descent figures"
    headline:
      id: h-002
      text: "Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; landing, descent unsettled"
      mode: attributes
      attributed_to: "Saudi ministry"
      claims: [fz1073-both-pilots-injured, {id: fz1073-flight-times, mode: open}]
    claims_at_update:
      fz1073-both-pilots-injured: established/moderate
      fz1073-flight-times: established/moderate
      fz1073-descent-magnitude: searched_gap/low
    paragraphs:
      - sentences:
          - id: s-009
            mode: attributes
            attributed_to: "The Saudi interior ministry and Tabuk airport"
            text: "The Saudi interior ministry and Tabuk airport say the aircraft landed at 06:45 UTC (9:45 a.m. local); AirNav Radar's blog says it landed safely at Tabuk, with its last ADS-B message at about 06:58 UTC."
            claims: [fz1073-flight-times]
          - id: s-010
            mode: open
            text: "How far and how fast the aircraft descended is not settled: reports give figures from 14,000 ft in under 30 seconds to 17,400 ft in just under two minutes."
            claims: [fz1073-descent-magnitude]
          - id: s-011
            mode: attributes
            attributed_to: "CNN"
            text: "CNN gave the departure as 6:05 a.m. local time, which differs from the trackers' 03:05 UTC."
            claims: [fz1073-flight-times]

  - id: u-003
    at: "2026-10-02T18:30:00Z"
    title: "Correction: CNN's departure time"
    headline:
      id: h-003
      text: "Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; landing, descent unsettled"
      mode: attributes
      attributed_to: "Saudi ministry"
      claims: [fz1073-both-pilots-injured, {id: fz1073-flight-times, mode: open}]
    claims_at_update:
      fz1073-both-pilots-injured: established/moderate
      fz1073-flight-times: established/moderate
    paragraphs:
      - sentences:
          - id: s-012
            supersedes: s-011
            change: corrected
            why: "The earlier sentence called CNN's 6:05 a.m. a different time from the trackers'. CNN's other times are on the UTC+3 clock, so 6:05 a.m. is 03:05 UTC; only CNN's ET figure is wrong (log L-17)."
            mode: attributes
            attributed_to: "CNN"
            text: 'CNN gave the departure as 6:05 a.m. on the UTC+3 clock it uses elsewhere, which is 03:05 UTC and matches the trackers; its "10:05 p.m. ET" is one hour off.'
            claims: [fz1073-flight-times]

  - id: u-004
    at: "2026-10-02T21:00:00Z"
    title: "Saudi statement read at source; landing time and head count unsettled"
    headline:
      id: h-004
      text: "Flydubai FZ1073: Saudi ministry says co-pilot assaulted captain; motive, weapon, landing open"
      mode: attributes
      attributed_to: "Saudi ministry"
      claims: [fz1073-both-pilots-injured, {id: fz1073-motive-not-established, mode: open}, {id: fz1073-weapon-not-established, mode: open}, {id: fz1073-landing-time, mode: open}]
    claims_at_update:
      fz1073-both-pilots-injured: established/high
      fz1073-landing-time: contested/low
      fz1073-persons-on-board: contested/low
      fz1073-motive-not-established: searched_gap/low
      fz1073-weapon-not-established: searched_gap/low
      fz1073-uae-investigation: established/high
      fz1073-event-simulated: searched_gap/low
    paragraphs:
      - sentences:
          - id: s-013
            supersedes: s-003
            change: corrected
            why: "The earlier sentence quoted the Saudi statement as rendered by CNN and Al Jazeera ('revealed an assault ...'). The agency's own English, read on 2 October, says 'an altercation occurred in which the co-pilot assaulted the captain' (log L-26, item 2)."
            mode: attributes
            attributed_to: "The Saudi interior ministry"
            text: 'The Saudi interior ministry''s own English text says its preliminary investigations "revealed that an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals"; it does not say how, with what, or why.'
            claims: [fz1073-both-pilots-injured, {id: fz1073-weapon-not-established, mode: open}]
          - id: s-014
            supersedes: s-009
            change: corrected
            why: "The earlier sentence gave 06:45 UTC as the Saudi ministry's landing time. That is a rendering by Al Jazeera; the agency's text says '9:45 a.m.' with no time zone, so 06:45 UTC assumes Saudi time, UTC+3 (log L-26, item 3)."
            mode: open
            text: "The Saudi interior ministry's text says the aircraft landed at 9:45 a.m. and gives no time zone; AirNav Radar and Al Jazeera give about 06:58 UTC, and the landing time is not settled."
            claims: [fz1073-landing-time]
          - id: s-015
            mode: open
            text: "The number of people aboard is not settled: the Saudi interior ministry's text gives 174 passengers and an eight-member crew, and the airline's chief executive says 172 passengers and crew."
            claims: [fz1073-persons-on-board]
      - sentences:
          - id: s-016
            mode: attributes
            attributed_to: "The UAE Attorney-General"
            text: 'The UAE Attorney-General ordered an investigation on 1 October into the circumstances and causes, including "any possible connection to terrorist activity or intent, and whether it involved prior planning or direction".'
            claims: [fz1073-uae-investigation]
          - id: s-017
            mode: open
            text: "No evidence has been found that anyone simulated the event, but the records read are statements and reports, not raw tracker, recorder or medical data, so the question stays open."
            claims: [fz1073-event-simulated]
`````

## Appendix F: `build/subjects/flydubai-fz1073/media.yaml` (worked example, new, unreviewed)

`````yaml
# media.yaml: who reported what, when, and how it changed (format: build/SCHEMA.md, rules MR1 to MR7).
# WORKED EXAMPLE for flydubai-fz1073: a subset of the researcher's media timeline of 2026-10-02 (scratchpad fz1073/media-timeline.md), converted to UTC by the
# researcher. Not a reviewed record. Confers no weight on any claim: a report is not evidence of what it reports, and copies of one origin count once.
subject: flydubai-fz1073
confers_weight: false
observed: 2026-10-02

topics:
  - {id: t-event-kind, label: "What kind of event: hijacking, altercation, assault, attack", claims: [fz1073-diverted-tabuk, fz1073-both-pilots-injured], resolution: open}
  - {id: t-copilot-nationality, label: "The co-pilot's nationality", claims: [fz1073-israel-says-omani, fz1073-omani-nationality-unconfirmed], resolution: open}
  - {id: t-captain-nationality, label: "The captain's nationality", claims: [fz1073-captain-wounds], resolution: resolved, resolved_by: fz1073-captain-wounds}
  - {id: t-landing-time, label: "When the aircraft landed at Tabuk", claims: [fz1073-landing-time], resolution: open}
  - {id: t-takeoff-clock, label: "CNN's departure time and its time-zone labels", claims: [fz1073-flight-times], resolution: corrected}
  - {id: t-descent-size, label: "How far and how fast the aircraft descended", claims: [fz1073-descent-magnitude], resolution: open}
  - {id: t-weapon, label: "What weapon was used", claims: [fz1073-weapon-not-established], resolution: open}
  - {id: t-extra-pilots, label: "Who the additional pilots were and who took the controls", claims: [fz1073-crew-details], resolution: open}
  - {id: t-pilot-rule, label: "Whether a rule bars Omani pilots from the Israel route", claims: [fz1073-omani-barred-rule], resolution: open}
  - {id: t-motive, label: "Motive and accusations by officials", claims: [fz1073-motive-statements, fz1073-motive-not-established], resolution: open}
  - {id: t-staged-claim, label: "The claim that the event was staged", claims: [fz1073-event-simulated], resolution: open}
  - {id: t-headcount, label: "How many people were aboard", claims: [fz1073-persons-on-board], resolution: open}

reports:
  - {id: m-001, outlet: "Times of Israel (live entry)", url: "https://www.timesofisrael.com/liveblog_entry/hijacking-ruled-out-as-flydubai-flight-to-tel-aviv-lands-at-saudi-airport/", kind: live_entry, access: summary, published: "2026-09-30T06:57:00Z", basis: displayed, origin: toi-live-0930-hijack-ruled-out, said_by: "Israeli security sources (unnamed)", says: [{topic: t-event-kind, value: "hijacking ruled out; altercation between the pilots"}], note: "Displayed 9:57 am, no zone; 06:57 matches Khaleej Times 10:57 UAE. Read as a tool summary only; no correction note confirmed either way."}
  - {id: m-002, source: src-flydubai-updates, kind: statement, access: read, published: "2026-09-30T07:30:00Z", basis: relayed, origin: flydubai-statement-1, said_by: "flydubai", says: [{topic: t-event-kind, value: "an incident while en route; landed safely at Tabuk"}], note: "Time from Khaleej Times (11:30 UAE). The airline's page carries no timestamps."}
  - {id: m-003, source: src-cnn-live, kind: live_entry, access: read, published: "2026-09-30T07:54:35Z", basis: metadata, origin: cnn-live-0930-first-entry, said_by: "unnamed sources; flight tracking data reviewed by CNN", says: [{topic: t-event-kind, value: "violent incident between two pilots"}, {topic: t-descent-size, value: "17,400 ft in under two minutes"}], changed: [{observed: "2026-09-30T10:49:44Z", what: "entry edited; what changed is not visible", how_known: "per-entry dateModified in the page"}]}
  - {id: m-004, outlet: "Al Jazeera English", url: "https://www.aljazeera.com/news/2026/9/30/flydubai-flight-to-israel-diverted-to-saudi-arabia-after-emergency-alert", kind: original, access: read, published: "2026-09-30T08:00:10Z", basis: metadata, origin: aj-0930-staff-afp-reuters, said_by: "Al Jazeera Staff, AFP, Reuters; Flightradar24", says: [{topic: t-descent-size, value: "34,000 ft at 05:21 to under 17,000 ft at 05:22", version: unknown}, {topic: t-event-kind, value: "one pilot stabbed the other (Israel's Prime Minister)", version: unknown}], changed: [{observed: "2026-09-30T19:49:48Z", what: "page rewritten; the URL keeps the first headline ('diverted to Saudi Arabia after emergency alert'), the current headline is about a pilot stabbing", how_known: "URL slug against current headline; page dateModified"}]}
  - {id: m-005, outlet: "CBS News", url: "https://www.cbsnews.com/news/tel-aviv-israel-flydubai-flight-saudi-arabia-diverted-pilots/", kind: original, access: read, published: "2026-09-30T07:59:00Z", basis: metadata, origin: cbs-0930-first-story, said_by: "CBS reporting; Israeli officials; Israel's Prime Minister", says: [{topic: t-event-kind, value: "current headline: co-pilot stabbed captain, tried to crash (Netanyahu says)", version: rewritten}], changed: [{observed: "2026-10-01T15:38:00Z", what: "retitled; the current headline describes events of 1 October, so the 07:59 stamp belongs to the first version", how_known: "headline against datePublished and dateModified"}]}
  - {id: m-006, outlet: "Euronews", url: "https://www.euronews.com/2026/09/30/flydubai-plane-traveling-to-israel-diverted-to-saudi-arabia-after-alleged-dispute-between-", kind: original, access: read, published: "2026-09-30T08:16:18Z", basis: metadata, origin: euronews-0930, said_by: "Israel's Prime Minister (video); passengers", says: [{topic: t-event-kind, value: "alleged dispute between pilots", version: first}], changed: [{observed: "2026-10-01T07:34:44Z", what: "headline changed from an 'alleged dispute between pilots' to 'Israel says pilot tried to crash flydubai plane during cockpit fight'", how_known: "URL slug against current headline"}]}
  - {id: m-007, outlet: "MiGFlug", url: "https://migflug.com/afterburner/flydubai-fz1073-squawk-7500-hijack-alert-israeli-jets-tabuk-2026/", kind: original, access: read, published: "2026-09-30T08:18:13Z", basis: metadata, origin: migflug-0930-first-story, said_by: "Israeli media; CNN; Aviation Herald (not opened)", says: [{topic: t-event-kind, value: "squawk 7500; Israel feared a hijack", version: first}, {topic: t-captain-nationality, value: "a citizen of the United Arab Emirates (Israel's Air Defense Forces said)", version: unknown}, {topic: t-copilot-nationality, value: "an Omani citizen (Israel's Air Defense Forces said)", version: unknown}, {topic: t-weapon, value: "pocket knife", version: unknown}], changed: [{observed: "2026-10-02T20:22:07Z", what: "page carries 'Update, 30 September 2026, afternoon: The picture has changed sharply since this story was first published'; the nationality and weapon lines may belong to the update", how_known: "update banner and dateModified"}]}
  - {id: m-008, outlet: "NBC News", url: "https://www.nbcnews.com/world/middle-east/flight-dubai-tel-aviv-diverted-emergency-alert-rcna600628", kind: original, access: read, published: "2026-09-30T08:56:44Z", basis: metadata, origin: nbc-0930, said_by: "Israel's Prime Minister (CBS interview); Flightradar24", says: [{topic: t-descent-size, value: "14,125 ft in 29 seconds (Flightradar24)", version: first}, {topic: t-copilot-nationality, value: "an Omani citizen (Israel's Prime Minister)", version: rewritten}], changed: [{observed: "2026-10-01T01:42:00Z", what: "updated 9:42 PM EDT on 30 September", how_known: "visible update stamp"}]}
  - {id: m-009, outlet: "Greek City Times", url: "https://greekcitytimes.com/2026/09/30/israel-flydubai-fz1073-tabuk-terror-attempt/", kind: aggregator, access: read, published: "2026-09-30T09:14:07Z", basis: metadata, origin: greekcity-0930, said_by: "Israeli media (Channel 7, Channel 12); an Israeli official to Reuters", says: [{topic: t-captain-nationality, value: "a Russian captain and a Ukrainian first officer (Israeli media)"}, {topic: t-weapon, value: "pocketknife"}]}
  - {id: m-010, outlet: "Walla (via AeroTime live entry)", url: "https://www.aerotime.aero/articles/flydubai-fz1073-diverts-saudi-arabia-7500-code", kind: live_entry, access: relayed, published: "2026-09-30T09:45:00Z", basis: relayed, origin: walla-0930, said_by: "an Israeli security source (unnamed)", says: [{topic: t-copilot-nationality, value: "believed to be of Omani origin; nationality not conclusively established"}, {topic: t-extra-pilots, value: "relief pilots travelling as passengers took the controls"}], note: "AeroTime stamp 12:45 (UTC+3). AeroTime was read; Walla was not opened."}
  - {id: m-011, source: src-cnn-live, kind: live_entry, access: read, published: "2026-09-30T10:06:54Z", basis: metadata, origin: cnn-live-0930-terror-entry, said_by: "two Israeli officials and an Israeli source (unnamed)", says: [{topic: t-event-kind, value: "may have been an attempted terror attack; the co-pilot tried to stab the pilot"}]}
  - {id: m-012, source: src-cnn-live, kind: live_entry, access: read, published: "2026-09-30T11:24:56Z", basis: metadata, origin: cnn-live-0930-omani-entry, said_by: "two Israeli officials (unnamed)", says: [{topic: t-copilot-nationality, value: "Omani; the co-pilot, allegedly the attacker"}]}
  - {id: m-013, source: src-jpost-910192, kind: original, access: read, published: "2026-09-30T11:32:00Z", basis: zone_unverified, origin: jpost-910192, said_by: "an anonymous Transport Ministry source; Israeli sources", says: [{topic: t-copilot-nationality, value: "may have been of Omani origin (unverified reports), later corroborated by Israeli sources"}, {topic: t-pilot-rule, value: "flydubai's agreement 'explicitly states' pilots must come from normalising states (in the Post's own voice); 'a clear breach' (ministry source)"}], note: "Displayed 14:32; the metadata gives 14:32:00+00:00. If the page clock is Israel time (UTC+3) the time is 11:32 UTC; if it is UTC, 14:32. Not verified."}
  - {id: m-014, outlet: "Reuters (via AeroTime)", url: "https://www.aerotime.aero/articles/flydubai-fz1073-diverts-saudi-arabia-7500-code", kind: wire, access: relayed, published: "2026-09-30T13:19:00Z", basis: relayed, origin: reuters-0930-three-officials, said_by: "three Israeli officials (unnamed)", says: [{topic: t-event-kind, value: "co-pilot stabbed captain; possible attempted terror attack"}, {topic: t-copilot-nationality, value: "one official identified the suspected attacker as an Omani national"}, {topic: t-extra-pilots, value: "cabin crew entered the cockpit and took control"}], note: "Reuters original not found; AeroTime stamp 16:19 (UTC+3)."}
  - {id: m-015, source: src-flydubai-updates, kind: statement, access: read, published: "2026-09-30T13:30:00Z", basis: relayed, origin: flydubai-statement-2, said_by: "flydubai", says: [{topic: t-event-kind, value: "an altercation occurred in the flight deck; reasons and motives unknown"}, {topic: t-extra-pilots, value: "on-duty flydubai crew travelling on the flight"}], note: "Khaleej Times 5:30 pm UAE; CNN logs it at 13:40:15; AeroTime at 14:10. The airline's page carries no timestamps."}
  - {id: m-016, outlet: "Israel's Prime Minister, video statement (AP via PBS)", url: "https://www.pbs.org/newshour/world/netanyahu-says-a-pilot-on-a-flydubai-flight-stabbed-another-and-apparently-tried-to-crash-the-plane", kind: statement, access: read, published: "2026-09-30T13:41:00Z", basis: relayed, origin: pm-video-0930, said_by: "Israel's Prime Minister", says: [{topic: t-event-kind, value: "one pilot stabbed the other and apparently tried to crash the plane (does not say which pilot)"}, {topic: t-extra-pilots, value: "another flight crew member stabilised the plane"}]}
  - {id: m-017, outlet: "AP (via PBS)", url: "https://www.pbs.org/newshour/world/netanyahu-says-a-pilot-on-a-flydubai-flight-stabbed-another-and-apparently-tried-to-crash-the-plane", kind: wire, access: read, published: "2026-09-30T14:29:09Z", basis: metadata, origin: ap-0930-pbs, said_by: "AP; Tabuk airport; a regional official (unnamed)", says: [{topic: t-descent-size, value: "33,000 to 17,000 ft in about a minute (Flightradar24)"}]}
  - {id: m-018, source: src-cnn-live, kind: live_entry, access: read, published: "2026-09-30T18:53:05Z", basis: metadata, origin: cnn-live-0930-captain-entry, said_by: "Israel's Prime Minister; the Indian embassy in Riyadh", says: [{topic: t-captain-nationality, value: "Indian"}]}
  - {id: m-019, outlet: "ABC News (US)", url: "https://abcnews.com/International/flight-tel-aviv-diverted-saudi-arabia-after-incident/story?id=136880832", kind: original, access: read, published: "2026-09-30T19:56:00Z", basis: displayed, origin: abc-us-0930, said_by: "a passenger; Israeli officials; Flightradar24", says: [{topic: t-weapon, value: "a pocketknife (a passenger)"}, {topic: t-descent-size, value: "34,000 to 16,000 ft in three minutes"}], note: "Displayed 3:56 PM (US Eastern); the page was modified on 1 Oct 10:00 UTC."}
  - {id: m-020, outlet: "The Media Line (relaying Shafaq News)", url: "https://themedialine.org/top-stories/from-hijacking-alert-to-false-flag-claims-how-arab-and-iranian-outlets-framed-the-flydubai-incident/", kind: aggregator, access: read, published: "2026-09-30T18:27:08Z", basis: metadata, origin: fars-0930-via-shafaq, said_by: "Fars News Agency, citing 'Iranian security agencies'", says: [{topic: t-staged-claim, value: "an Iranian outlet says Israel was considering an aviation attack to blame Iran; Shafaq: 'Fars presented no evidence'"}], note: "Fars and Shafaq originals were not opened."}
  - {id: m-021, source: src-cnn-explainer, kind: original, access: read, published: "2026-10-01T01:51:23Z", basis: metadata, origin: cnn-explainer-1001, said_by: "Israel's Prime Minister, Israeli officials, the Saudi interior ministry, passengers", says: [{topic: t-takeoff-clock, value: "departed at 6:05 a.m. local time (10:05 p.m. ET)"}, {topic: t-landing-time, value: "touchdown at 9:54 a.m."}, {topic: t-descent-size, value: "17,400 ft in just under two minutes"}], changed: [{observed: "2026-10-02T20:43:01Z", what: "last edit; the 10:05 p.m. ET figure and the 9:54 a.m. touchdown were still on the page", how_known: "'Updated Oct 2, 2026, 4:43 PM ET' stamp"}]}
  - {id: m-022, source: src-abc-verify, kind: fact_check, access: read, published: "2026-10-01T02:22:56Z", basis: metadata, origin: abc-au-verify-1001, said_by: "ABC News Verify", says: [{topic: t-staged-claim, value: "a deepfake imitating a BBC report, 300,000+ views; a US account's 'false flag' post, 1.5 million views"}], changed: [{observed: "2026-10-01T21:54:39Z", what: "updated; the page title (og:title) now differs from the on-page headline", how_known: "page metadata"}]}
  - {id: m-023, outlet: "Arab News", url: "https://www.arabnews.com/middle-east/uae-launches-investigation-into-flydubai-flight-incident-3004025", kind: original, access: read, published: "2026-10-01T05:16:56Z", basis: metadata, origin: arabnews-1001, said_by: "the Israeli envoy to the UAE; Israel's Prime Minister", says: [{topic: t-copilot-nationality, value: "Omani, according to the Israeli envoy to the UAE"}], changed: [{observed: "2026-10-01T18:50:12Z", what: "modified", how_known: "page dateModified"}]}
  - {id: m-024, outlet: "UAE Attorney-General order (via Emirates 24|7)", url: "https://www.emirates247.com/uae/uae-attorney-general-orders-investigation-into-flydubai-flight-incident/6220", kind: statement, access: relayed, published: "2026-10-01T06:57:00Z", basis: relayed, origin: uae-ag-order-1001, said_by: "UAE Attorney-General", says: [{topic: t-motive, value: "to examine any terrorist activity or purpose, and any prior planning or direction"}], note: "Time from Khaleej Times (10:57 UAE). The WAM original was not reached."}
  - {id: m-025, outlet: "Gulf News", url: "https://gulfnews.com/business/aviation/flydubai-fz1073-what-happened-on-board-and-what-we-know-so-far-1.500694593", kind: original, access: read, published: "2026-10-01T08:14:00Z", basis: displayed, origin: gulfnews-1001, said_by: "the airline; the UAE civil aviation authority", says: [{topic: t-event-kind, value: "the airline confirmed an altercation but not the detailed accounts; Israel's Prime Minister's account 'has not been independently established by the UAE authorities'"}]}
  - {id: m-026, source: src-mofa-uae, kind: statement, access: read, published: "2026-10-01T09:33:00Z", basis: relayed, origin: uae-mofa-1001, said_by: "UAE Ministry of Foreign Affairs", says: [{topic: t-motive, value: "investigation covers motives, including any terrorist link and prior planning"}], note: "Time from Khaleej Times (1:33 pm UAE). The page carries no timestamp."}
  - {id: m-027, source: src-theprint, kind: aggregator, access: read, published: "2026-10-01T11:24:22Z", basis: metadata, origin: theprint-1001, said_by: "Jerusalem Post, Times of Israel, CNN; its own reading", derives_from: jpost-910192, says: [{topic: t-pilot-rule, value: "the 2020 bilateral agreement 'mentions nothing on pilot nationality'; reports differ on where a clause sits"}]}
  - {id: m-028, source: src-aljazeera-uae, kind: original, access: read, published: "2026-10-01T11:46:08Z", basis: metadata, origin: aj-1001-uae-investigates, said_by: "Israel's Prime Minister (Fox interview); WAM", says: [{topic: t-motive, value: "'underwent Islamist radical indoctrination' (Israel's Prime Minister, an accusation)"}]}
  - {id: m-029, source: src-cbs-copilot, kind: original, access: read, published: "2026-10-01T15:07:00Z", basis: displayed, origin: cbs-1001-copilot, said_by: "an unnamed Omani official; an Israeli official", says: [{topic: t-copilot-nationality, value: "an Omani official told CBS he was born in Oman and holds Omani citizenship; the Omani government has not confirmed"}, {topic: t-extra-pilots, value: "two off-duty pilots"}], changed: [{observed: "2026-10-02T13:23:20Z", what: "last edit", how_known: "page dateModified"}]}
  - {id: m-030, outlet: "Bloomberg (reprint, Spokesman-Review)", url: "https://www.spokesman.com/stories/2026/oct/01/flydubai-pilot-who-tried-to-crash-plane-identified/", kind: wire, access: read, published: "2026-10-01T15:39:00Z", basis: displayed, origin: bloomberg-1001, said_by: "Israel's Prime Minister (Fox News)", says: [{topic: t-copilot-nationality, value: "Omani; 'neither the airline nor the UAE government has announced the nationality'"}], note: "Bloomberg's own page was not reachable (HTTP 403)."}
  - {id: m-031, source: src-jpost-910349, kind: original, access: read, published: "2026-10-01T17:23:41Z", basis: zone_unverified, origin: cam-arc-study, said_by: "Combat Antisemitism Movement and Antisemitism Research Center (advocacy groups)", says: [{topic: t-staged-claim, value: "4,136 'false flag' posts in 12 hours, 2,963 hostile; the first post 67 minutes after the emergency signal"}], note: "Displayed 17:23 and metadata +00:00; zone unverified. The study and posts were not seen."}
  - {id: m-032, outlet: "Ynetnews", url: "https://www.ynetnews.com/jewish-world/article/r1zyjm2qfe", kind: original, access: read, published: "2026-10-01T18:03:53Z", basis: metadata, origin: cam-arc-study, said_by: "Combat Antisemitism Movement", says: [{topic: t-staged-claim, value: "the same counts, '67 minutes'"}], note: "Same underlying study as m-031: counts once."}
  - {id: m-033, source: src-saudi-moi-original, kind: statement, access: read, published: "2026-10-01T18:31:00Z", basis: displayed, origin: saudi-moi-spa-1001, said_by: "Saudi Ministry of Interior (via the Saudi Press Agency)", says: [{topic: t-event-kind, value: "an altercation occurred in which the co-pilot assaulted the captain, resulting in injuries to both individuals"}, {topic: t-headcount, value: "174 passengers and an eight-member flight crew"}, {topic: t-landing-time, value: "landed at 9:45 a.m. local"}], note: "SPA stamp '21:31 Local Time 18:31 GMT'. The research pass read the SPA original on 2 Oct; the repository manifest still lists this source as not read."}
  - {id: m-034, source: src-cnn-live, kind: live_entry, access: read, published: "2026-10-01T18:41:32Z", basis: metadata, origin: cnn-live-1001-saudi-rendering, derives_from: saudi-moi-spa-1001, said_by: "Saudi interior ministry (CNN's English rendering)", says: [{topic: t-event-kind, value: "an assault on the captain by the co-pilot, resulting in various injuries to both"}], note: "CNN's rendering omits 'altercation', which the SPA English text contains."}
  - {id: m-035, outlet: "Lead Stories", url: "https://leadstories.com/hoax-alert/2026/10/fact-check-video-does-not-show-passengers-flydubai-flight-fz1073-tel-aviv-celebrating-big-speaker-hijacking-attempt-2025.html", kind: fact_check, access: read, published: "2026-10-01T20:37:06Z", basis: displayed, origin: leadstories-basketball-video, said_by: "Lead Stories", says: [{topic: t-staged-claim, value: "the 'aftermath party' video is an Israeli basketball team in August 2025; rated false"}]}
  - {id: m-036, source: src-jpost-910405, kind: original, access: read, published: "2026-10-02T07:34:00Z", basis: zone_unverified, origin: jpost-910405, said_by: "anonymous sources", says: [{topic: t-copilot-nationality, value: "no other nationality"}, {topic: t-pilot-rule, value: "the bilateral agreement 'did not stipulate' crew nationality; does not address a separate operating arrangement"}], note: "Displayed 10:34 and metadata 10:34:36+00:00. If the page clock is Israel time the time is 07:34 UTC; if UTC, 10:34. Not verified. The repo timeline uses 07:34."}
  - {id: m-037, outlet: "IBTimes UK", url: "https://www.ibtimes.co.uk/flydubai-fz1073-false-flag-claim-debunked-1823302", kind: fact_check, access: read, published: "2026-10-02T08:46:14Z", basis: metadata, origin: leadstories-basketball-video, said_by: "Lead Stories", says: [{topic: t-staged-claim, value: "the 'aftermath party' video is from August 2025"}], note: "Relays m-035: counts once."}
  - {id: m-038, source: src-ibtimes-700mph, kind: aggregator, access: read, published: "2026-10-02T09:07:25Z", basis: metadata, origin: ibtimes-700mph, said_by: "CNN (Flightradar24); a Canadian pilot", says: [{topic: t-descent-size, value: "over 16,000 ft in 35 seconds; ground speed from about 460 to nearly 700 mph"}, {topic: t-staged-claim, value: "Facebook posts use a pilot's doubts about tracker figures; he did not say the flight was staged"}]}
  - {id: m-039, source: src-flydubai-updates, kind: statement, access: read, published: "2026-10-02T14:04:03Z", basis: metadata, origin: flydubai-statement-4, said_by: "flydubai CEO", says: [{topic: t-event-kind, value: "a safety incident in the flight deck"}, {topic: t-headcount, value: "all 172 passengers and crew on board are safe"}], note: "This is the page's modified_time. The CEO statement is the last numbered statement on the page."}
  - {id: m-040, source: src-reuters-kfgo, kind: wire, access: read, published: "2026-10-02T14:22:58Z", basis: metadata, origin: reuters-1002-kfgo, said_by: "a source briefed on the investigation; an Israeli official; Flightradar24", says: [{topic: t-descent-size, value: "16,625 ft in just over 30 seconds"}, {topic: t-extra-pilots, value: "a reserve flydubai pilot crew"}, {topic: t-copilot-nationality, value: "Omani authorities have not commented"}], note: "The same text appears in other outlets; counts once."}
  - {id: m-041, outlet: "Full Fact", url: "https://fullfact.org/world/flydubai-flight-bbc-presenter-deepfake/", kind: fact_check, access: read, published: "2026-10-02T15:50:53Z", basis: metadata, origin: fullfact-bbc-deepfake, said_by: "Full Fact; a BBC statement to Full Fact", says: [{topic: t-staged-claim, value: "the BBC-style video is fake; BBC confirmed"}]}
  - {id: m-042, source: src-gcaa-emirates247, kind: statement, access: read, published: "2026-10-02T17:15:00Z", basis: displayed, origin: gcaa-statement-1002, said_by: "UAE General Civil Aviation Authority (via WAM)", says: [{topic: t-motive, value: "will not comment on any details or claims in circulation"}], note: "Emirates 24|7 stamp 21:15 (+04)."}
`````

## Appendix G: `story.yaml` worked example for `gulf-of-tonkin` (neutrality run; scratch only)

`````yaml
# story.yaml worked example for gulf-of-tonkin (a historical dig that points the opposite way from FZ1073: its headline claim is refuted, and some of its claims are the project's own judgments).
# Written only to show that the same format and rules treat a settled, politically charged dig and a live technical-news one alike. Not published text.
subject: gulf-of-tonkin
names:
  people: []
  places: [Gulf, Tonkin, Vietnamese, Maddox, North]
  organisations: [USS]
  demonyms: [Vietnamese]
  other: [August, Signals]   # Signals: a sentence-opening word the name check does not know
updates:
  - id: u-001
    at: "2026-10-02T12:00:00Z"
    title: "What the record shows"
    headline:
      id: h-001
      text: "Gulf of Tonkin: the second attack reported on 4 August 1964 did not happen, the record shows"
      mode: states
      denies_target: true
      claims: [tonkin-aug4-attack-occurred]
    claims_at_update:
      tonkin-aug2-maddox-engaged: established/high
      tonkin-aug4-attack-occurred: refuted/high
      tonkin-sigint-selectively-presented: established/moderate
      tonkin-bait-order: searched_gap/low
      tonkin-original-text-missing: searched_gap/moderate
    paragraphs:
      - sentences:
          - id: s-001
            mode: states
            text: "North Vietnamese torpedo boats attacked USS Maddox on 2 August 1964; the destroyer and supporting aircraft returned fire."
            claims: [tonkin-aug2-maddox-engaged]
          - id: s-002
            mode: states
            denies_target: true
            text: "The second attack reported on 4 August 1964 did not take place."
            claims: [tonkin-aug4-attack-occurred]
          - id: s-003
            mode: states
            text: "Signals intelligence about 4 August was presented to senior decision-makers in a way that left out almost all the material showing no attack."
            claims: [tonkin-sigint-selectively-presented]
      - sentences:
          - id: s-004
            mode: open
            text: "No document read so far shows an order to provoke the 2 August clash by sending the Maddox in as bait."
            claims: [tonkin-bait-order]
          - id: s-005
            mode: open
            text: "The original decrypted Vietnamese text of the key intercept cited for 4 August cannot be located."
            claims: [tonkin-original-text-missing]
`````

## Appendix H: `story.yaml` worked example for `incandescent-lamp` (neutrality run; scratch only)

`````yaml
# story.yaml worked example for incandescent-lamp (a technical, historical dig). Written only to show that the same format and rules treat it like any other. Not published text.
# People are historical figures named in the sources; the people register still demands an authority that names them and two more sources (SR9).
subject: incandescent-lamp
names:
  people:
    - {name: "Thomas Edison", role: "inventor and patentee", named_by: src-us223898, also_named_by: [src-47f454, src-52f300]}
    - {name: "Joseph Swan", role: "inventor", named_by: src-chemnews-1879, also_named_by: [src-chemnews-1880, src-47f454]}
  places: []
  organisations: []
  demonyms: []
  other: [Edison, Swan, Lodygin]
updates:
  - id: u-001
    at: "2026-10-02T12:00:00Z"
    title: "What the record shows"
    headline:
      id: h-001
      text: "Edison did not invent the bulb alone: carbon lamps were patented by 1845; Edison v Swan is open"
      mode: states
      denies_target: true
      claims: [lamp-edison-sole-inventor, {id: lamp-swan-before-edison, mode: open}]
    claims_at_update:
      lamp-edison-sole-inventor: refuted/high
      lamp-lodygin-first-claim: refuted/high
      lamp-swan-before-edison: contested/moderate
      lamp-first-practical-priority: contested/low
    paragraphs:
      - sentences:
          - id: s-001
            mode: states
            denies_target: true
            text: "Edison was not the first or only inventor of the incandescent lamp."
            claims: [lamp-edison-sole-inventor]
          - id: s-002
            mode: states
            denies_target: true
            text: "Lodygin was not the first to patent an electric light in an enclosed globe."
            claims: [lamp-lodygin-first-claim]
          - id: s-003
            mode: open
            text: "Whether Swan, not Edison, should be credited with the incandescent lamp is not settled."
            claims: [lamp-swan-before-edison]
          - id: s-004
            mode: open
            text: "Who first made, and who first sold, a lamp practical for ordinary use is not settled by anything read so far."
            claims: [lamp-first-practical-priority]
`````

## Appendix I: `failure2.py` (the failure-case measurements of section 1.2)

Reads the built site (`siteB`) and the `051778c` files of FZ1073; changes nothing.

`````python
import re,html,glob,yaml
site='siteB'; sub='wtB/build/subjects/flydubai-fz1073/'
h=open(glob.glob(site+'/digs/flydubai*/index.html')[0]).read()
body=re.sub(r'<style>.*?</style>','',h,flags=re.S)
txt=html.unescape(re.sub(r'<[^>]+>',' ',body))
seg=h[h.find('<h2>Sources</h2>'):h.find('<h2>The data</h2>')]
man=yaml.safe_load(open(sub+'sources/MANIFEST.yaml'))['sources']
log=yaml.safe_load(open(sub+'log.yaml'))['log']
print("1. Fields the manifest holds per source vs what the page's Sources list prints")
print("   sources in manifest:",len(man)," listed on page:",len(re.findall(r'<li[^>]*>',seg)))
for k in ['read','retrieved','stored_as','sha256','origin','provenance','tests','gaps','next_step']:
    inm=sum(1 for s in man if k in s or k in (s.get('authenticity') or {}))
    small=' '.join(re.findall(r'<span class="small">(.*?)</span>',seg))
    print(f"   {k:11s} in manifest for {inm:2d} source(s); printed in the source line: {'yes' if re.search(k.replace('_',' '),small) else 'no'}")
ids=sorted(set(re.findall(r'\bL-\d+\b',txt)))
shown=[]
print("   what each source line prints, in full: title, link, and '· authenticity: <status>'; example:", re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>','',re.findall(r'<li[^>]*>(.*?)</li>',seg,re.S)[3])))[:140])
print("2. Log")
print("   log entries:",len(log)," entry ids the dig page mentions:",len(ids),ids)
print("   log entries printed on any published page: 0 (log.yaml is not copied to the site and no template renders it)")
print("   (L-24 says 'the log is published on the dig page'; the build does not do this.)")
print("3. Corrections page: how the build cuts each FZ1073 correction")
n=0
for e in log:
    t=" ".join(str(e['entry']).split())
    m=re.search(r"CORRECTION[^.]*\.(?:[^.]*\.){0,2}",t)
    if m:
        n+=1; print(f"   {e['id']}: entry {len(t):5d} chars, page shows {len(m.group(0)):4d}; ends: ...{m.group(0)[-60:]!r}")
miss=[e['id'] for e in log if 'correction' in str(e['entry']).lower() and not re.search(r"CORRECTION[^.]*\.",' '.join(str(e['entry']).split()))]
print("   entries that state a correction but are not matched by the page's regex:",miss)
tl=open(glob.glob(site+'/digs/flydubai*/timeline/index.html')[0]).read()
print("4. Timeline page exists:", len(tl),"bytes; it plots event times and links each dot to a source; it shows no first-report time, no edit, no origin")
`````

## Appendix J: `bad_story_demo.py` (the validator on broken input, section 3.6)

`````python
"""Run the story rules on deliberately broken copies of the FZ1073 story. Prints each rule firing. Reads the scratch worktree only."""
import copy, sys, yaml
sys.path.insert(0, "wtT/build/tools")
import story_rules as R
sd = "wtT/build/subjects/flydubai-fz1073/"
claims = {c["id"]: c for c in yaml.safe_load(open(sd + "claims.yaml"))["claims"]}
man = {s["id"] for s in yaml.safe_load(open(sd + "sources/MANIFEST.yaml"))["sources"]}
good = yaml.safe_load(open(sd + "story.yaml"))
e, w = R.check_story(good, claims, man)
print("as written:", len(e), "errors,", len(w), "warnings")
def run(label, edit):
    st = copy.deepcopy(good); edit(st)
    e, _ = R.check_story(st, claims, man)
    print(f"\n[{label}]"); [print("  ", x[:230]) for x in e]
S = lambda st, i, j=0: st["updates"][-1]["paragraphs"][i]["sentences"][j]
run("1 stronger than its claim: our own voice on a reported claim", lambda st: S(st, 1, 0).update(mode="states", text="The UAE Attorney-General ordered an investigation on 1 October."))
run("2 cites a claim that does not exist, and a sentence with no claim", lambda st: (S(st, 0, 1).update(claims=["fz1073-made-up"]), S(st, 0, 2).update(claims=[])))
run("3 a gap spoken as fact, attributed", lambda st: S(st, 1, 1).update(mode="attributes", attributed_to="The UAE", text="The UAE says nobody simulated the event."))
run("4 hype, a percentage and a loaded word in our voice", lambda st: S(st, 0, 2).update(text="The shocking attack by a radical pilot is 90% certain to be terror and the airline is not sure."))
run("5 a person named who no authority named", lambda st: S(st, 0, 2).update(text="The co-pilot John Smith is not confirmed to be Omani and is not known to the airline.", mode="open", claims=["fz1073-omani-nationality-unconfirmed"]))
run("6 headline too short", lambda st: st["updates"][-1]["headline"].update(text="Pilots fought on a flight"))
run("7 accusation not attributed", lambda st: S(st, 1, 0).update(accusation=True, mode="open"))
old = copy.deepcopy(good); new = copy.deepcopy(good)
new["updates"][0]["paragraphs"][0]["sentences"][0]["text"] = "Flydubai says nothing happened."
print("\n[8 SR11: edit an earlier sentence in place, checked against the base copy]"); [print("  ", x) for x in R.check_story_history(old, new)]
`````

## Appendix K: `run_all.sh` (rebuilds every output in this proposal)

`````sh
#!/bin/sh
# Rebuild every prototype output from the scratch worktree wtT (051778c + the proposed files). Usage: sh run_all.sh
cd "$(dirname "$0")"
cp wtT/build/tools/dossier.py wtT/build/tools/story_rules.py wtT/build/tools/test_story_dossier.py lib/
rm -rf outF outF0 outN
S=wtT/build/subjects
python3 gen.py --repo wtT --subject flydubai-fz1073 --out outF --pdf
python3 gen.py --repo wtT --subject flydubai-fz1073 --out outF0 --bare
cp story-tonkin.yaml $S/gulf-of-tonkin/story.yaml
python3 gen.py --repo wtT --subject gulf-of-tonkin --out outN
rm $S/gulf-of-tonkin/story.yaml
cp story-lamp.yaml $S/incandescent-lamp/story.yaml
python3 gen.py --repo wtT --subject incandescent-lamp --out outN
rm $S/incandescent-lamp/story.yaml
`````

## Appendix L: fingerprints of the prototype files (first 16 hex digits of sha256)

`````text
516baac35d55e789  gen.py
d4d5b8bbc877738e  lib/dossier.py
fb937150a16ec74e  lib/story_rules.py
e135b0186faedc58  lib/test_story_dossier.py
e495cda6a873653b  story-tonkin.yaml
f6c5cdce5dbd31f2  story-lamp.yaml
ef91e5989d4ee565  wtT/build/subjects/flydubai-fz1073/story.yaml
87ee2eaaa473ce37  wtT/build/subjects/flydubai-fz1073/media.yaml
8f27dddbcb17027b  failure2.py
d4626018dfa649da  bad_story_demo.py
47c11760e85c79b5  run_all.sh
`````
