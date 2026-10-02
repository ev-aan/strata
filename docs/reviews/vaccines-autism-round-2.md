# Independent review, round 2: dig/vaccines-autism (head d43c49a)

Scratch worktree only; nothing pushed, no PR; /home/user/strata working tree untouched; worktree removed at end.
Newer rules copied from claude/jolly-hopper-ira8mk (conformance.py, SCHEMA.md, review_dig.py, taxonomy.yaml, PUBLISH_GATE.md, REVIEW.md, CLAUDE.md).
I also ran the schema/publication-status validator (PS1-PS4): no PS errors for this subject.

## Verdict: NEEDS REVISION

The three new commits are additive (+159 lines in claims.yaml, +36 in log.yaml, +7 in MANIFEST.yaml; 0 deletions). They fix none of B1-B4 and N1-N9. They add two blocking problems of their own, both on the first screen or in the legal block the owner asked to be clear. Format debt is unchanged.

## 1. Status of earlier requests

| id | changed by new commits? | status |
|---|---|---|
| B1 wakefield-paper-account-accurate bundles ethics/referral/onset (para 157) | No. Text identical; still weight 5 / primary; para 157 still only in the "Yes" position | OPEN, blocking |
| B2 retraction-reasons: 2010 notice unread, "earlier investigation = GMC hearing" gloss, "two steps" | No in claims. WORSE: the new MANIFEST `publication.reason` for src-wakefield-1998 repeats "contrary to an earlier investigation" with no gloss, so the page now carries the phrase in two places. Still missing the 2004 Lancet funding admission | OPEN, blocking |
| B3 geier-licence: "Lupron protocol", "misleading consent", "standard of care" not in the cited opinion | No (claims.yaml lines 1305-1320 unchanged) | OPEN, blocking |
| B4 IOM 2004 / WHO GACVS used as anchor evidence; overlapping Danish registers | No. And the new summary puts WHO GACVS 2025 in the first-screen answer as a "figure" (see new finding F1) | OPEN, blocking |
| N1 thimerosal "precautionary" quote / omitted mercury-guideline point | No | OPEN |
| N2 Simpsonwood read in full possible | No | OPEN |
| N3 Poling: Rule 4(c) wording unverified; "established" on secondary | No; now compounded (F2) | OPEN |
| N4 signs-in-window overstated | No | OPEN |
| N5 Sotomayor "Yes, the question stays open" label | No (still labelled so) | OPEN |
| N6 rise-mostly-reporting scope | No | OPEN |
| N7 measles-RNA "high" | No | OPEN |
| N8 aluminum autism figure only via press release | No (the manifest now notes the correction, good; still unread) | OPEN |
| N9 DeStefano/Thompson (age-cutoff result; Thompson URL) | No | OPEN |
| Format: 38 `ref:`, no assessment, no taxonomy, no statement_kind, henry-ford disputed_by, 3 dead manifest URLs | No. `ref:` count is now 39 anchors (new va-compensation-program adds one) | OPEN |

## 2. New material: what I verified

True and correct:
- Retracted: Wakefield 1998 (Lancet notice PMID 20137807, Lancet 2010;375:445, Europe PMC type Retraction Notice); Hooker 2014 (Transl Neurodegener 2014;3:22, published 3 Oct 2014, wording "undeclared competing interests ... compromised the peer review process ... concerns about the validity of the methods and statistical analysis" exact).
- Corrected: Verstraeten 2003 (erratum Pediatrics 2004 Jan;113(1):184), Jain 2015 (erratum JAMA 2016 Jan 12;315(2):204), Andersson 2025 (Ann Intern Med 2025;178(10):1527, PMID 40674587). All three confirmed in Europe PMC.
- Henry Ford draft is unpublished: consistent with earlier read; the 26 Sep 2025 shelving statement not re-tested.
- Mawson 2017 "published" with a pulled earlier version: not re-tested (secondary).
- Numbers: Taylor 2014 5 cohorts 1,256,407 + 5 case-control 9,920 (abstract); Cochrane 2021 "2 observational studies; 1,194,764 children", RR 0.93 (0.85-1.01); Madsen 537,303 + Hviid 657,461 = 1,194,764 (arithmetic checks; the dig infers these are Cochrane's two studies, the abstract does not name them); Hviid 2019 6,517 cases, 5,025,754 person-years, 129.7 per 100,000, HR 0.93 (0.85-1.02); 2% x 129.7 = 2.6 (labelled own arithmetic, fine); Rossignol 5.0% (3.2-6.9) vs about 0.01%; "4 of 12 regressed with fever after routine vaccination" (Rossignol text); Shoffner 17/28 and 12/17; Berger 1,228 (830-6,225), 2001-2010; Chess 7% (earlier round).
- Bruesewitz majority (Cornell LII ZO page) quotes: "establishes a no-fault compensation program 'designed to work faster and with greater ease than the civil tort system'"; "No showing of causation is necessary; the Secretary bears the burden of disproving causation"; "for those the claimant must prove causation"; claimants need not show defect; awards paid from "a fund created by an excise tax on each vaccine dose". All verbatim (the dig lower-cases "No"). Hannah Bruesewitz: DTP, seizures, "residual seizure disorder", "developmental delay"; no "autism" in majority/syllabus. Dissent n.25: "some 5,000 petitions", "uniformly rejected", "do not necessarily mean that no such causal link exists".
- Poling (CNN 6 Mar 2008): "concluded last November ... 'significantly aggravated'"; Gerberding "absolutely no statement indicating that vaccines are a cause of autism"; concession "last fall, shortly before a deadline for expert testimony" (lawyer's account); decision had been sealed.
- Source-notice texts are accurate (Wakefield 1998 retracted in Feb 2010; Hooker 2014 retracted Oct 2014; Henry Ford unpublished).

## 3. New findings

| id | severity | where | finding |
|---|---|---|---|
| F1 | BLOCKING | short_answer.summary and summary_figures ("31 studies and 5 meta-analyses ... no causal relationship") | The WHO page says only 20 of the 31 primary studies found no association; "the other eleven studies (with nine originating from one single research group in the United States) suggested a potential association", judged very low strength, high risk of bias. All five meta-analyses found none. The first-screen figure reads as 31 of 31 null and omits the strongest opposing count. It is also adoption (a committee statement) shown as a headline "figure" next to evidence, the same B4 problem, now above everything else. Fix: state 20 of 31, the 11 with their grade, or drop the item from the figures and keep WHO as adoption. The summary also reports the Taylor "1,266,327" which is Strata's sum of cohort children and case-control participants (not in the abstract) without labelling it as such, while the same block says counts are not summed; label it or give the two numbers. |
| F2 | BLOCKING (small fix) | va-poling-concession what_it_is: "Made under no-fault rules where causation can be presumed (va-compensation-program)" | No source read says the Poling concession rested on a presumption. CNN says the program "concluded ... significantly aggravated"; the dig itself says the decision was never read (log L-14). The line invites the reading that the concession was an artefact of the low bar, which is unsupported and tilts the item. Remove, or hedge as "the compensation rules allow a presumption for listed injuries; whether it applied here was not checked". Also, bullet 1 "decision not to contest" understates the sourced wording ("concluded", "conceded the link"); use the sourced words. |
| F3 | Moderate (fix before publish) | short_answer, mito scale: "published reports of regression after a post-vaccination fever amount to 4 children in one series of 28" | The same Rossignol review reports "another child" with regression after a post-vaccination fever (refs 25, 85, i.e. the Poling case report the dig itself cites). The count is at least 5 across two reports, and "amount to" implies a complete census. Say "at least 5 children in two reports, found in a review, not a systematic count". |
| F4 | Moderate | scale for Poling: "One known concession ... all six test cases ... rejected" | CNN says Poling's case was itself designated a potential test case in 2007 and then conceded; omitting it hides the strongest fact for the other side. Also "one known concession" is not established: other compensated cases with autism-spectrum features exist in public reporting (for example Banks v. HHS, 2007, MMR causing ADEM; I only saw search leads and did not open them). Check before the word "one"; at minimum say "the best-known". "More than 5,000" vs sources: CNN 2008 "nearly 5,000 pending", Bruesewitz dissent "some 5,000"; the OAP page (the source cited) was not reachable for me (404/blocked), so ">5,000" and "about 4,800 pending" are unchecked by me. |
| F5 | Moderate | va-vicp-table-no-autism what_it_is_not: "Not a scientific list ... a policy decision" | Overstated: the Table is amended by rulemaking that draws on Institute of Medicine causality reviews as well as policy. Say "a legal list informed by, but not the same as, scientific findings". |
| F6 | Low | va-bruesewitz what_it_is_not: failure-to-warn "not barred by this holding" | True of the holding, but the same opinion notes manufacturers are generally immune from failure-to-warn claims if they complied with regulatory requirements. Add the qualifier. |
| F7 | Low | Hooker-Miller | The sibling 2020 SAGE paper is under an expression of concern (18 May 2026, PMC13187378: "under investigation"). Verified. The claims cite the EoC but the anchor text never says so, and src-hooker-miller-2021 has no `publication` entry. State in the anchor which paper the EoC covers, and record the 2021 paper's status. |
| F8 | Low | Wakefield manifest `publication.reason` | Reason is paraphrased from BMJ c696 (not read by me or the dig). Quote the notice or mark "as quoted". Same fix as B2. |
| F9 | Low | Process | `source_notices`, `flagged_sources`, `publication` are defined only on the unmerged branch schema/publication-status, and `summary`, `summary_figures`, `scale`, `what_it_is`, `what_it_is_not` appear in no schema here (the repo's own rules). They are unvalidated extensions; escalate or hold until the schema lands. |
| F10 | Low | Fairness (positive) | Good: "not a finding that vaccines cause autism" is paired everywhere with "not a proof that none ever did"; the compensation frame is introduced correctly; no new living person is named beyond earlier items; adoption_weight kept separate. |

## 4. Fairness check
Opposing views present for the legal items. Weak spots: F1 (WHO 11 of 31), F4 (Poling as test case, other cases), F3 (undercount), F2 (framing). No claim in the new text goes the other way (no overclaim of harm). Adoption: still mixed into anchors (B4) and now into the summary (F1).

## 5. Remaining format debt (counts, unchanged unless noted)
- 39 anchors use `ref:` (was 38; new va-compensation-program adds one) -> `sources:`. Every manifest id cited resolves; 3 manifest URLs still do not resolve (src-thompson-2014, src-cdc-2004-study-statement, src-stat-geier-2025); src-poling-npr-2008 still "search result only" yet cited.
- 40 claims lack `statement_kind` (all; review_dig lists first five).
- No `assessment:` block; 0 key_points (need 3); `short_answer` retained.
- No taxonomy entry for vaccines-autism.
- va-henry-ford-why-unpublished: no `disputed_by`.
- 12 conformance warnings: established claims anchored `secondary` (mmr-no-detectable-increase, retraction-reasons, thimerosal-no-detectable-increase, aluminum-no-detectable-increase, antigen-count, destefano-race-subset, poling-concession, omnibus-test-cases, rise-mostly-reporting, rubella, cdc-page-2025) plus henry-ford disputant. Several can be re-anchored to primary from here (MMWR, Simpsonwood PDF, CDC page, WHO page, Europe PMC abstracts).
- review_dig: conformance FAIL, assessment FAIL, key_points FAIL, taxonomy FAIL, statement_kind FAIL; quote matcher 16 quotes unmatched only because no source text is stored.
- Log: append-only OK (L-12 to L-14 are new entries); needs entries for any correction.

## 6. Sources not reached
Lancet 2004/2010 notices and Lancet 1998; bmj.com (c696 etc.); uscfc.uscourts.gov OAP page (404/WAF) and the six decisions; Poling Rule 4(c) report and the sealed decision; supremecourt.gov PDF (not a PDF to me); acpjournals full text; GMC findings; NHS Digital; Henry Ford statement; Retraction Watch on Mawson. Reached: Europe PMC, PubMed efetch, Cornell LII (opinion and dissent), CNN, WHO page, PMC (Hooker retraction note, SAGE EoC, Rossignol full text).

## 7. Owner decisions
1. Whether the first-screen answer carries any institution-count (WHO, IOM) at all, or only studies (recommended: studies only; institutions in adoption).
2. Whether "Two Narrow Exceptions Explained" headline stays (round 1 owner decision 1 still open); the new scale lines help but do not remove the "exceptions" reading.
3. Whether "one known concession" is to be investigated (Banks and others) or softened.
4. Adopt or hold the publication-status schema (F9) before publishing.
5. Rule 9 for statistical evidence (round 1 item 2) still open.
Nothing written to review.yaml.
