# Proposal: a written test for suggested topics, and a public record of what happens to them

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`. Not in force. Needs an independent re-assessment, then the owner's decision.

Revised 2026-10-02 after the independent assessment in `docs/reviews/assessment-topic-proposal-pr4-pr6.md` (section 1). Section 10 maps each of its ten required changes to where it is met.

Rule ids: the test is **TQ1 to TQ8** (admission) and **TQ9 to TQ11** (records). Searched on 2026-10-02 in every file of `main` and of the branches `dig/vaccines-autism`, `process/review-gate` and `schema/publication-status` (`TQ[0-9]`): no hit. It also avoids the families in use (T, TH, PS, P, N, X, A, S, C, R, B, F, V). Record ids are `TL-001` and up (also no hit).

## 1. The failure case (and an honest statement that it is pre-emptive)

**No real failure exists in the repository.** I looked for one and did not find it:
- No file records a topic suggestion, a declined topic or a topic that was admitted and not opened. `build/` holds no such file, and the only open-question and topic templates are in `.github/ISSUE_TEMPLATE/`.
- I could not read GitHub issues from this session (access to the repository's issue API is not enabled). The independent assessment, which could, found one open issue (#5, unrelated) and no submitted topic.

So this proposal is **pre-emptive**. The owner is asked to accept it as such, with the gap it closes stated exactly.

The gap, checked in the files on 2026-10-02:
1. **There is no suggest-a-topic form.** `.github/ISSUE_TEMPLATE/` holds `challenge.yml`, `dig-step.yml`, `news-review.yml`, `open-question.md` and `config.yml` (blank issues disabled). The Ideas page and the Start a dig page both link to `issues_url` (`build/site.yaml`: `.../issues/new/choose`, the generic template chooser; see `build/tools/build_site.py`, the "Suggest an idea or a dig" and "open an issue" links). The only template that fits a dig topic is `open-question.md`, a free-text template: it asks for the question, the "oracle" and whether sources are open, but nothing says which questions are not admitted, and nothing records the outcome.
2. **No written test applies to digs or ideas.** `docs/CHALLENGES.md` (S1 to S5) covers challenges. `docs/NEWS_REVIEW.md` covers News Review suggestions only (section 2).
3. **Nothing records what was declined, or what was admitted and not opened.** `docs/GOVERNANCE.md` says "Owner opens it". The logs of the existing digs show how topics were opened ("TOPIC OPENED by the owner" in `chemtrails` and `flood-myths-worldwide`, "TOPIC SELECTED" with reasons in `dyatlov-pass`, "Owner proposed ... Owner chose" in `congress-promise-vote`), but no file shows what was not opened or why.

**The harm it prevents.** The first public suggestion that is evaluative ("Is X an idiot?"), names a private person, presumes a conspiracy, or asks for a conclusion to be proven would be declined, or quietly not opened, with no stated reason. Whichever direction it points, that looks arbitrary, and the project's standing rests on weighing evidence and not preference. It is cheaper to write the test before the first case than after it, when the test would look like a reaction to a particular submission.

## 2. Evidence: what the existing rules already do

Read on 2026-10-02:
- `docs/NEWS_REVIEW.md`, "What gets reviewed": the owner chooses what is opened; "nothing is opened because it is popular or because many people ask"; "A suggestion must name the specific claims to check and give at least one source. A request to 'prove it was staged' is not a claim." Guardrail 1: do not name "a suspect or a private individual who has not been named by authorities and by multiple independent outlets"; never speculate about religion, ethnicity or beliefs. Guardrail 3: "staged" or "manufactured" is a claim to test.
- `.github/ISSUE_TEMPLATE/news-review.yml`: three required fields (`story`, `claims`, `sources`) and the sentence "We do not name suspects or speculate about anyone's beliefs or background."
- `docs/GOVERNANCE.md`: the table row "Suggest a topic, dig or News Review | Anyone (issue form) | Owner opens it"; the rule "Counts, reactions, popularity and repetition carry no weight".
- `build/tools/triage_challenge.py`: checks completeness and flags duplicates, and "NEVER admits or declines".
- `docs/CHALLENGES.md` C6: declined challenges "are summarised there too, with the criterion failed and without the submitter's name".

What this already catches, for the News Review channel: a request without named claims and a source; naming a suspect before authorities and several outlets have; speculation about religion, ethnicity or beliefs; popularity as a reason. It does not catch, in any channel: an evaluative question ("Is X an idiot?") phrased with a named claim and a source; a policy question; a question that takes a conspiracy as given; a private individual who is not a suspect; and it says nothing at all about digs and ideas. Nor does any channel record outcomes, apart from challenges (C6).

What is therefore **not** missing: popularity carries no weight (C1, GOVERNANCE, NEWS_REVIEW); the owner decides what is opened. This proposal does not re-decide either.

## 3. What this proposal does and does not change

Adds: a rules file `docs/TOPICS.md`, a form `.github/ISSUE_TEMPLATE/suggest-topic.yml`, a record file `build/topic_log.yaml`, an optional public page `/topics/`, one changed row in `docs/GOVERNANCE.md`, one added row in the `build/SCHEMA.md` Files table. Exact text is in section 4 and the appendices.

Does not change: claim states, evidence classes, `conformance.py`, the publish gate, S1 to S5, `docs/NEWS_REVIEW.md` (not one word), `news-review.yml`, any existing dig, any finding, or who decides (the owner opens topics). **No validator check is added.** Enforcement is procedural: the reviewer applies the test, and the log entry is itself reviewed in a pull request under `docs/REVIEW.md`. A missing or wrong record is therefore not caught by a machine; section 9 states this as a limit. If a check is wanted later, it follows the same proposal path.

## 4. The exact change

### 4.1 Files and locations
| Path | Change |
|---|---|
| `docs/TOPICS.md` (new) | The test TQ1 to TQ11, the process, the record format. Text below. |
| `.github/ISSUE_TEMPLATE/suggest-topic.yml` (new) | The form. Full YAML in Appendix A. |
| `.github/ISSUE_TEMPLATE/open-question.md` | Retired in favour of the form (owner's choice; if kept, it must link to `docs/TOPICS.md`). |
| `build/topic_log.yaml` (new) | The public record, append-only. Format in 4.4 and Appendix B. |
| `build/SCHEMA.md` Files table | One row: `build/topic_log.yaml` is described in `docs/TOPICS.md` and is not read by `conformance.py`. I put the rules in `docs/TOPICS.md` and not in `SCHEMA.md` on purpose: `SCHEMA.md` defines dig data that the validator checks, and this is a procedure. The owner may prefer otherwise. |
| `docs/GOVERNANCE.md` row 1 | Now: "Suggest a topic, dig or News Review / Anyone (issue form) / A reviewer applies the topic test (docs/TOPICS.md) and records the result; the owner opens it". |
| `build/tools/build_site.py` | The Ideas page and Start a dig page link to the new form for digs; a `/topics/` page is generated from `build/topic_log.yaml`. Until built, the YAML in the repository is the public record. |
| `.github/CODEOWNERS` | Unchanged. `docs/` and `.github/` are already the owner's; `build/topic_log.yaml` is deliberately **not** added, so a reviewer can record a decision by pull request without the owner being the only author of declines. |

All of `docs/`, `.github/` and `build/tools/` are owner-reviewed paths (`CODEOWNERS`) and are escalated, never merged by an agent (`CLAUDE.md`).

### 4.2 The test (text for `docs/TOPICS.md`)

A suggestion is admitted for consideration only if it passes TQ1 to TQ8. The test is applied to the question **as it will be dug**: if the question is reworded (TQ9), the reworded question is tested again. Passing does not oblige the owner to open the topic (TQ11).

**Definitions used below.**
- *Private individual*: a living person who is none of (a) a holder of, or candidate for, public office, or someone acting in an official or public capacity that the question is about; (b) a person widely known through their own public activity (author, executive, performer, athlete, scholar and the like); (c) a person who has been named in connection with the event by an authority (a court, an agency, an official report) **and** by at least two independent outlets. A person under (c) is treated as public only for what those records say about the event, and never for beliefs, motives, health, family or background. A deceased person is treated by the same tests; in every case the question concerns what the record shows.
- *Conspiracy narrative (as a premise)*: a question that takes as given that a hidden, coordinated act by a named or implied group happened, and asks only why, how, or for proof. A question about a conspiracy is a *hypothesis under test* when it states the claim as one that may be false, says who would have had to do what, and names evidence that could bear on it. Example. Premise: "Why did NASA fake the Moon landings?" Hypothesis under test: "Were the Apollo landings staged on Earth?" (the question the `apollo-landings` dig tests, claim `apollo-staged-hoax`). Premise: "How did the government hide the chemtrail program?" Hypothesis under test: "Does a secret, large-scale spraying program exist?" (`chemtrails`, log L-02, part C).
- *Legal terms*: "stolen", "fraud", "treason", "murder", "genocide", "terrorism", "war crime", "illegal" and the like. These are allowed when the question asks whether a **named court, tribunal, agency, body or instrument** found, charged, ruled or applied them, or when the term is quoted as the claim under test (TQ3). They are not allowed as the project's own conclusion ("Was it genocide?"), which is rewritten (TQ9) to the named-body question, or to the specific acts the term describes (who did what, when).

**TQ1. Evidence can bear on it.** The question asks about something that evidence can bear on: what happened, when, who said, made or wrote it, whether a document or object is genuine, whether a figure is right, whether a causal claim is supported, where or when something began, or what a text says and how it has been read. It need not be settleable: a dig may end "unsettled" (`casket-letters`, `eikon-basilike`). Declined: questions on which no evidence of any kind could bear (taste, value, faith as such).

**TQ2. Factual, not evaluative.** No judgment of character, intelligence, morality or worth as a conclusion ("idiot", "evil", "corrupt", "genius"). Legal terms follow the definition above.

**TQ3. Neutral wording.** The question does not assume its answer. A loaded word is allowed only when it is quoted as the claim under test and the question asks whether the claim is supported ("Was the event manufactured?", with the dig stating who would have had to do what). "Why did X lie about Y?" becomes "Was X's statement about Y accurate?".

**TQ4. Public record, not private lives.** The question concerns public statements, records, events, documents or objects. It does not target a private individual (definition above), ask for personal information, or speculate about anyone's beliefs, religion, ethnicity, health, background or motives. Published official records (a medical summary a government released, a court finding) are public statements and can be checked as such; the question may ask what they say, never what is behind them. Religion and ethnicity are barred as subjects of speculation about *persons*; a question about a text, a tradition or a historical event involving religion is not barred by this clause.

**TQ5. A source, or the kind of evidence.** The suggestion names at least one source we can open, or says what kind of evidence can bear on the question and where it would be found. For the News Review channel the stricter rule of `docs/NEWS_REVIEW.md` applies in addition (named claims and at least one source), and this clause's alternative does not.

**TQ6. Not a campaign.** It is not an advertisement, a request to prove a preferred conclusion, or a way to attach the project's name to a position.

**TQ7. Fits the taxonomy and asks what is known.** It belongs to an area of `build/taxonomy.yaml`, can be dug to the project's standards, and asks what is known, not what should be done. A policy question ("Should X be banned?") is declined as worded. It may be offered a rewrite into an empirical question (TQ9), but only if the rewritten question can be answered by evidence without the answer being a policy conclusion, and the record states what part of the original the dig does not cover (TQ9).

**TQ8. Harm check.** (a) It does not presume the guilt of a group (by nationality, religion, ethnicity, party, profession or similar) or ask for proof of it. A question may ask whether a named person or body did a specific act, or what a named body found. "Prove that [group] commits more crime" becomes "What do [named data] show about [measure] for [place, years]?". (b) It does not take a conspiracy narrative as a premise (definition above). A hypothesis under test is admissible. (c) **Admissibility never depends on what is believed at the time.** The test looks at the structure of the question (a stated claim, an actor and mechanism, evidence that can bear), not at whether the claim is popular, officially dismissed or dominant. A hypothesis with serious evidence on one side is admissible; admitting it is not endorsing it, because the dig's states and confidence follow the evidence. (d) A live event follows the guardrails of `docs/NEWS_REVIEW.md`.

**TQ9. Original and rewrite are kept apart.** The submitter's question is kept verbatim as `original_question` (with only a private individual's name or personal data replaced by "[private individual]", and `redacted: true`). A rewrite is recorded in `rewritten_question`, never over the original. A rewrite is an offer: the submitter may accept it or not, and the dig opens only on a question the submitter accepted or the owner confirms, with the original shown beside it. Each rewrite carries `not_covered`: what in the original the rewritten question does not ask. When a dig opens, its `log.yaml` L-01 quotes both questions and the record id, and `assessment.question` is the question as dug.

**TQ10. Declines are public.** Every decline is recorded, with the tests failed, the reason, and the rewrite offered if any.

**TQ11. Admitted-but-not-opened is public.** A topic that passes and is not opened is recorded with a reason code and a sentence, and a date on which it will be looked at again. Counts by area and by outcome are shown on the topics page.

### 4.3 Process (text for `docs/TOPICS.md`)
1. Anyone files `suggest-topic.yml`. A GitHub account is needed, as for challenges.
2. A reviewer applies TQ1 to TQ8. The reviewer is never the submitter and never an automated step (as in `docs/CHALLENGES.md` C7); the owner may decide any case, with the same record. No completeness script is proposed here.
3. The reviewer comments on the issue with the outcome and the record id (`TL-nnn`), and adds the entry to `build/topic_log.yaml` by pull request.
4. Outcome is one of `declined`, `admitted`, `admitted_with_rewrite` (waiting for the submitter's answer).
5. The owner opens an admitted topic or records `not_opened` with a reason (TQ11).
6. A declined submitter may submit a new suggestion that cites the clause and rewords. Repeats that add nothing are closed with a pointer to the record (as C3).
7. A decision can be challenged on the clause it rests on; the answer is a new record, never an edit of the old one.

### 4.4 The public record
Where: `build/topic_log.yaml` (rendered at `/topics/`). Append-only, like the dig logs: a correction is a new entry with `supersedes: TL-nnn`. Format and a worked example are in Appendix B.

Fields: `id`, `received`, `decided`, `channel` (`topic-form`, `news-review-form`, `idea`), `original_question`, `redacted`, `rewritten_question`, `rewrite_status` (`offered`, `accepted`, `declined`), `not_covered`, `tests` (each of TQ1 to TQ8 as `pass`, `fail` or `unclear`, with one sentence for any that is not a plain pass), `result`, `reason`, `area`, `question_type`, `decided_by` (`reviewer` or `owner`, not a name), `status` (`declined`, `admitted`, `opened` with `subject`, or `not_opened` with `not_opened_reason` and `reconsider_on`), `supersedes`.

Left out on purpose: the submitter's name, handle, contact, **and the issue number** (the issue stays on GitHub with its author's account name, so identity is not hidden at the source, but the record does not point to it; the issue comment points to the record, not the other way round); any private individual's name or personal data; the submitter's evidence beyond the title of a source; the reviewer's name. `not_opened_reason` is one of `capacity`, `sources_not_reachable`, `duplicate_of_existing_dig`, `waiting_on_events`, `outside_current_focus`, `owner_choice` plus a required sentence. `owner_choice` is allowed, and visible.

## 5. Impact: all 15 subjects, tested

Baseline: `python3 build/conformance.py --base origin/main` on this branch: **15 subjects and 107 shared nodes checked: 0 errors, 93 warnings.** Nothing in the proposal touches a file the validator reads, so the result after is the same; no dig needs migrating and no finding changes.

The test below is applied to the question each subject asks, taken from `assessment.question` where there is one and otherwise from the title, headline claim or the question the dig's own log states (the column says which). `build/subjects/` has 15 folders; `vaccines-autism` is on branch `dig/vaccines-autism` only and is not counted.

| Subject | Question tested (source) | Result | Note |
|---|---|---|---|
| gulf-of-tonkin | "Did a second attack on US destroyers happen in the Gulf of Tonkin on 4 August 1964?" (assessment) | Pass | Public officials, public record. |
| mcafee-and-surfside | "Was the Surfside condominium collapse tied to John McAfee's death?" (assessment) | Pass; **reviewer discretion** on TQ8 | The link is stated as a claim that may be false (hypothesis under test), not as a premise. A reader who took the "grew a claim" wording differently could call it a premise. The dig's own description makes no claims on private individuals (the Surfside victims, his family), consistent with TQ4. |
| eikon-basilike | "Who wrote the King's Book: Charles I or John Gauden?" (assessment) | Pass **only with TQ1 "bear on"** | The assessment is `unsettled`. The first draft's "could settle" would have excluded it. |
| casket-letters | "Did Mary Queen of Scots write the Casket Letters?" (assessment) | Pass **only with TQ1 "bear on"** | `unsettled`; the evidence that would decide it does not survive. |
| flydubai-fz1073 | "Was the Flydubai FZ1073 cockpit attack of 30 September 2026 manufactured?" (assessment) | Pass; **reviewer discretion** on TQ3 and TQ8 | "Manufactured" is a loaded word, allowed under the TQ3 quote rule because it is the claim under test, and the dig states who would have had to do what (`docs/NEWS_REVIEW.md` guardrail 3). The co-pilot is not named in the dig (no authority has named him), consistent with TQ4(c) and guardrail 1. Live event: News Review rules apply in addition. |
| apollo-landings | "The Apollo landings were staged on Earth and never took place." (headline claim `apollo-staged-hoax`; the title is "Apollo Crewed Lunar Landings (1969-1972)") | Pass | Hypothesis under test. The dig refutes it; admission did not depend on that. |
| chemtrails | Five parts, (A) to (E), filed separately (`log.yaml` L-02; no claims drafted) | Pass; **reviewer discretion** on TQ8 | Parts B and C are hypotheses under test ("is or contains something other than exhaust"; "a secret large-scale spraying program exists"); part E (harm) depends on C and is admissible only as a conditional. The popular "how do they hide it" form would fail TQ8(b). |
| dyatlov-pass | "What physical event drove them out of the tent, and does the evidence support or exclude each proposed cause?" (`log.yaml` L-01) | Pass | Deceased, named in the public record; the question concerns causes, not their beliefs. |
| proto-indo-european | Homeland and descent claims, e.g. `pie-steppe-homeland` (claims; title "Proto-Indo-European: A Reconstructed Language") | Pass **only with TQ1 "bear on"** | An origin question; no PIE text exists, so evidence bears indirectly. |
| flood-myths-worldwide | "Is the likeness between flood stories greater than chance?" and "inheritance or independent origin?" (`log.yaml` L-03, Q1 and Q2) | Pass **only with TQ1 "bear on"** | Origin question. Q4 (Genesis) is a text question, not barred by TQ4's religion clause. |
| teti-pyramid-texts | Corpus of 19 utterance files; what the texts say and how scholars read them (title, claims) | Pass **only with TQ1 "bear on"** | `what_does_it_mean`. TQ5: the sources are named (Sethe, Allen, Faulkner), and the dig says none was read. |
| congress-promise-vote | "Promise to vote to outcome" (`log.yaml` L-01) | Pass as the narrower question; **reviewer discretion** | The owner's first wording in the same entry, "whether politicians are true to their constituents", is evaluative (TQ2) and would have been given a rewrite. This is a real case of TQ9: original and rewrite both kept. |
| votes-2009-present | All recorded roll calls, 111th to 119th Congress (title, `log.yaml` L-01) | Pass | A dataset with a fixed rule, not a hypothesis. |
| votes-johnson-tonkin | Votes tied to the Tonkin dig, 1963 to 1971 (title, `log.yaml` L-01) | Pass | Same. |
| incandescent-lamp | "Who invented the light bulb?" (assessment) | Pass | `partly`; historic public figures. |

Result: **15 of 15 pass.** What this shows and does not show: the test does not reject existing work. It cannot show that the test is fair, because every one of these was chosen by the owner without a test; the author of this proposal also knew the results. Five rows pass only because TQ1 says "bear on", and four need a reviewer's reading (TQ3 and TQ8; TQ2 for congress-promise-vote).

## 6. Neutrality test

The first draft paired mirror-image submissions, which are symmetric by construction. These cases are not mirrors: they differ in structure, subject and how the claim is framed. The "direction" column is how each is commonly coded, and that coding is itself my judgment. Results are those of the text in 4.2.

| # | Submission | Direction | Result | Clause and note |
|---|---|---|---|---|
| 1 | "Did the Biden administration pressure platforms to remove content?" | right | Admit | Public officials, public record. TQ1, TQ5. |
| 2 | "Did the 2016 Trump campaign coordinate with Russia?" | left | Admit | "Coordinate" is not loaded; the dig uses named findings and primary records. Same treatment as 1 and 3. |
| 3 | "Did Dominion voting machines change vote totals in 2020?" | right | Admit as a hypothesis under test | Actor, mechanism and evidence (audits, court records) are named. TQ8(b) does not apply. Same structure as 2. |
| 4 | "Prove the 2020 election was stolen" | right | Decline as worded; rewrite offered | TQ3, TQ6, TQ2 ("stolen" is a legal term). Rewrites: "What did courts decide on the merits, and what on procedure, in the post-2020 election cases?" and "Did audits or recounts in named states change the totals?" `not_covered`: whether the election as a whole was "stolen". The assessor's point holds: "did a court find fraud" alone could be decided by standing dismissals, so the first rewrite keeps merits and procedure apart. |
| 5 | "Prove Trump's 2016 win was illegitimate" | left | Decline as worded; rewrite offered | Same clauses. Rewrite: "What did named investigations find about interference and its effect on the result?" Treated like 4. |
| 6 | "Is Israel committing genocide in Gaza?" | left-coded | Decline as worded; rewrite offered | TQ2: a bare legal conclusion. Rewrite: "What did the named tribunal order or find, and what do the cited records show on [specific alleged acts]?" |
| 7 | "Did Hamas commit atrocities on 7 October 2023?" | right-coded | Admit with rewrite | TQ2: "atrocities" is a conclusion. Rewrite: "What do official and independent investigations document about killings and hostage-taking that day?" Same operation as 6. |
| 8 | "Was the COVID lab-leak hypothesis true?" (asked in 2020) | cross-coded | Admit as a hypothesis under test | TQ8(c): admitted in 2020, when it was widely treated as a conspiracy narrative, because it names an actor (a laboratory incident), a mechanism and evidence (genomes, lab records, assessments). The same test admits "Did the virus come from an animal market?". The premise form "Why did China release the virus?" would be declined under TQ8(b). |
| 9 | "Was the Butler rally shooter acting alone?" | none | Admit; guardrail 1 governs naming | See 7 below on which rule governs. A question about the event and the acts, not his beliefs. |
| 10 | "Is Biden senile?" or "Is Trump suffering from dementia?" | left / right | Decline as worded; rewrite offered | TQ2, TQ4 (speculation about health). Rewrite: "What did the published official reports and medical summaries say about [person]'s memory or health, and does [named report] say what is claimed?" |
| 11 | "Should the US ban TikTok?" | none | Decline | TQ7. Rewrite: "Do the cited records show [named data flows]?" `not_covered`: whether to ban. |
| 12 | "Does a higher minimum wage raise unemployment?" | mixed | Admit; **reviewer discretion** | TQ7. Empirical, but a policy question can be rewritten into one to pass. See 8 below. |
| 13 | "Do vaccines cause autism?" | popular claim | Admit as a hypothesis under test | A dig on it exists on branch `dig/vaccines-autism`. |
| 14 | "Did the 1619 Project's claim about the Revolution hold up?" | left | Admit | A named text and claim. Religion clause not engaged. |
| 15 | "Was America founded as a Christian nation?" | right-coded | Admit with a definition required; **reviewer discretion** | The dig must define "founded as" first, as `incandescent-lamp` had to define "invented". TQ4's religion clause applies to persons, not to this. |
| 16 | "Why does the media hide that crime is rising?" | right | Decline as worded; rewrite offered | TQ3, TQ8(b): "hide" is a premise. Rewrite: "Is crime rising on [named measures], and how do they differ?" |
| 17 | "Why does the right ignore climate science?" | left | Decline as worded; rewrite offered | TQ3, TQ8(a). Rewrite: "What do named statements and votes of [named bodies] say on [named finding]?" |
| 18 | "Did the contents of Hunter Biden's laptop get authenticated?" | right-coded | Admit; **reviewer discretion** on TQ4 | A person who is a relative of an official is not automatically public. He qualifies under definition (c) (named by authorities in public filings and by several outlets) and the question concerns the authenticity of a device and its files, not his private life. |
| 19 | "Is [named neighbour] an illegal immigrant?" | none | Decline | TQ4. |
| 20 | "Is the Shroud of Turin authentic?" | none | Admit | An object with tests (TQ1, TQ5). |
| 21 | "Does God exist?" | none | Decline | TQ1: no evidence of the kind the project weighs bears on it. A question about what a text says, or the history of a belief, would pass. |

**Reading the table.** 21 submissions: 6 coded right (1, 3, 4, 7, 16, 18), 6 coded left (2, 5, 6, 10 in part, 14, 17), the rest mixed or neither. The same operations are applied whichever way a case points: bare legal or moral words are replaced by a named body or specific acts (4 to 7); hidden-actor premises are replaced by a stated hypothesis (3, 8, 16, 17); health and private-life speculation is replaced by a question about the published record (10, 18, 19). No rule in the text mentions a party, a country or a topic.

**Where reviewer discretion decides (honestly).** (i) Whether a question is a premise or a hypothesis under test (TQ8(b); rows 3, 8, mcafee, flydubai, chemtrails). (ii) Whether a rewrite keeps the question or changes it (TQ9; rows 4, 5, 12). (iii) Whether a person is "widely known through their own public activity" (TQ4(b); row 18). (iv) Whether an interpretive question is one evidence "can bear on" (TQ1). (v) Whether a loaded word is a quote of the claim under test (TQ3). The proposal narrows these with definitions and examples; it does not remove them. What it adds is that each decision is written down with the clause, is public, and can be challenged (4.3, step 7).

**Policy questions rephrased as empirical ones (row 12).** The risk is real: "Should X be banned?" becomes "Does X cause Y?", and the answer then serves as a policy argument. Three safeguards: (1) the original and the rewrite are both kept, and the `not_covered` field says what the dig will not answer; (2) the test is applied to the question as it will be dug, so a dig that concludes "therefore X should be banned" fails TQ7 at review; (3) the owner or reviewer may decline the rewrite if its only evident purpose is to carry a policy conclusion. This relies on judgment; it is not mechanical.

## 7. Conflict with News Review guardrail 1

The two seem to conflict: TQ4 bars questions about a private individual; guardrail 1 allows naming "a suspect or a private individual" who has been "named by authorities and by multiple independent outlets" (the Butler case, row 9).

**They do not conflict, because they govern different steps, and the stricter applies at each.**
- **TQ4 governs admission of the question.** Definition (c) of "private individual" is written to match guardrail 1: a person named by an authority and at least two independent outlets is treated as public for what those records say about the event. So a topic about an event with such a person is admissible, and a topic about someone who has not been so named is not.
- **Guardrail 1 governs naming inside a News Review entry.** It is a floor: it does not permit naming a person merely because TQ4 admitted the topic. Before the condition is met, the topic is admissible only as a question about the event, with the person unnamed (as `flydubai-fz1073` does: "the co-pilot is NOT named: no authority has named him").
- Where the two could differ in wording, whichever is stricter for the step at hand applies. If `NEWS_REVIEW.md` is later changed, TQ4(c) must be changed with it, by the same path. This proposal does not change `NEWS_REVIEW.md`.
- Even for a person named under (c), no question may ask about beliefs, motives, health, family or background (TQ4; also P6 and P11, "motive and sincerity are not assessed", `build/SCHEMA.md`).

## 8. Alternatives considered

- **Do nothing.** Declines and non-openings stay unexplained and arbitrary-looking. Costs nothing now; the cost comes with the first contested case. Rejected for the reasons in section 1, with the honest caveat that the case is pre-emptive.
- **Free-form moderation by the owner.** Fast; not auditable; exposes the owner to charges of bias. The test makes each decision a clause and a sentence in public. Rejected.
- **Voting on topics.** Counts carry no weight here (GOVERNANCE, CHALLENGES C1). Rejected.
- **Extend the existing News Review test and S1 to S5 to digs.** This deserves a real comparison, because it adds no new rule family.
  - *S1 to S5 do not fit a suggestion.* They test evidence offered against an existing claim. S1 needs "one claim and the statement disputed"; S2 needs "a source the page does not already cite"; S4 says what the claim should say instead. A new topic has no claim page to quote or to be new against. Applying them would fail every origin and meaning question (`proto-indo-european`, `flood-myths-worldwide`, `teti-pyramid-texts`) for lack of a quotable claim.
  - *The News Review test fits news but is narrower than needed.* It requires named claims and a source, which is right for a rumour about a live event and is kept as the stricter rule for that channel (TQ5). It says nothing about evaluative questions, policy questions, conspiracy premises, legal terms or private individuals other than suspects; and nothing about records.
  - *What the extension would give:* one existing vocabulary, no new ids, less to learn, and no risk of two tests disagreeing.
  - *What it would cost:* either S1 to S5 are stretched until they no longer mean what `docs/CHALLENGES.md` says, or `NEWS_REVIEW.md` is generalised, which changes a rules file and affects the live News Review channel and `news-review.yml`. Neither is a smaller change than adding one file.
  - *Decision:* do not extend; **reuse by reference**. TQ4(c) restates guardrail 1, TQ5 defers to the News Review requirement, TQ2 echoes S5 ("not opinion"), and the record follows C6. The owner may later fold the topic test into `NEWS_REVIEW.md` or `CHALLENGES.md` by the same proposal path if one document is preferred.
- **A machine check for the test.** Not proposed: the judgments in section 6 are not mechanical, and `docs/CHALLENGES.md` C7 says an automated step never admits or declines. A completeness script like `triage_challenge.py` could be proposed later.

## 9. Limits

- Reviewer discretion remains in the five places listed in section 6.
- Selection by the owner among admitted topics is not removed. It is made visible: each `not_opened` entry has a reason code and a date, and `owner_choice` is a permitted, visible reason. That shows a pattern if there is one; it does not stop one.
- No validator check. An unrecorded decline is not detected by a machine; it is caught, if at all, in the pull request review.
- The GitHub issue of a declined submission remains public with its author's account name. The record omits the name; the source does not.
- Evidence for this proposal is a reading of the files and the 15 plus 21 cases above, which are my application of the text. The independent re-assessment should repeat them.

## 10. Response to the independent assessment (ten required changes)

| # | Required change | Where |
|---|---|---|
| 1 | Cite a real failure case or state it is pre-emptive | Section 1: pre-emptive; the specific gap (no suggest-a-topic form, `open-question.md` is free text, Ideas page links to the chooser, no record anywhere). |
| 2 | Correct section 2 | Section 2: restated against `NEWS_REVIEW.md`, `news-review.yml` (required `story`, `claims`, `sources`), `GOVERNANCE.md`; what each already catches and what not. |
| 3 | Exact change | Section 4 and Appendices A and B: files, test text, form YAML, record format, what is omitted; section 3 states no validator check. |
| 4 | Final rule prefix | `TQ1` to `TQ11`; collision search stated at the top. |
| 5 | Define private individual, conspiracy narrative, legal terms | Section 4.2, definitions, with an example pair. |
| 6 | "bear on" in place of "could settle" | TQ1, TQ5; section 5 shows which digs depend on it. |
| 7 | TQ4 against guardrail 1 | Section 7. |
| 8 | 15-subject table, non-mirror neutrality test, discretion, TA8 and policy rephrasing | Sections 5 and 6; TQ8(c). |
| 9 | Admitted-but-not-opened public | TQ11, 4.4. |
| 10 | Original and rewrite separate | TQ9, 4.4, Appendix B. |
| + | Alternative: extend News Review test and S1 to S5 | Section 8. |

Independent re-assessment against the seven standards of `docs/SCHEMA_PROPOSALS.md`: pending.
Owner decision: pending.

---

## Appendix A. `.github/ISSUE_TEMPLATE/suggest-topic.yml` (proposed text; not created)

```yaml
name: Suggest a topic
description: Suggest a question for a dig. A reviewer applies a written test and records the result publicly. The owner decides what is opened.
title: "Topic: "
labels: ["topic-suggestion"]
body:
  - type: markdown
    attributes:
      value: |
        A topic is a question that evidence can bear on: what happened, who wrote or made something, whether a document or object is genuine, whether a figure is right, what a text says. It is not a judgment of anyone's character, not a request to prove a conclusion, and not a question about what should be done.
        Popularity, repeats and reactions carry no weight, and nothing is opened because many people ask. A suggestion is tested against [docs/TOPICS.md](https://github.com/ev-aan/stratah/blob/main/docs/TOPICS.md). The result, including a decline and the reason, is published without your name. For a current story use the News Review form instead.
        Do not give the name or details of a private individual.
  - type: textarea
    id: question
    attributes:
      label: The question
      description: One question. Ask what happened, who said or made something, whether something is genuine, or what the evidence shows. Say who would have had to do what if the question is about a hidden act.
    validations:
      required: true
  - type: textarea
    id: claim
    attributes:
      label: The claim behind it, if there is one
      description: If the question starts from something people say, quote it and say where it appears or who says it. Otherwise write "none".
    validations:
      required: true
  - type: textarea
    id: evidence
    attributes:
      label: What evidence can bear on it
      description: Name at least one source we can open (a document, record, dataset, report, object), or say what kind of evidence would bear on the question and where it would be found.
    validations:
      required: true
  - type: dropdown
    id: person
    attributes:
      label: Does the question point at a living person who is not a public figure?
      description: Public means holding or seeking public office, acting in an official capacity the question is about, widely known through their own public activity, or named in connection with the event by an authority and by at least two independent outlets.
      options:
        - "No"
        - "Yes (a reviewer will read it with care; do not name them here)"
    validations:
      required: true
  - type: dropdown
    id: live
    attributes:
      label: Is it about something still unfolding, in days or weeks?
      options:
        - "No"
        - "Yes (please use the Suggest a News Review form)"
    validations:
      required: true
  - type: dropdown
    id: area
    attributes:
      label: Area
      options:
        - History
        - Politics and Government
        - Current Events
        - Science and Nature
        - Medicine and Health
        - Technology and Engineering
        - Archaeology and Ancient Texts
        - Language and Linguistics
        - Religion and Mythology
        - Law and Justice
        - Media and Misinformation
        - Economics and Business
    validations:
      required: true
  - type: dropdown
    id: qtype
    attributes:
      label: Kind of question
      options:
        - Did it happen?
        - Who wrote or made it?
        - Is the document or object genuine?
        - What caused it?
        - What did people know, and when?
        - Is a widely shared claim true?
        - Where and when did it begin?
        - What does it say or mean?
    validations:
      required: true
  - type: checkboxes
    id: confirm
    attributes:
      label: Before you submit
      options:
        - label: I am asking what the evidence shows, not asking for a conclusion to be proven.
          required: true
        - label: I understand the question may be reworded, that my original and the rewording are both published without my name, and that I may decline the rewording.
          required: true
        - label: I have not included the name or personal details of a private individual.
          required: true
```

The `area` and `qtype` options are copied from `build/taxonomy.yaml` (`areas` and `question_types`, 2026-10-02) and must be kept in step with it by hand; no check does this.

## Appendix B. `build/topic_log.yaml` (record format, with one invented example)

```yaml
# Public record of suggested topics (docs/TOPICS.md). Append-only: a correction is a new entry with `supersedes`.
# Omitted on purpose: submitter name, handle, contact, issue number, any private individual's name or details, reviewer name.
records:
  - id: TL-001                       # EXAMPLE ONLY, not a real submission
    received: 2026-11-03
    decided: 2026-11-05
    channel: topic-form              # topic-form | news-review-form | idea
    original_question: "Prove the election was stolen"
    redacted: false                  # true if a private individual's name or details were replaced by [private individual]
    rewritten_question: "What did courts decide on the merits, and what on procedure, in the post-election cases of [named year and states]?"
    not_covered: "Whether the election as a whole was 'stolen'; the project asks only what named bodies found."
    rewrite_status: offered          # offered | accepted | declined
    tests:                           # TQ1..TQ8: pass | fail | unclear; a sentence for anything that is not a plain pass
      TQ1: pass
      TQ2: {result: fail, note: "'stolen' is a legal term used as a conclusion, not tied to a named body."}
      TQ3: {result: fail, note: "Assumes its answer."}
      TQ4: pass
      TQ5: unclear
      TQ6: {result: fail, note: "Asks for a preferred conclusion to be proven."}
      TQ7: pass
      TQ8: pass
    result: admitted_with_rewrite    # declined | admitted | admitted_with_rewrite
    reason: "Fails TQ2, TQ3, TQ6 as worded; the rewrite passes."
    area: politics
    question_type: did_it_happen
    decided_by: reviewer             # reviewer | owner
    status: admitted                 # declined | admitted | opened | not_opened
    # When the owner decides not to open an admitted topic, a new entry (supersedes this one) sets:
    #   status: not_opened
    #   not_opened_reason: owner_choice   # capacity | sources_not_reachable | duplicate_of_existing_dig | waiting_on_events | outside_current_focus | owner_choice
    #   not_opened_note: "one required sentence"
    #   reconsider_on: 2026-12-01
    supersedes: null
```

When a record becomes a dig, `status: opened` and `subject: <subject folder>` are added in a new entry that supersedes this one, and the dig's `log.yaml` L-01 quotes the original and the rewritten question and this id.
