# Challenges and submitted evidence (policy v0.1, 2026-10-02)

Owner intent: anyone can challenge a finding or add data, and nobody can overturn the system by volume. A challenge is a submission of evidence that must pass our process. It is not a vote.

## Rules
- C1. **Evidence, not numbers.** Counts of challenges, reactions, comments, duplicate submissions, popularity and authority carry no weight. One admitted challenge with real evidence outweighs a thousand without.
- C2. **Admission test.** A challenge is admitted for review only if it meets all five criteria:
  S1 *Specific*: it names one claim and quotes the statement disputed.
  S2 *Evidential*: it gives at least one source the page does not already cite, or shows a different reading of a cited source, with a page or locator.
  S3 *Checkable*: the source is accessible, or the submission says exactly how to obtain it and how it was obtained (so authenticity can be tested).
  S4 *Relevant*: it says which part of the claim it affects (the statement, the anchor, the source's authenticity, the scope, or the confidence) and what the claim should say instead.
  S5 *Not opinion*: it rests on a document, record, measurement or reproducible analysis, not on assertion, motive, or who believes what.
- C3. **One argument, one entry.** A repeat that adds no new evidence is closed and pointed to the existing ledger entry.
- C4. **Same process as any finding.** An admitted source is tested for authenticity (SCHEMA A-rules), read directly, given an evidence class, and counted by independent origin: a source that repeats an origin we already cite adds nothing (N13). Its effect on confidence is written down as reasons (N20).
- C5. **The bar to overturn matches the bar that was met.** To move a claim established at high confidence, the evidence must meet what that claim met (a primary source read directly) or show that the anchor was misread. Weaker evidence can lower confidence only through recorded reasons, and cannot change a claim's state alone. A claim is refuted only under Rule 9: it names its target and rests on material or primary-text evidence.
- C6. **Everything is public.** Admitted challenges appear in the excavation's challenges ledger with an `intake` record (the issue, the date, and each criterion passed or failed). Declined challenges are summarised there too, with the criterion failed and without the submitter's name. Submitters may be credited if they ask.
- C7. **No automated decisions.** Automation checks that the form is complete and flags duplicates and sources already cited. A reviewer, never the submitter and never an automated step, decides admission. The owner holds the final say. Reviewers follow docs/PUBLISH_GATE.md for anything that changes a page.
- C8. **Adding data uses the same gate.** Supporting or extending evidence is submitted the same way and must pass the same test. Supporting evidence from an origin already cited does not raise confidence.
- C9. **Abuse.** Bad-faith, repeated or harassing submissions are closed, and GitHub's own conduct rules apply. Someone who repeatedly submits non-admissible challenges has new ones placed at low priority.

## How it works
1. A reader presses "Challenge or add evidence" on a claim. The button opens the structured GitHub form with the excavation and claim filled in. (GitHub account required: this keeps submissions attributable and rate-limited.)
2. A workflow checks completeness (S1 to S3 by form, duplicates, sources already cited) and labels it `challenge:needs-info` or `challenge:ready`, with a comment listing what is missing. Incomplete ones are closed after 14 days.
3. A reviewer reads a `challenge:ready` submission, decides admission against S1 to S5, and labels it `challenge:admitted` or `challenge:declined`, giving the reason.
4. An admitted challenge is tested as in C4 and the result is one of the ledger's results: answered (finding stands), partly answered, open, or finding changed. Any change to a claim is a new revision with a log entry and, where it applies, an entry on the corrections page.

## Limits
The form cannot prove a source is real; the review does. A reviewer can be wrong, so every outcome is public and can itself be challenged with new evidence. This policy does not decide what is true; it decides what gets examined.
