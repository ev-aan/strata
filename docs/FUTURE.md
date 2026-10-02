# Future expansions (parked by the owner, 2026-10-02)

Parked means designed or noted, not scheduled. Pick one up by moving it out of this file and logging the decision.

> The public list of ideas is generated from `build/ideas.yaml` and appears on the site at `/ideas/`. Edit that file to add or change an idea; this page keeps the longer notes.

## Parked ideas
- **Academic paper review.** Upload a paper and get a review that adds new information and finds errors and gaps. Design and criteria C1-C6 are in `docs/PAPER_REVIEW.md`. Decisions already made: the paper stays private, only the review is published, nothing changes a dig without passing the criteria and the owner's approval. Waiting for: a first paper to run by hand.
- **Donated agents (owner idea, 2026-10-02).** Publish ideas, claims and open next steps in git as work orders; contributors run their own AI agent on one and submit the result for review. Sketch, not a build:
  - *Work orders:* a generated list of every open `next_step`, searched gap and proposed claim, each with its subject, claim id, what is being asked and what would count as done. The "Start this step" button already creates one issue per step (`docs/DIG_AGENT.md`); this opens the same list to outside agents.
  - *Instructions:* the Start a dig page (`docs/AGENT_RULES.md`) is the portable rule set an outside agent loads.
  - *Submission:* a fork and a pull request, never a push to `main`. Same gate as our own work: validator (`build/conformance.py`), then an independent reviewer who re-opens the cited sources and checks quotes, dates and places. Challenge admission (S1 to S5) applies to anything that disputes a finding.
  - *What it must not do:* more agents, more submissions or more agreement never raise weight; only a source read and checked does. Claims rest on material anchors, not on an agent's say-so. A donated result has to say what it could not read.
  - *Open problems:* untrusted PRs and prompt injection through fetched pages (agents must treat source text as data); duplicate and spam submissions; who reviews at volume without an unpaid owner bottleneck; claiming a work order so two agents do not collide; recording which agent and tool produced what (without naming people); cost and API keys stay with the donor.
  - *First step when picked up:* generate the work-order list from the repository, and run one outside agent by hand on one order to see what breaks.
- **The frontier map: a home for what is not yet known (owner observation, 2026-10-02).** A by-product of the dig format is a boundary layer between what is known and what is not. Today it is already in the data: 23 claims across 9 excavations are `searched_gap` (22 open with a `next_step`, 1 structural with a `gap_reason`), plus contested claims and claims anchored only at secondary level. Sketch, not a build:
  - *A generated Frontier page:* list every gap with its subject, what is unknown, why (source not reachable, record lost, evidence does not exist, method cannot decide), what was tried, and the kind of evidence that would move it. Group by area and by type of obstacle.
  - *A gap record that outlives the dig:* give a gap its own id and a `gap` node so the same unknown can be shared by several digs and stays open after a dig is published; closing it is a log entry that points to the claim that settled it.
  - *Articulating how to push further:* each gap states its next step, what a good answer would look like, and what it would change (which claims and which assessment answers). That is the work order for the donated-agents idea.
  - *Kinds of gap:* missing access (a book or archive we could not open), lost record, unasked question, contested evidence, method limit (structural), and not yet dug.
  - *Care needed:* a gap list must not rank topics by popularity, and an unknown is not evidence for or against anything (absence stays capped at provisional).
  - *First step when picked up:* generate the list from the existing `searched_gap` and contested claims and read it, before adding any new fields.
- **A verified feed (owner idea, 2026-10-02).** Distribution in the manner of a news wire: statements, objects (shared nodes) and timelines are added to a feed that others can carry, and the end reader knows each item passed the Stratah process. Sketch, not a build:
  - *The unit:* a statement (an assessment answer or a claim), an object or event node, or a timeline, each with its review status, `reviewed_on`, review round history and confidence.
  - *The proof:* a mark a reader can verify, not a badge anyone can copy. That means a stable identifier and version per item, a checksum, and a signed manifest (the private export tool already makes checksums; signing needs the owner's own key, `docs/DATA_RELEASE.md`), plus a public verification page that says what the item is, which review passed it, and its current status.
  - *Updates and withdrawals:* publishing is not the end, so the feed must carry corrections and retractions, and a carried copy must be able to show "corrected" or "withdrawn" when the source changes. A mark that cannot go stale is the biggest risk.
  - *Terms of use:* what a distributor may do (carry unaltered, with attribution and a link to the verification page) and may not (alter an item and keep the mark, imply endorsement). This is licensing and name protection, so it ties to the open licence and trademark decision.
  - *Boundaries:* only items that passed review and are on the publish list enter the feed; the data download decision (private for now) stays until the owner lifts it; the mark is never used by or for an outside organisation's name without its agreement.
  - *Open problems:* who signs and how a key is protected or rotated; whether a mark covers an item or each version; how a feed stays honest when the owner's role changes (docs/SCHEMA_PROPOSALS.md); cost and abuse of a public verification service; legal advice on a certification mark.
  - *First step when picked up:* define the item format and verification page for one published item (a single News Review statement), with a signed manifest, and test what breaks when it is corrected.
- **Shared nodes for the other digs.** The Tonkin family is migrated (`build/SCHEMA.md`, Nodes). Casket, Eikon, McAfee, flydubai, Teti and the politics digs still hold their own copies of timeline events.
- **Atlas overview strip.** A draggable mini-map of the whole time range for very long ranges (Teti's 4,000 years), on top of the phone zoom already built.
- **Narrative time on the Atlas.** The data model supports it (`axis: narrative`); the view is switched off until events exist (for example from the Mesopotamian files).
- **Image storage beyond page images.** Thumbnail, link and rights status exist (`build/tools/make_thumb.py`); no copyrighted figures have been added yet.

## Future needs: managing the project in git (noted 2026-10-02)
- **Suggest a dig or idea form.** The Ideas page sends people to a generic issue form.
- **Labels created in advance** (`challenge`, `news-review`, `dig:start`, and the like) with colours and descriptions. The forms apply them, but the repository has to have them.
- **A GitHub Project board** tracking a topic from proposed, digging, in review, to published. Owner setup on GitHub.
- **Branch protection on `main`:** require pull requests and code-owner review (`.github/CODEOWNERS` is in place) so "no pushes to main" is enforced mechanically. Owner setting on GitHub.
- **Work-order list and an issue form for donated agents,** with a way to claim an order so two agents do not collide.
- **Frontier page** generated from the open gaps (see the frontier map idea above).
- **Reviewer capacity:** independent review is the bottleneck at volume; decide who reviews and how reviewers are recorded without a name on the page.
- **Browser check of the generated pages** (Start a dig, News Review, copy button), and a test of the issue forms on GitHub; neither can be run from this environment.

## Open work noted elsewhere
- Teti: read Sethe 1908 from the Internet Archive page images to fill the hieroglyphs (`build/subjects/teti-pyramid-texts/log.yaml`).
- Gilgamesh seed corpus and retranslation: not yet located.
- Claims whose anchors are secondary only (the conformance warnings).
- Browser checks that need a real browser: `docs/BROWSER_CHECKS.md`.
- Domain and DNS for stratah.org; the homepage and bounty pages still say Strata.
