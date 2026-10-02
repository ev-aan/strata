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
- **Shared nodes for the other digs.** The Tonkin family is migrated (`build/SCHEMA.md`, Nodes). Casket, Eikon, McAfee, flydubai, Teti and the politics digs still hold their own copies of timeline events.
- **Atlas overview strip.** A draggable mini-map of the whole time range for very long ranges (Teti's 4,000 years), on top of the phone zoom already built.
- **Narrative time on the Atlas.** The data model supports it (`axis: narrative`); the view is switched off until events exist (for example from the Mesopotamian files).
- **Image storage beyond page images.** Thumbnail, link and rights status exist (`build/tools/make_thumb.py`); no copyrighted figures have been added yet.

## Open work noted elsewhere
- Teti: read Sethe 1908 from the Internet Archive page images to fill the hieroglyphs (`build/subjects/teti-pyramid-texts/log.yaml`).
- Gilgamesh seed corpus and retranslation: not yet located.
- Claims whose anchors are secondary only (the conformance warnings).
- Browser checks that need a real browser: `docs/BROWSER_CHECKS.md`.
- Domain and DNS for stratah.org; the homepage and bounty pages still say Strata.
