# Proposal: an admission test for suggested topics (digs, News Reviews, ideas)

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`. Not in force. Needs an independent assessment, then the owner's decision.

## 1. The failure case
Challenges have an admission test (S1 to S5, `docs/CHALLENGES.md`). Suggestions for a topic, dig, News Review or idea do not. The Ideas page and the News Review form accept any text. Nothing stops a submission like "Is the president an idiot?", "Prove the election was stolen", or a question that names a private person. Such a submission cannot be settled by evidence, would be a vehicle for opinion or harassment, and does not fit the project's purpose ("what do we actually know"). With no written test, each decline is an unexplained judgment call and looks arbitrary or partisan.

## 2. Evidence
Checked in the repository on 2026-10-02: `.github/ISSUE_TEMPLATE/news-review.yml` and the Ideas page link ask for a story and claims but apply no test; `docs/CHALLENGES.md` covers challenges only; `docs/NEWS_REVIEW.md` sets guardrails for how a review is done, not for what may be suggested.

## 3. Proposed rule: the topic test (T-tests; to be named to avoid clashing with the existing T1 to T4 thread rules, e.g. TA1 to TA8)
A suggestion is admitted for consideration only if it passes all of these. Passing does not oblige the owner to open it (see 4).
- **TA1. A checkable question.** It asks something evidence could settle: what happened, when, who said or did what, whether a document is genuine, whether a statistic is right, whether a causal claim is supported. It names the claim and says where to look.
- **TA2. Factual, not evaluative.** No judgments of character, intelligence, morality or worth ("idiot", "evil", "corrupt" as a conclusion). A concern behind such a question can be rewritten as a checkable one (for example, "Did X say Y on date Z?").
- **TA3. Neutral wording.** The question does not assume its answer or carry a loaded term. "Why did X lie about Y?" is rewritten as "Was X's statement about Y accurate?".
- **TA4. Public record, not private lives.** It concerns public statements, records, events, documents or objects. It does not target a private individual, ask for personal information or speculate about anyone's beliefs, background, religion, ethnicity, health or motives.
- **TA5. Evidence exists or could exist.** At least one source we can open is named, or the question states what kind of evidence would settle it. Unfalsifiable questions are declined.
- **TA6. Not a campaign.** It is not an advertisement, a request to prove a preferred conclusion, or a way to attach the project's name to a position.
- **TA7. Fits the brand and the taxonomy.** It belongs to an area in `build/taxonomy.yaml`, can be dug to the project's standards (anchors read directly, dates and places where they exist), and is a question about what is known, not what should be done (policy preferences and "should" questions are out of scope).
- **TA8. Harm check.** It does not presume the guilt of a group or promote a conspiracy narrative as a premise. A live event follows the guardrails of `docs/NEWS_REVIEW.md`.

## 4. Decision and records
- Only the owner opens a topic. Counts, reactions and repeats carry no weight; many requests for a topic do not admit it.
- An automated step may check completeness against TA1 to TA8 and label it, but never admits or declines (as in `build/tools/triage_challenge.py`).
- A decline gives the reason by test number and, where possible, a rewritten checkable form. Declines are listed on a public page with their reason, with the submitter's identity left off.
- Admitted topics start as a dig in scoping; they still pass the publish gate and revision rounds like any other.

## 5. What it does not change
No change to claim states, the schema, the validator, the publish gate or the challenge test. It adds a topic form field set and a declined-topics page only, and does not alter any existing finding.

## 6. Impact
Existing digs are unaffected (checked by running the test against their questions below). The News Review issue form and a future "suggest a topic" form would add the questions TA1 to TA8 as fields; docs would link this test.

## 7. Neutrality test (cases that point in different directions)
| Submission | Result | Why |
|---|---|---|
| "Is the president an idiot?" | Declined | TA1, TA2: evaluative, not checkable. Rewrite offered: "Did the president say X on date Y?" |
| "Is the president a genius?" | Declined | Same tests; symmetric. |
| "Prove the election was stolen" | Declined as worded | TA3, TA6: assumes its answer. Rewrite: "Did court cases A to C find fraud affecting the result?" |
| "Prove the election was not stolen" | Declined as worded | Same tests; symmetric. |
| "Did the 1964 Gulf of Tonkin second attack occur?" | Admitted for consideration | Existing dig; checkable, public record. |
| "Do vaccines cause autism?" | Admitted for consideration | Checkable; follows the existing dig's standards. |
| "Is [named private person] a criminal?" | Declined | TA4. |
| "Should the airline be banned?" | Declined | TA7: policy preference. |
| "Was the flight FZ1073 event staged?" | Admitted as a claim to test | TA1, TA5 and the live-event guardrails; worded neutrally. |

## 8. Alternatives considered
- **Do nothing:** declines stay unexplained and arbitrary-looking.
- **Free-form moderation by the owner:** fast but not auditable and exposes the owner to charges of bias; the test makes each decision reproducible.
- **Voting on topics:** rejected; counts carry no weight here.

## 9. Independent assessment and decision (to be completed)
Assessment by an independent reviewer against the seven standards of `docs/SCHEMA_PROPOSALS.md`: pending.
Owner decision: pending.
