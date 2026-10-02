# News Review: rules for checking current stories

News Review is a fact-check that keeps going. It takes a current story or rumour, breaks it into claims, checks each against sources we can open, and keeps a dated log of what was known when. It is built on the same dig format as everything else (claims, anchors, sources, timeline, append-only log, publish gate), plus the rules below.

## What gets reviewed
- The owner chooses what is opened. The public can suggest a story with the "Suggest a News Review" issue form. Nothing is opened because it is popular or because many people ask.
- A suggestion must name the specific claims to check and give at least one source. A request to "prove it was staged" is not a claim; "the report says X, but source Y says Z" is.

## Guardrails (set in the log before any claim is written)
1. Do not name a suspect or a private individual who has not been named by authorities and by multiple independent outlets. Never speculate about religion, ethnicity or beliefs.
2. An accusation is not a finding. Report who said what, and what was shown.
3. A discrepancy between reports is a discrepancy to resolve. It is not evidence of fabrication. "Manufactured" or "staged" is a claim to test: say who did what, how, and what evidence would show it.
4. Early reporting on a live event is often wrong. Log every fact with its source and the time it was reported; later changes are new entries.
5. Wikipedia is never an anchor. Wire reports that copy one another count as one source.

## Entry format
- **Claim by claim.** Each claim is a normal Stratah claim (state, evidence class, confidence, anchor in the one anchor format, would_change_if).
- **What we knew when.** The log is append-only with dated, timed entries. Each entry names the source and what changed.
- **Status label:** live, settled or closed (`event_status` in the log). A live entry shows the "as of" date prominently, and the answer at the top says what is still unknown.
- **Timeline** of the event, with dates, times and places only where a source names them.
- **Primary material first:** official investigation reports, flight/trade/court/agency data, original documents and recordings. Statements by officials are adoption-class until backed by material.
- Same answer block as any dig (answer, 70 to 95 character headline, 3 key points, no percentages). For a live event the answer is usually "unsettled" or "partly", and that is fine.

## Publishing
An entry appears on the site only when its subject is in `build/site.yaml` `publish` and its `review.yaml` has passed (docs/PUBLISH_GATE.md). A separate reviewer, not the author, writes it. A live entry is re-reviewed at each significant update, and its `reviewed_on` date shows.

## Corrections
Visible and permanent: a correction is a new log entry that states what was wrong, and it also appears on the corrections page.
