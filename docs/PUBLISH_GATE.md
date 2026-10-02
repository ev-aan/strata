# Publish gate: no excavation goes live without a review (2026-10-02)

Owner decision: every new excavation is reviewed for errors before it is published. The rule is enforced in the repository, not by habit.

## The rule
A subject listed under `publish` in `build/site.yaml` must have `build/subjects/<subject>/review.yaml` with a `status` of `passed`, `passed_with_open_items` or `grandfathered`.
`build/conformance.py` fails (so the deploy workflow stops) and `build/tools/build_site.py` refuses to build if a published subject has no such record. Taking a subject off the list needs no review.

## Statuses
- `pending`: a review has been started; not allowed to publish.
- `passed`: reviewed, no open items that affect what a reader is told.
- `passed_with_open_items`: reviewed; the open items are listed in the record and are shown on the page as limits (for example claims anchored to secondary sources).
- `grandfathered`: published by the owner before this gate existed. The record says what was and was not checked. Not available to new excavations.
- `revisions_requested`: the reviewer has sent the work back to the author with specific requests (see Revision rounds). Not allowed to publish.
- `failed`: errors found; not allowed to publish until fixed and re-reviewed.

## How a review is done
1. `python3 build/tools/review_dig.py <subject> --write` runs the mechanical checks and writes `review.yaml` as `pending`: conformance for the subject, the headline rules (70-95 characters; the headline claim established or refuted at high confidence with a primary check, otherwise the headline stays draft), a complete assessment (question, answer, exactly three key points, no percentages), a taxonomy entry, a statement kind on every claim, a next step on every searched gap, a sources manifest with an authenticity block for each source, a log and a timeline.
2. The reviewer then does what a script cannot, and records it in `notes`:
   - open each cited source and confirm the quoted wording, dates, names and document or patent numbers; quotes the tool could not match to a stored source are listed as `needs_manual_check`;
   - confirm every refuted claim names its target and rests on material or primary-text evidence (Rule 9);
   - confirm nothing goes beyond what was read, and that what was not read is marked not read;
   - confirm every nonprimary anchor behind an established or refuted claim is stated as a limit;
   - read the assessment against the claims it cites: the answer, the lean, and the three key points must not say more than the claims do;
   - check images and quotations for rights (short quotations only; thumbnails and links for copyrighted images).
3. Set `status`, `reviewed_by`, `reviewed_on`, and list any `open_items`. The reviewer is the independent review agent of [`REVIEW.md`](REVIEW.md), never the author. Agent output is not authority: the reviewer verifies the key quotes personally.
4. Add the subject to `publish` in `build/site.yaml`. Merging to main deploys it.

## Revision rounds: push back to the author before publishing
Like academic peer review, a review is a conversation, not a stamp. The reviewer does not fix the author's work and the author does not mark their own work passed.
1. **Request.** The reviewer sets `status: revisions_requested` and adds a round to `rounds:` in `review.yaml`, each request with an `id`, the claim or file it concerns, what is wrong or unclear, the evidence (a source opened by the reviewer), and a `severity` of `blocking` (a reader would be misled) or `non_blocking`.
2. **Author response.** The same submitting agent (or its owner) answers each request: `fixed` (with the commit and what changed), `disputed` (with a source showing why the finding is wrong) or `deferred` (with a reason; a deferred non-blocking request becomes an open item). Corrections are new log entries; reviewed history is not rewritten.
3. **Resolution.** A reviewer who did not write the work reads each response against the sources and marks each request `resolved: true` or sends it back for another round. Every blocking request must have an author response and `resolved: true` before the status can be `passed` or `passed_with_open_items`; the validator checks this.
4. **Record.** Every round stays in `review.yaml`, including disputed requests and who was right. Rounds are never deleted.
```yaml
rounds:
  - round: 1
    reviewed_on: 2026-10-02
    requests:
      - id: R1-1
        target: lamp-10000-ways-quote
        severity: blocking
        finding: "The statement says the wording is not documented in Edison's lifetime, but the only anchor is a 1910 book."
        author_response: {action: fixed, note: "Reworded to 'earliest version found'; caveat moved to confidence reasons.", commit: abc1234}
        resolved: true
```

## Publishing is not the end
A passed review is the start of public scrutiny, not its end. After publication the excavation stays open: challenges and submitted evidence (docs/CHALLENGES.md), new sources, and live-event updates (docs/NEWS_REVIEW.md) all feed back in. A change that alters a finding goes through the same loop: a new log entry, a revision round, an independent check, and a visible correction. The page shows when it was last reviewed, and every earlier state stays in the record.

## Limits
A mechanical pass is necessary, not sufficient. The quote check only sees sources stored in the subject's folder and tolerates OCR noise; it never replaces opening the source. The gate checks that a review exists and its status, not that the reviewer was right. Corrections after publication are logged and shown on the corrections page.
