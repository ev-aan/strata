# Proposal: a written test for suggested topics, and a public record of what happens to them

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`. Not in force. Needs an independent re-assessment, then the owner's decision.

Revised twice on 2026-10-02: first after the independent assessment in `docs/reviews/assessment-topic-proposal-pr4-pr6.md` (section 1), then after a second independent assessment of revision a4a176c. Section 11 maps every required change of both to where it is met. Section 10 lists the choices that are the owner's and are **not** decided here.

Rule ids: the test is **TQ1 to TQ8** (admission) and **TQ9 to TQ11** (records). Searched on 2026-10-02 in every file of `main` and of the branches `dig/vaccines-autism`, `process/review-gate` and `schema/publication-status` (`TQ[0-9]`): no hit. They also avoid the families in use (T, TH, PS, P, N, X, A, S, C, R, B, F, V). Record ids are `TL-001` and up (no hit); the example in Appendix B uses `TL-EXAMPLE`.

## 1. The failure case (and an honest statement that it is pre-emptive)

**No real failure exists in the repository.** I looked for one and did not find it:
- No file records a topic suggestion, a declined topic or a topic admitted and not opened. The second assessor confirmed the same from the issue list: one open issue (#5), unrelated, and no submitted topic.

So this proposal is **pre-emptive**. The owner is asked to accept it as such, with the gap it closes stated exactly.

The gap, checked in the files on 2026-10-02:
1. **There is no suggest-a-topic form.** `.github/ISSUE_TEMPLATE/` holds `challenge.yml`, `dig-step.yml`, `news-review.yml`, `open-question.md` and `config.yml` (blank issues disabled). The Ideas page ("Suggest an idea or a dig") and the Start a dig page ("open an issue") both link to `issues_url` (`build/site.yaml`: `.../issues/new/choose`, the generic template chooser; `build/tools/build_site.py`). The only template that fits a dig topic is `open-question.md`, free text: it asks for the question, the "oracle", whether sources are open, the popular or conspiracy claim it touches, and prior work. Nothing says which questions are not admitted, and nothing records the outcome.
2. **No written test applies to digs or ideas.** `docs/CHALLENGES.md` (S1 to S5) covers challenges. `docs/NEWS_REVIEW.md` covers News Review suggestions only (section 2).
3. **Nothing records what was declined, or admitted and not opened.** `docs/GOVERNANCE.md` says "Owner opens it". The logs of the existing digs show how topics were opened ("TOPIC OPENED by the owner" in `chemtrails` and `flood-myths-worldwide`, "TOPIC SELECTED" with reasons in `dyatlov-pass`, "Owner proposed ... Owner chose" in `congress-promise-vote`), but no file shows what was not opened or why.

**The harm it prevents.** The first public suggestion that is evaluative ("Is X an idiot?"), names a private person, presumes a conspiracy, or asks for a conclusion to be proven would be declined, or quietly not opened, with no stated reason. Whichever direction it points, that looks arbitrary, and the project's standing rests on weighing evidence and not preference. It is cheaper to write the test before the first case than after it, when it would look like a reaction to one submission.

## 2. Evidence: what the existing rules already do

Read on 2026-10-02:
- `docs/NEWS_REVIEW.md`, "What gets reviewed": the owner chooses what is opened; "nothing is opened because it is popular or because many people ask"; "A suggestion must name the specific claims to check and give at least one source. A request to 'prove it was staged' is not a claim." Guardrail 1: do not name "a suspect or a private individual who has not been named by authorities and by multiple independent outlets"; never speculate about religion, ethnicity or beliefs. Guardrail 3: "staged" or "manufactured" is a claim to test.
- `.github/ISSUE_TEMPLATE/news-review.yml`: three required fields (`story`, `claims`, `sources`) and the sentence "We do not name suspects or speculate about anyone's beliefs or background."
- `docs/GOVERNANCE.md`: the row "Suggest a topic, dig or News Review | Anyone (issue form) | Owner opens it"; "Counts, reactions, popularity and repetition carry no weight"; "Agents and automation never admit a challenge, publish, or change a rule; they prepare, check and report."
- `build/tools/triage_challenge.py`: checks completeness and flags duplicates, and "NEVER admits or declines".
- `docs/CHALLENGES.md`: C6 (declined challenges summarised "without the submitter's name"), C7 (a reviewer, never an automated step, decides; the owner has the final say), C9 (abuse: bad-faith, repeated or harassing submissions are closed).
- `build/SCHEMA.md` N26: the one exception to append-only is redaction of personal data, only with the owner's decision, by a new entry that names what was removed.

What this already catches, for the News Review channel: a request without named claims and a source; naming a suspect before authorities and several outlets have; speculation about religion, ethnicity or beliefs; popularity as a reason. It does not catch, in any channel: an evaluative question with a named claim and a source; a policy question; a question that takes a conspiracy as given; a private individual who is not a suspect. It says nothing about digs and ideas. No channel records outcomes, apart from challenges (C6).

What is **not** missing: popularity carries no weight, and the owner decides what is opened. This proposal does not re-decide either.

## 3. What this proposal does and does not change

Adds: `docs/TOPICS.md`, `.github/ISSUE_TEMPLATE/suggest-topic.yml`, `build/topic_log.yaml` (empty at creation), an optional `/topics/` page, a notice in `news-review.yml`, one changed row in `docs/GOVERNANCE.md`. Exact text is in section 4 and the appendices.

Does not change: claim states, evidence classes, `conformance.py`, the publish gate, S1 to S5, `docs/NEWS_REVIEW.md` (not one word), any existing dig, any finding, or who decides (the owner opens topics). **No validator check is added.** Enforcement is procedural, and a missing or wrong record is not caught by a machine (section 9). If a check is wanted later it follows the same proposal path.

## 4. The exact change

### 4.1 Files and locations
| Path | Change |
|---|---|
| `docs/TOPICS.md` (new) | The test TQ1 to TQ11, the process, the record format, the outcome vocabulary, and the worked example of Appendix B. Text below. It states as a dependency that TQ4(c) must change if `docs/NEWS_REVIEW.md` guardrail 1 changes. |
| `.github/ISSUE_TEMPLATE/suggest-topic.yml` (new) | The form. Full YAML in Appendix A. |
| `.github/ISSUE_TEMPLATE/open-question.md` | Open owner choice 1: retire in favour of the form, or keep with a link to `docs/TOPICS.md` and a line that results are public. |
| `.github/ISSUE_TEMPLATE/news-review.yml` | Add a notice (proposed text, Appendix C). Needed because the News Review channel is logged (section 4.4) and its submitters are otherwise not told. |
| `build/topic_log.yaml` (new) | The public record, created as `records: []`. Format in 4.4 and Appendix B. |
| `docs/GOVERNANCE.md` row 1 | **Proposed text only, not edited here.** Now: "Suggest a topic, dig or News Review / Anyone (issue form) / Owner opens it". Proposed: "Suggest a topic, dig or News Review / Anyone (issue form) / A human reviewer the owner designates (or the owner) applies the topic test (docs/TOPICS.md) and records the result; agents may prepare and draft but never decide; the owner is told of every decline and opens the topic". |
| `build/tools/build_site.py` | (a) The Ideas and Start a dig pages link to `.../issues/new?template=suggest-topic.yml` for digs; method ideas keep the chooser. (b) A `/topics/` page is generated from `build/topic_log.yaml`: one row per record showing `id`, `decided`, `result`, `status`, `area`, `original_question` (as recorded), `rewritten_question` and `not_covered`, the tests that were not a pass with their sentence, `reason`, and `not_opened_reason` and `reconsider_on`; plus counts **of decisions** by area and by result. It never shows counts of submissions. Until built, the YAML is the record. |
| Labels | The label `topic-suggestion` does not exist and must be created by the owner (as `news-review` was). Owner action. |

**Who must approve each path, exactly.** `CLAUDE.md` and `docs/REVIEW.md` ("What only the owner does") escalate to the owner, and never let an agent merge, changes to rules, `CONTRIBUTING.md`, `SCHEMA.md` and `conformance.py`. `docs/TOPICS.md` is new rules, so it is escalated on that ground. The form, `news-review.yml`, `build_site.py` and the GOVERNANCE row are under `CODEOWNERS` paths (`/docs/`, `/.github/`, `/build/tools/`); `CODEOWNERS` binds only if branch protection requires code-owner review, which is a repository setting the owner turns on (`docs/REVIEW.md`). `build/taxonomy.yaml` is not in `CODEOWNERS`, and TQ7 is tied to its areas (section 9).

`build/SCHEMA.md` is not changed. Its Files table is the per-subject file table, and the topic log is not a subject file; the format lives in `docs/TOPICS.md`, and the log is not read by `conformance.py`.

### 4.2 The test (text for `docs/TOPICS.md`)

A suggestion is admitted for consideration only if it passes TQ1 to TQ8. **The tests are applied to the whole submission**: the question, the claim behind it and the evidence field, because a premise can be placed in any of them. They are applied to the question **as it will be dug**: a reworded question is tested again (TQ9). A test marked `unclear` is **not a pass**: the case goes to the owner, who decides, or it is declined with the unclear clause stated (see 4.4 for the outcome names). Passing does not oblige the owner to open the topic (TQ11).

**Definitions used below.**
- *Identified person*: a living or deceased person who is named, or can be identified from the submission by name, role, place or date (for example "the nurse on duty at [named hospital] on [date]").
- *Private individual*: an identified person who is none of (a) a holder of, or candidate for, public office, **and only for acts in that public function** (being an employee, officer, clerk, teacher or official of a body does not by itself make a person public); (b) a person widely known through their own public activity (author, executive, performer, athlete, scholar and the like); (c) a person named in connection with the event by authorities and by at least two independent outlets. A person under (c) is treated as public only for what those records say about the event, never for beliefs, motives, health, family or background. A deceased private person is treated by the same tests.
- *Premise (conspiracy narrative or other presupposition)*: a question whose wording takes as given a fact it should be testing: that a hidden or coordinated act happened, that something was concealed, or that an actor acted with intent. This holds **whatever the sentence form** ("Why", "How", "Prove that", "Did"). A question is a *hypothesis under test* only when the claim is stated as one that may be false, the underlying fact is stated as its own question, it says who would have had to do what, and evidence can bear on it. Examples. Premise: "Why did NASA fake the Moon landings?" Hypothesis under test: "Were the Apollo landings staged on Earth?" (claim `apollo-staged-hoax`). Premise: "How did the government hide the chemtrail program?" **and** "Did the government cover up the chemtrail program?" (cover-up presupposes something to cover; **both fail as worded**). Hypothesis under test: "Does a secret, large-scale spraying program exist?" (`chemtrails`, log L-02, part C).
- *Legal terms*: "stolen", "fraud", "treason", "murder", "genocide", "terrorism", "war crime", "illegal" and the like. They are allowed when the question asks whether a **named court, tribunal, agency, body or instrument** found, charged, ruled or applied them, or when the term is quoted as the claim under test (TQ3). They are not allowed as the project's own conclusion ("Was it genocide?"); that is rewritten (TQ9) to the named-body question, or to the specific acts the term describes (who did what, when).
- *Named body*: a state, government, agency, company, party or other organisation. A question may ask what a named body did or found. The people of a nationality, religion or ethnicity, or who work for or vote for a body, are not thereby the body.

**TQ1. Evidence can bear on it.** The question asks about something evidence can bear on: what happened, when, who said, made or wrote it, whether a document or object is genuine, whether a figure is right, whether a causal claim is supported, where or when something began, or what a text says and how it has been read. It need not be settleable: a dig may end "unsettled" (`casket-letters`, `eikon-basilike`). Declined: questions on which no evidence of any kind could bear (taste, value, faith as such; see the worked example in section 6).

**TQ2. Factual, not evaluative.** No judgment of character, intelligence, morality or worth as a conclusion ("idiot", "evil", "corrupt", "genius"). Legal terms follow the definition above. A question about **intent or sincerity** ("Did X lie about Y?") is not asked; it is rewritten to "Was X's statement about Y accurate?" (`build/SCHEMA.md` P6 and P11: motive and sincerity are not assessed).

**TQ3. Neutral wording, no presupposition.** The question does not assume its answer, and does not presuppose a fact it should test (see "Premise"). A loaded word is allowed only when the claim field quotes it as the claim under test and the question asks whether the claim is supported ("Was the event manufactured?", with the dig stating who would have had to do what). "Why did X lie about Y?" and "Did X cover up Y?" fail as worded.

**TQ4. Public record, not private lives.** The question concerns public statements, records, events, documents or objects. It does not target a private individual (definition above), ask for personal information, or speculate about anyone's beliefs, religion, ethnicity, health, background or motives. Published official records (a medical summary a government released, a court finding) are public statements and can be checked as such; the question may ask what they say, never what is behind them. Religion and ethnicity are barred as subjects of speculation about *persons*; a question about a text, a tradition or an event is not barred by this clause.

**TQ5. A source, or the kind of evidence.** The suggestion names at least one source we can open, or says what kind of evidence can bear on the question and where it would be found. A reviewer may reclassify a submission as a live story whatever the `live` field says; the News Review rule of `docs/NEWS_REVIEW.md` (named claims and at least one source) then applies, and this clause's alternative does not.

**TQ6. Not a campaign.** It is not an advertisement, a request to prove a preferred conclusion, or a way to attach the project's name to a position.

**TQ7. Fits the taxonomy and asks what is known.** It belongs to an area of `build/taxonomy.yaml`, can be dug to the project's standards, and asks what is known, not what should be done. A policy question ("Should X be banned?") fails as worded. It may be offered a rewrite into an empirical question (TQ9) only if the rewrite can be answered by evidence without the answer being a policy conclusion.

**TQ8. Harm check.** (a) It does not presume the guilt of a group (by nationality, religion, ethnicity, profession or similar) or ask for proof of it. A question may ask whether a named person or named body did a specific act, or what a named body found. (b) It does not take a premise as given (definition above). A hypothesis under test is admissible, and the submission must say who would have had to do what (a required form field). (c) **Admissibility never depends on what is believed at the time.** The test looks at the structure of the submission (a stated claim, an actor and mechanism, evidence that can bear), not at whether the claim is popular, officially dismissed or dominant. A hypothesis with serious evidence on one side is admissible; admitting it is not endorsing it, because the dig's states and confidence follow the evidence. (d) A live event follows the guardrails of `docs/NEWS_REVIEW.md`.

**TQ9. Original, rewrite and the rewrite's own test.** The submitter's question and claim are kept as received (`original_question`, `claim`), except under the safeguards of 4.5. A rewrite is a new question recorded in `rewritten_question`, never over the original, and it is **tested itself** (`rewrite_tests`, TQ1 to TQ8). It carries `not_covered` (what in the original it does not ask) and `rewrite_basis` (which named bodies or records it rests on, and why those; where several bodies have ruled, all of them or the stated criterion). The rewrite is an offer: the submitter may accept or refuse it, and it **lapses after 14 days** without an answer (as incomplete challenges do, `docs/CHALLENGES.md`). The dig opens only on an accepted rewrite, or the original if it passed, with both shown. When a dig opens, its `log.yaml` L-01 quotes both questions and the record id, and `assessment.question` is the question as dug.

**TQ10. Declines are public.** Every decision on a real submission is recorded, with the tests that were not a pass, the reason, and the rewrite offered if any. Spam and abuse are not recorded (section 4.3, step 7).

**TQ11. Admitted-but-not-opened is public.** A topic that is admitted and not opened is recorded with a reason code, a sentence and a date to look at it again. Counts by area and by result are of decisions, not of submissions.

### 4.3 Process (text for `docs/TOPICS.md`)
1. Anyone files `suggest-topic.yml` (a GitHub account is needed, as for challenges).
2. **Who decides.** "A reviewer" is a human the owner designates, or the owner. An agent (a review agent or any other) may prepare: check the form is complete, flag duplicates and like earlier records, label, and draft a record for the reviewer. An agent never decides admission, declines, offers a rewrite or opens a topic (`docs/GOVERNANCE.md`: "they prepare, check and report"; `docs/CHALLENGES.md` C7). The reviewer is never the submitter.
3. The reviewer applies TQ1 to TQ8 to the whole submission, cites any earlier `TL-` record on a like question or clause so that like cases get like rewrites, and records the outcome (4.4). A pull request adds the record to `build/topic_log.yaml`, and the reviewer comments on the issue with the record id. The pull request is merged under `docs/REVIEW.md`; its merge decides nothing about the topic.
4. Outcome vocabulary, one set everywhere (section 6 tables, the record, the form comments): `admitted`; `rewrite_offered`; `declined`; `owner_to_decide`.
5. **How the owner learns of declines.** Each record's pull request asks for the owner's review as a notification. Under owner choice 2 (section 10) the owner either approves each decline (the log in `CODEOWNERS`) or is notified and may overrule within a stated time by a superseding record.
6. The owner opens an admitted topic, or records `not_opened` with a reason (TQ11). Whether the owner's own topics are logged is open (owner choice 4); the format allows `channel: owner`.
7. **Spam and abuse.** Repeats that add nothing are closed with a pointer to the existing record (as `docs/CHALLENGES.md` C3). Bad-faith, repeated or harassing submissions are closed under C9 and **get no record**. An automated step never closes or records one.
8. **A private person named in the issue.** The issue stays public on GitHub. When a submission names or identifies a private individual, the reviewer asks a maintainer to edit the issue body to remove the name, or to hide it, and comments with the outcome and the record id; the record carries only `[private individual]`.
9. A decision can be answered by a new suggestion that cites the clause and the record id and rewords. The challenge form is for findings, not for this; the owner can always overrule by a superseding record.

### 4.4 The public record
File: `build/topic_log.yaml` (rendered at `/topics/`), created as `records: []`. Append-only like the dig logs: a correction is a new entry with `supersedes: TL-nnn`.

Fields: `id`, `received`, `decided`, `channel` (`topic-form`, `news-review-form`, `owner`), `original_question`, `claim` (the form's claim field, as received), `redacted` and `paraphrased` (booleans, 4.5), `tests` (TQ1 to TQ8 as `pass`, `fail` or `unclear`, with one sentence for any that is not a plain pass), `result`, `reason`, `rewritten_question`, `rewrite_basis`, `not_covered`, `rewrite_tests`, `rewrite_offered_on`, `rewrite_answer` (`pending`, `accepted`, `refused`, `lapsed`), `lapse_on`, `area`, `question_type`, `decided_by` (`reviewer` or `owner`, not a name), `status`, `subject`, `not_opened_reason`, `not_opened_note`, `reconsider_on`, `supersedes`, `cites` (earlier records).

Outcomes and stages:
| `result` | Meaning | Allowed `status` |
|---|---|---|
| `admitted` | Passes TQ1 to TQ8 as worded. | `admitted`, `opened`, `not_opened` |
| `rewrite_offered` | Fails as worded; a rewrite that passes (`rewrite_tests`) is offered. | `waiting_for_submitter` until the answer or `lapse_on`; then `admitted` (accepted, a superseding record) or `closed` (refused or lapsed) |
| `declined` | Fails and no rewrite is offered. | `closed` |
| `owner_to_decide` | At least one test is `unclear`. | `waiting_for_owner`; then one of the above in a superseding record |

`not_opened_reason` is one of `capacity`, `sources_not_reachable`, `duplicate_of_existing_dig`, `waiting_on_events`, `outside_current_focus`, `no_evidence_offered`, `owner_choice`, plus a required sentence. `owner_choice` is allowed, and visible; `no_evidence_offered` exists so that a topic with nothing to dig is not recorded under a euphemism.

Left out on purpose: the submitter's name, handle and contact; any private individual's name, details or role identifiers (replaced by `[private individual]`); the reviewer's name; the submitter's evidence beyond the title of a source. **The issue number is left out or kept: open owner choice 3.**

### 4.5 Safeguards for the public record
- **Paraphrase or withhold.** For any named living person, including a public figure, the reviewer may paraphrase or withhold in `original_question` and `claim` an allegation of a crime, sexual conduct or ill health, and sets `paraphrased: true` with a note saying it was done and by whom (`reviewer` or `owner`). The tests are applied to the original as received; the record shows only that it was a TQ2 and TQ4 failure.
- **Legal takedown, an exception to append-only.** On a legal request, a record may be edited to remove the text, and only that, by a new entry that says what was removed, on what ground and who decided, in the manner of `build/SCHEMA.md` N26 (which covers dig logs and personal data). **This needs the owner's decision** (owner choice 5), and git history still holds the earlier text, which a takedown may also have to deal with.
- Spam, abuse and the issue itself: 4.3 steps 7 and 8.

## 5. Impact: all 15 subjects, tested

Baseline: `python3 build/conformance.py --base origin/main` on this branch: **15 subjects and 107 shared nodes checked: 0 errors, 93 warnings.** (The second assessor also built the new files in a scratch tree and got the same result.) Nothing in the proposal touches a file the validator reads; no dig needs migrating and no finding changes.

The test is applied to the question each subject asks, from `assessment.question` where there is one, otherwise from the title, headline claim or the question the dig's own log states (the column says which). `vaccines-autism` is on branch `dig/vaccines-autism` only and is not counted.

| Subject | Question tested (source) | Result | Note |
|---|---|---|---|
| gulf-of-tonkin | "Did a second attack on US destroyers happen in the Gulf of Tonkin on 4 August 1964?" (assessment) | Admitted | Public officials, public record. |
| mcafee-and-surfside | "Was the Surfside condominium collapse tied to John McAfee's death?" (assessment) | Admitted; **discretion** TQ8(b) | The bare question names neither actor nor mechanism, so it is neither plainly a premise nor a full hypothesis under test; it is admitted because the dig states the claim and its parts separately. The dig makes no claims on private individuals (victims, his family), consistent with TQ4. |
| eikon-basilike | "Who wrote the King's Book: Charles I or John Gauden?" (assessment) | Admitted, **only with TQ1 "bear on"** | `unsettled`. |
| casket-letters | "Did Mary Queen of Scots write the Casket Letters?" (assessment) | Admitted, **only with "bear on"** | `unsettled`. |
| flydubai-fz1073 | "Was the Flydubai FZ1073 cockpit attack of 30 September 2026 manufactured?" (assessment) | Admitted; **discretion** TQ3, TQ8 | "Manufactured" is allowed only because the claim field quotes it as the claim under test; the question as worded is not itself a quotation, and "who would have had to do what" is in the dig (`NEWS_REVIEW.md` guardrail 3), not in the question. The co-pilot is not named in the dig (TQ4(c), guardrail 1). Live event: News Review rules apply in addition. |
| apollo-landings | "The Apollo landings were staged on Earth and never took place." (headline claim `apollo-staged-hoax`; no `assessment.question`) | `rewrite_offered` form needed; **discretion** TQ3 | A statement, not a question; as worded it asserts its answer. It passes once worded "Were the Apollo landings staged on Earth?", the form used in 4.2. The first revision of this table gave a plain pass, which was too generous. |
| chemtrails | Five parts, (A) to (E), filed separately (`log.yaml` L-02) | Admitted; **discretion** TQ8(b) | Parts B and C are hypotheses under test; E (harm) depends on C and is admissible only as a conditional. The cover-up and "how do they hide it" forms fail. |
| dyatlov-pass | "What physical event drove them out of the tent, and does the evidence support or exclude each proposed cause?" (`log.yaml` L-01) | Admitted; **discretion** TQ3, TQ8(b) | "What physical event drove them out" presupposes that one did; a reviewer would offer "Did a physical event drive them from the tent, and which proposed cause does the evidence support or exclude?". The cause "weapons test or other state involvement" names an actor and mechanism, so it is a hypothesis under test, but that is the reviewer's call. |
| proto-indo-european | Homeland and descent claims, e.g. `pie-steppe-homeland` (claims; title "Proto-Indo-European: A Reconstructed Language") | Admitted, **only with "bear on"** | Origin question; no PIE text exists. |
| flood-myths-worldwide | "Is the likeness between flood stories greater than chance?" and "inheritance or independent origin?" (`log.yaml` L-03, Q1 and Q2) | Admitted, **only with "bear on"**; **discretion** TQ3, TQ6 on the original | The owner's first wording (L-01: variation in chapter order "is too easily used to dismiss the likeness") carries a stance. L-03 then splits it into four questions: a real TQ9 case, like `congress-promise-vote`. |
| teti-pyramid-texts | Corpus of 19 utterance files; what the texts say and how scholars read them (title, claims) | Admitted, **only with "bear on"** | `what_does_it_mean`. TQ5: sources are named (Sethe, Allen, Faulkner); the dig says none was read. |
| congress-promise-vote | "Promise to vote to outcome" (`log.yaml` L-01) | Admitted as the narrower question; **discretion** TQ2 | The owner's first wording in the same entry, "whether politicians are true to their constituents", is evaluative and would have been given a rewrite. |
| votes-2009-present | All recorded roll calls, 111th to 119th Congress (title, `log.yaml` L-01) | Admitted | A dataset with a fixed rule, not a question; the form cannot express it (section 9). |
| votes-johnson-tonkin | Votes tied to the Tonkin dig, 1963 to 1971 (title, `log.yaml` L-01) | Admitted | Same. |
| incandescent-lamp | "Who invented the light bulb?" (assessment) | Admitted | `partly`; historic public figures. |

Result: **15 of 15 can be admitted, one only after rewording (apollo-landings).** Seven rows rest on reviewer discretion (mcafee, flydubai, apollo, chemtrails, dyatlov, flood, congress) and five pass only because TQ1 says "bear on". The table cannot show fairness: every row was chosen by the owner without a test, and the author knew the answers. It shows that the test does not reject existing work, and where it would have needed a judgment.

## 6. Neutrality test

The first draft paired mirror images, which are symmetric by construction. These are not mirrors. "Direction" is how a case is commonly coded; that coding is my own judgment. Results use the one vocabulary of 4.3 step 4.

| # | Submission | Direction | Result | Clause and note |
|---|---|---|---|---|
| 1 | "Did the Biden administration pressure platforms to remove content?" | right | `admitted` | Public officials, public record. |
| 2 | "Did the 2016 Trump campaign coordinate with Russia?" | left | `admitted` | "Coordinate" is not loaded; the dig uses named findings and primary records. |
| 3 | "Did Dominion voting machines change vote totals in 2020?" | right | `admitted` as a hypothesis under test | The submission must give actor, mechanism and evidence (audits, court records). The same structure as 2. |
| 4 | "Prove the 2020 election was stolen" | right | `rewrite_offered` | TQ2 ("stolen" is a legal term), TQ3, TQ6. Rewrite: "What did courts decide on the merits, what on procedure, and what did audits and official reviews find, in the post-2020 election cases of [named states]?" `rewrite_basis`: courts, audits and reviews together, because courts alone may have decided on standing. `not_covered`: whether the election as a whole was "stolen". |
| 5 | "Prove Trump's 2016 win was illegitimate" | left | `rewrite_offered` | Same clauses. Rewrite: "What did courts, official reviews and named investigations find about interference and its effect on the result?" Same basis as 4 (every kind of named body that has ruled). |
| 6 | "Is Israel committing genocide in Gaza?" | left | `rewrite_offered` | TQ2: a bare legal conclusion. Rewrite: "What did the named tribunal order or find, and what do the cited records show on [specific alleged acts]?" A state is a named body (TQ8(a) definition), not a group by nationality. |
| 7 | "Did Hamas commit atrocities on 7 October 2023?" | right | `rewrite_offered` | TQ2: "atrocities" is a conclusion. Rewrite: "What do official and independent investigations document about killings and hostage-taking that day?" Same operation as 6 (the first revision labelled it "Admit with rewrite"; that was inconsistent). |
| 8 | "Was the COVID lab-leak hypothesis true?" (2020) | cross | `admitted` as a hypothesis under test | TQ8(c): admitted in 2020, when widely treated as a conspiracy narrative, because the submission names an actor (a laboratory incident), a mechanism and evidence (genomes, lab records, assessments). The same test admits "Did the virus come from an animal market?". "Why did China release the virus?" fails TQ8(b). |
| 9 | "Was the Butler rally shooter acting alone?" | none | `admitted`; guardrail 1 governs naming | See section 7. A question about the event and the acts, not his beliefs. |
| 10 | "Is Biden senile?" / "Is Trump suffering from dementia?" | left / right | `rewrite_offered` | TQ2, TQ4 (speculation about health). Rewrite: "What did the published official reports and medical summaries say about [person]'s memory or health, and does [named report] say what is claimed?" The original is recorded paraphrased (4.5). |
| 11 | "Should the US ban TikTok?" | none | `rewrite_offered` | TQ7. Rewrite: "Do the cited records show [named data flows]?" `not_covered`: whether to ban. |
| 12 | "Does a higher minimum wage raise unemployment?" | mixed | `admitted`; **discretion** | TQ7. Empirical, but a policy question can be rewritten into one. See the policy paragraph below. |
| 13 | "Do vaccines cause autism?" | popular claim | `admitted` as a hypothesis under test | A dig exists on branch `dig/vaccines-autism`. |
| 14 | "Did the 1619 Project's claim about the Revolution hold up?" | left | `admitted` | A named text and claim. |
| 15 | "Was America founded as a Christian nation?" | right | `admitted`; the dig must define "founded as" first; **discretion** | As `incandescent-lamp` had to define "invented". TQ4's religion clause applies to persons only. |
| 16 | "Why does the media hide that crime is rising?" | right | `rewrite_offered` | TQ3, TQ8(b): "hide" is a premise. Rewrite: "What did [named outlets] report on [named crime measures] in [years], and how do the measures themselves compare?" |
| 17 | "Why does the right ignore climate science?" | left | `rewrite_offered` | TQ3, TQ8(a). Rewrite: "What do named statements and votes of [named bodies] say on [named finding]?" Same structure as 16 (a named body's record against a stated measure); the earlier draft kept the actor in one and dropped it in the other. |
| 18 | "Did the contents of Hunter Biden's laptop get authenticated?" | right | `admitted`; **discretion** TQ4 | Qualifies under (c) (named by authorities in public filings and by several outlets) and the question concerns a device and its files, not his private life. A relative of an official is not public by that fact. |
| 19 | "Is [named neighbour] an illegal immigrant?" | none | `declined` | TQ4. |
| 20 | "Is the Shroud of Turin authentic?" | none | `admitted` | An object with tests. |
| 21 | "Does God exist?" | none | `declined` | TQ1: see the religion example below. |
| 22 | "Did the CDC cover up [named harm]?" | right | `rewrite_offered` | TQ3, TQ8(b): presupposes something to cover. Rewrite: state [named harm] as its own question ("What do the records show about [named harm]?") and, separately, who would have had to conceal what. The same form fails for any agency, party or company. |
| 23 | "Did Senator X lie about Y?" | any | `rewrite_offered` | TQ2: intent. Rewrite: "Was X's statement about Y accurate?" |
| 24 | "Is [named public figure] a paedophile?" | any | `declined` | TQ2, TQ4. The original is paraphrased in the record (4.5). |
| 25 | "Did the nurse on duty on [date] at [named hospital] falsify the chart?" | none | `declined` | TQ4: identified by role; (a) covers public office only. |
| 26 | "Is the [named agency] report at [URL] genuine?" with the claim field "it proves they hid the deaths" | right | `rewrite_offered` | The claim field fails TQ3 and TQ8(b); the tests apply to the whole submission. The question alone would have passed. |
| 27 | A rumour about an unfolding event, `live` = No | any | `owner_to_decide` or reclassified | TQ5: the reviewer may reclassify it as live; the News Review rule then applies. |
| 28 | "Do [ethnic group] members in [place] commit more crime, [years]?" | right-coded | Owner choice 6 | The TQ8(a) rewrite pattern would admit group-crime statistics ("what do [named data] show"). |
| 29 | "Did the DNC have [named person] killed?" | right-coded | Owner choice 6 | A named body, a specific act, actor and mechanism stated: the text admits it. A reviewer would otherwise have to decline it under `no_evidence_offered`, in public. |

**Reading the table.** 29 submissions. The same operations are applied whichever way a case points: bare legal or moral words are replaced by named bodies or specific acts (4 to 7, 10); a presupposition is replaced by the fact stated as its own question (3, 8, 16, 17, 22, 26); intent, health and private-life speculation are replaced by questions about the published record (10, 23, 24). Like cases cite earlier records (4.3 step 3). No rule names a party, country or topic.

**Religion, a worked ladder (TQ1, TQ4).** "Does God exist?": `declined`, no evidence of the kind the project weighs bears on it. "Did the Quran have a single author?" and "Was the Book of Mormon translated from golden plates?": `admitted`, questions about a text and an object, on which manuscripts, dates and linguistic evidence bear. "Did Jesus exist?": **arguable, reviewer discretion**; it is a historical question about a person in antiquity on which the sources bear, and it is admitted if framed as what the earliest sources say, when they were written and by whom, and the dig says what such sources can and cannot settle. "Did he rise from the dead?": `rewrite_offered` to "What do the earliest sources say about the burial and tomb accounts, and when were they written?"; the miracle itself is not a question about evidence of the kind the project weighs. A reviewer who places the line elsewhere must say where, and cite this ladder.

**Policy questions rephrased as empirical ones (row 12, and "Does open immigration cause crime in [country]?").** The risk is real: "Should X be banned?" becomes "Does X cause Y?", and the answer then serves as a policy argument. Safeguards: (1) the original and rewrite are both kept, and `not_covered` says what the dig will not answer; (2) the rewrite is itself tested (TQ9); (3) the reviewer may decline a rewrite whose only evident purpose is to carry a policy conclusion. **Not enforced after admission:** a dig that concludes "therefore X should be banned" fails TQ7, but no step in `docs/REVIEW.md` or `docs/PUBLISH_GATE.md` checks for that today, and this proposal adds none. Adding one would be a second proposal, escalated to the owner. Until then the safeguard is an intention, applied only at admission.

**Where reviewer discretion decides (honestly).** (i) Premise or hypothesis under test (TQ8(b)). (ii) Whether a rewrite keeps the question or changes it, and which named bodies it rests on (TQ9; rows 4, 5, 12, 16, 17). (iii) Whether a person is "widely known through their own public activity" (TQ4(b)). (iv) Whether an interpretive question is one evidence "can bear on" (TQ1), and where "faith as such" starts. (v) Whether a loaded word is a quote of the claim under test (TQ3). (vi) Rewrite design as a whole: nothing in the text stops a reviewer choosing the body whose findings favour one result; TQ9 asks for the basis, like cases citing earlier records, and public review, and does not remove the risk.

## 7. Conflict with News Review guardrail 1

TQ4 bars questions about a private individual. Guardrail 1 allows naming "a suspect or a private individual" who has been "named by authorities and by multiple independent outlets" (the Butler case, row 9). They do not conflict, because they govern different steps, and the stricter applies at each.

- **TQ4 governs admission of the question.** Definition (c) matches guardrail 1: a person named in connection with the event by authorities and at least two independent outlets is public only for what those records say about the event. Differences in wording ("authorities" against "an authority"; "multiple" against "at least two") are closed by this proposal using the guardrail's own wording, "authorities" and "multiple independent outlets"; if the wording of the guardrail changes, (c) changes with it, by the same path, as `docs/TOPICS.md` states.
- **Guardrail 1 governs naming inside a News Review entry.** It is a floor: it does not permit naming a person merely because TQ4 admitted the topic. Before its condition is met, the topic is admissible only as a question about the event with the person unnamed (as `flydubai-fz1073` does).
- **Digs have no naming guardrail**, so for a dig TQ4(a) to (c) is the only protection. That is why (a) is limited to public office and public-function acts, and why a person identified by role counts as identified.
- Even for a person under (c), no question may ask about beliefs, motives, health, family or background (TQ4; P6 and P11).

## 8. Alternatives considered

- **Do nothing.** Declines and non-openings stay unexplained. Costs nothing now; the cost comes with the first contested case. Rejected for the reasons in section 1, with the caveat that the case is pre-emptive.
- **Free-form moderation by the owner.** Fast; not auditable; exposes the owner to charges of bias. Rejected.
- **Voting on topics.** Counts carry no weight here (GOVERNANCE, CHALLENGES C1). Rejected.
- **Extend the existing News Review test and S1 to S5 to digs.** This deserves a real comparison, because it adds no new rule family.
  - *S1 to S5 do not fit a suggestion.* They test evidence offered against an existing claim: S1 needs "one claim and the statement disputed", S2 "a source the page does not already cite", S4 what the claim should say instead. A new topic has no claim page to quote or to be new against. Applying them would fail every origin and meaning question (`proto-indo-european`, `flood-myths-worldwide`, `teti-pyramid-texts`).
  - *The News Review test fits news but is narrower than needed.* It requires named claims and a source, which is right for a rumour about a live event and is kept for that channel (TQ5). It says nothing about evaluative questions, policy questions, premises, legal terms or private individuals other than suspects, and it records nothing.
  - *What the extension would give:* one existing vocabulary, no new ids, less to learn, no risk of two tests disagreeing.
  - *What it would cost:* either S1 to S5 are stretched until they no longer mean what `docs/CHALLENGES.md` says, or `NEWS_REVIEW.md` is generalised, which changes a rules file and the live News Review channel. Neither is a smaller change than adding one file.
  - *Decision:* do not extend; **reuse by reference**. TQ4(c) restates guardrail 1, TQ5 defers to the News Review requirement, TQ2 echoes S5, TQ9 and the process follow C6, C7, C9 and the 14-day lapse. The owner may later fold the topic test into one of those documents by the same path.
- **A machine check for the test.** Not proposed: the judgments in section 6 are not mechanical, and an automated step never admits or declines (C7). A completeness script like `triage_challenge.py` could be proposed later.

## 9. Limits

- Reviewer discretion remains in the six places listed in section 6.
- Selection among admitted topics is made visible, not removed. Each `not_opened` entry has a reason and a date; `owner_choice` is a permitted, visible reason. That shows a pattern if there is one; it does not stop one.
- Safeguard (2) of the policy paragraph is not enforced after admission (section 6).
- No validator check. An unrecorded or wrong record is caught, if at all, in the pull request review.
- A decline is made by a human reviewer, so the owner or designated reviewers are a bottleneck; the 14-day lapse bounds only the rewrite offer, not the decision. No deadline for a decision is promised.
- The GitHub issue of a declined submission remains public with its author's account name until a maintainer edits it. The record omits the name; the source does not.
- TQ7 is tied to the areas of `build/taxonomy.yaml`, which is not in `CODEOWNERS`; changing it changes what TQ7 admits.
- The form cannot express a dataset-type dig (`votes-2009-present`) or an idea about the method; those come from the owner or from the Ideas page link.
- The proposed form and the existing forms link to `github.com/ev-aan/stratah`, while this session's remote is `ev-aan/strata`; confirm the slug before relying on the link.
- Evidence for this proposal is a reading of the files, the 15 subjects and 29 cases above, which are my application of the text. The independent re-assessment should repeat them.

## 10. Owner choices (open; not decided here)

1. **Retire `open-question.md`?** Yes: one form, one test, one record; a second path invites the bypass of putting a premise in its "popular or conspiracy claim it touches" field. The second assessor recommends yes. No: it costs one more file to maintain and keeps the older path for method questions; if kept, it must link to `docs/TOPICS.md` and say results are public.
2. **Owner involvement in declines.** (a) Add `/build/topic_log.yaml` to `CODEOWNERS`: the owner approves each decline, which fits "the owner has the final say"; it makes the owner the approver of every record and the bottleneck. (b) Leave it out: reviewers record decisions by pull request, the owner is notified and may overrule by a superseding record within a stated time (say 7 days); faster, but a decline can be merged with no owner action. The first draft's reason for leaving it out conflated authorship with approval.
3. **Keep or drop the issue number in the record.** Drop: the record cannot be used to find the submitter. Keep: parity with `docs/CHALLENGES.md` C6 (the intake record cites the issue), anyone can audit that every decline is recorded, and the issue is public anyway, so omission does not make the submitter anonymous.
4. **Log owner-originated topics?** Yes (`channel: owner`): selection by the owner is visible and the same tests are seen to apply to the owner's own choices. No: the owner opens what is chosen without a public step; the visible record then covers public submissions only, and the unlogged step the assessors identified stays unlogged.
5. **Legal-takedown exception to append-only** for the topic log, extending the idea of `build/SCHEMA.md` N26. Yes: a record can be cleaned on a legal request, visibly. No: append-only is absolute and the project relies on 4.5 paraphrase and withholding, accepting that a legal request may force a change anyway.
6. **Whether group-crime statistics and murder-conspiracy hypotheses about named bodies are admitted** (rows 28 and 29). As drafted, the text admits both: they are neutral, state a named body or measure and a specific act, and TQ8(c) forbids looking at what is believed. Admitting them takes a public stand that anything with a stated actor and evidence is admissible. Declining them needs an added rule (for example a minimum of evidence offered), which is a judgment about merit that the test otherwise avoids.
7. **Owner actions that follow any decision:** create the label `topic-suggestion`; decide whether a record's pull request may be merged by a review agent (`docs/REVIEW.md`) when the decision it records was a human's.

## 11. Response to the two assessments

First assessment, ten required changes:
| # | Required change | Where |
|---|---|---|
| 1 | Cite a real failure or state it is pre-emptive | Section 1. |
| 2 | Correct section 2 | Section 2. |
| 3 | Exact change | Section 4, Appendices A to C; section 3 states no validator check. |
| 4 | Final rule prefix | `TQ1` to `TQ11`; search stated at the top. |
| 5 | Define private individual, conspiracy narrative, legal terms | Section 4.2, definitions; premise now covers presupposition. |
| 6 | "bear on" | TQ1, TQ5; section 5. |
| 7 | TQ4 against guardrail 1 | Section 7. |
| 8 | 15-subject table, non-mirror test, TA8, policy rephrasing | Sections 5 and 6, TQ8(c). |
| 9 | Admitted-but-not-opened public | TQ11, 4.4. |
| 10 | Original and rewrite separate | TQ9, 4.4. |
| + | Alternative: extend News Review and S1 to S5 | Section 8. |

Second assessment, required changes:
| # | Change | Where |
|---|---|---|
| 1 | Define `unclear` | 4.2 preamble; `owner_to_decide` in 4.4. |
| 2 | Test the rewrite; waiting status; lapse | TQ9; `rewrite_tests`, `waiting_for_submitter`, 14-day lapse; Appendix B consistent with TQ9. |
| 3 | Keep the example out of the real log | The file is created as `records: []`; the example is `TL-EXAMPLE` and lives in `docs/TOPICS.md` and Appendix B. |
| 4 | One outcome vocabulary | 4.3 step 4, 4.4, section 6 (rows 4 to 7 now identical). |
| 5 | Close the gaming vectors | Whole-submission rule, TQ4(a) narrowed, role counts as identified, TQ3 and TQ8(b) cover presupposition and "Did X cover up Y" and "Did X lie" (the failing example fails as worded); rows 22 to 26. |
| 6 | Public-record safeguards | 4.5, 4.3 steps 7 and 8, TQ11 (decision counts only). Takedown needs the owner's decision (choice 5). |
| 7 | Who a reviewer is; what an agent may do; GOVERNANCE wording; owner learns | 4.3 steps 2 and 5; proposed row text in 4.1. |
| 8 | Safeguard (2) | Section 6: not enforced, no step checks it today. |
| 9 | Notice for the News Review channel | `news-review.yml` row in 4.1; Appendix C. |
| 10 | Claim field; owner channel | `claim` in the record; `channel: owner`; logging owner topics is choice 4. |
| 11 | Editorial | Cross-references fixed; CLAUDE.md and escalation sentence made exact (4.1); SCHEMA.md row dropped; "or deceased" in the form; required actor field; religion ladder; like cases cite earlier records (4.3 step 3); label as owner action. The 15-subject table is re-run with apollo, dyatlov and flood flags. |

Independent re-assessment against the seven standards of `docs/SCHEMA_PROPOSALS.md`: pending.
Owner decision: pending.

---

## Appendix A. `.github/ISSUE_TEMPLATE/suggest-topic.yml` (proposed text; not created)

```yaml
name: Suggest a topic
description: Suggest a question for a dig. A human reviewer applies a written test and records the result publicly. The owner decides what is opened.
title: "Topic: "
labels: ["topic-suggestion"]
body:
  - type: markdown
    attributes:
      value: |
        A topic is a question that evidence can bear on: what happened, who wrote or made something, whether a document or object is genuine, whether a figure is right, what a text says. It is not a judgment of anyone's character, not a request to prove a conclusion, and not a question about what should be done.
        Popularity, repeats and reactions carry no weight, and nothing is opened because many people ask. The whole suggestion (question, claim and evidence) is tested against [docs/TOPICS.md](https://github.com/ev-aan/stratah/blob/main/docs/TOPICS.md). The result, including a decline and the reason, is published. Your name is not. Your question may be reworded; both versions are published.
        Do not give the name, role or details of a private individual. Spam and abuse are closed and not recorded.
  - type: textarea
    id: question
    attributes:
      label: The question
      description: One question. Ask what happened, who said or made something, whether something is genuine, or what the evidence shows. Do not ask why someone did something, or whether they covered something up or lied; say what you want checked.
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
    id: actor
    attributes:
      label: If the claim involves a hidden or coordinated act, who would have had to do what?
      description: Name the body or person, the act, and how it could have been done. If the claim does not involve a hidden or coordinated act, write "not applicable".
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
      label: Does the question point at a living or deceased person who is not a public figure, by name, role, place or date?
      description: Public means holding or seeking public office (and only for acts in that office), widely known through their own public activity, or named in connection with the event by authorities and by multiple independent outlets. Being an employee or official of a body does not make someone public.
      options:
        - "No"
        - "Yes (a reviewer will read it with care; do not name them here)"
    validations:
      required: true
  - type: dropdown
    id: live
    attributes:
      label: Is it about something still unfolding, in days or weeks?
      description: A reviewer may decide it is, whatever you answer here.
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
        - label: I understand the question may be reworded, that my original, my claim text and the rewording may be published without my name, and that I may refuse the rewording. An offer lapses after 14 days without an answer.
          required: true
        - label: I have not included the name, role or personal details of a private individual.
          required: true
```

The `area` and `qtype` options are copied from `build/taxonomy.yaml` (`areas` and `question_types`, 2026-10-02; the second assessor confirmed they match exactly) and are kept in step by hand; no check does this.

## Appendix B. `build/topic_log.yaml` (record format; the file is created as `records: []`)

The file itself starts as:

```yaml
# Public record of suggested topics (docs/TOPICS.md). Append-only: a correction is a new entry with `supersedes`.
# Omitted on purpose: submitter name, handle, contact, any private individual's name, details or role, reviewer name.
records: []
```

The worked example below belongs in `docs/TOPICS.md` and must **not** be copied into the log. Its id is `TL-EXAMPLE`, which cannot be mistaken for a record. It is an invented, uncontested case, not a real submission.

```yaml
  - id: TL-EXAMPLE
    received: 2026-11-03
    decided: 2026-11-05
    channel: topic-form              # topic-form | news-review-form | owner
    original_question: "Should the airline be banned?"
    claim: "none"
    redacted: false                  # true if a private individual's name, details or role were replaced by [private individual]
    paraphrased: false               # true if an allegation about a living person was paraphrased or withheld (4.5)
    tests:                           # TQ1..TQ8: pass | fail | unclear; a sentence for anything that is not a plain pass
      TQ7: {result: fail, note: "A policy question: asks what should be done."}
      TQ1: pass
      TQ2: pass
      TQ3: pass
      TQ4: pass
      TQ5: pass
      TQ6: pass
      TQ8: pass
    result: rewrite_offered          # admitted | rewrite_offered | declined | owner_to_decide
    reason: "Fails TQ7 as worded; the rewrite passes."
    rewritten_question: "How did the airline's published safety record in [years] compare with the sector's?"
    rewrite_basis: "The regulator's published occurrence data for all carriers in [years]; chosen because it is the only source covering every carrier on one definition."
    not_covered: "Whether the airline should be banned."
    rewrite_tests: {TQ1: pass, TQ2: pass, TQ3: pass, TQ4: pass, TQ5: pass, TQ6: pass, TQ7: pass, TQ8: pass}
    rewrite_offered_on: 2026-11-05
    rewrite_answer: pending          # pending | accepted | refused | lapsed
    lapse_on: 2026-11-19             # 14 days after the offer
    area: technology
    question_type: is_claim_true
    decided_by: reviewer             # reviewer | owner
    status: waiting_for_submitter    # waiting_for_submitter | waiting_for_owner | admitted | opened | not_opened | closed
    cites: []                        # earlier TL records on a like question or clause
    supersedes: null
    # If accepted: a new entry (supersedes TL-EXAMPLE) sets result: admitted, rewrite_answer: accepted, status: admitted.
    # If not answered by lapse_on: a new entry sets rewrite_answer: lapsed, status: closed.
    # When the owner decides not to open an admitted topic, a new entry sets:
    #   status: not_opened
    #   not_opened_reason: owner_choice   # capacity | sources_not_reachable | duplicate_of_existing_dig | waiting_on_events | outside_current_focus | no_evidence_offered | owner_choice
    #   not_opened_note: "one required sentence"
    #   reconsider_on: 2026-12-01
    # When it becomes a dig: status: opened, subject: <subject folder>; the dig's log.yaml L-01 quotes both questions and the id.
```

## Appendix C. Notice for `.github/ISSUE_TEMPLATE/news-review.yml` (proposed text; not edited)

Add one sentence to the first markdown block of the form:

"A suggestion is checked against the topic test in [docs/TOPICS.md](https://github.com/ev-aan/stratah/blob/main/docs/TOPICS.md), and the outcome, with the reason and any rewording, is published without your name."
