# Proposal B: one explicit owner-only list in the review gate

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`, split out of PR #4. Not in force. Needs an independent assessment, then the owner's decision. This proposal touches rules documents (`docs/REVIEW.md`, `CLAUDE.md`), so it is itself owner-only. It does not depend on Proposal A: the REVIEW.md text that mentions the thread and chain checks refers to the rule ids in `build/SCHEMA.md` without naming them, so it is accurate whether or not A is in force.

## 1. The failure case
`CLAUDE.md` step 5 on main tells the review agent that "changes to rules, `CONTRIBUTING.md`, `SCHEMA.md`, `conformance.py` or `docs/REVIEW.md`" are escalated. "Rules" is not defined, and `docs/REVIEW.md` on main has no list at all. Meanwhile `.github/CODEOWNERS` and `docs/GOVERNANCE.md` already put much more under the owner. A review agent following only CLAUDE.md and REVIEW.md cannot tell whether a PR touching `build/taxonomy.yaml`, `build/site.yaml`, a `review.yaml`, `docs/CHALLENGES.md` or `docs/SCHEMA_PROPOSALS.md` is escalated or mergeable. Concrete case: the original PR #4 tried to fix this with a list that omitted exactly those paths (list: `REVIEW.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SCHEMA.md`, `method/index.html`, `conformance.py`, `build/tools/`, `.github/`, `netlify.toml`) and replaced the word "rules"; under that text an agent could merge a change to `docs/SCHEMA_PROPOSALS.md`, the standards document itself. That wording is withdrawn.

## 2. Evidence
Sources read in this repository: `.github/CODEOWNERS` (owner on `/CLAUDE.md`, `/CONTRIBUTING.md`, `/docs/`, `/build/SCHEMA.md`, `/build/conformance.py`, `/build/site.yaml`, `/build/news.yaml`, `/build/tools/`, `/.github/`, `**/review.yaml`); `docs/GOVERNANCE.md` ("Agents never merge these" for rules, schema, validator; "Publish: Owner (the `publish` list and a passed `review.yaml`)"); `docs/SCHEMA_PROPOSALS.md` ("Agents never make these changes"; changed only by the proposal path); `docs/PUBLISH_GATE.md` (review agent writes `review.yaml`). Gap check, listing paths that main's rules put under the owner and whether each appears in the old PR #4 list: docs/SCHEMA_PROPOSALS.md no, docs/GOVERNANCE.md no, docs/PUBLISH_GATE.md no, docs/CHALLENGES.md no, docs/NEWS_REVIEW.md no, build/site.yaml no, build/news.yaml no, build/taxonomy.yaml (not in CODEOWNERS; it is the taxonomy the publish gate checks) no, review.yaml no. Licence files and `CODEOWNERS` itself: covered via `.github/` and the licence files (see 3).

## 3. The change, exactly
`docs/REVIEW.md`, section "What only the owner merges (the gate itself)": a list that is a superset of CODEOWNERS:
- the rules and the process: `CLAUDE.md`, `CONTRIBUTING.md`, everything under `docs/`
- `build/SCHEMA.md`, `build/conformance.py`, `build/tools/`
- `build/site.yaml`, `build/news.yaml`, `build/taxonomy.yaml`
- every `build/subjects/<subject>/review.yaml`
- `.github/`, `method/index.html`, `netlify.toml`, the licence files (`LICENSE*`)
A PR touching any of them with content is escalated whole. The flow in `docs/REVIEW.md` is made explicit: step 5 APPROVE says the agent merges "unless the PR touches an owner-only path", in which case it posts APPROVE and escalates; ESCALATE lists "the PR touches any owner-only path". A change to a rule, schema or validator also needs a proposal under `docs/SCHEMA_PROPOSALS.md`. Plus a "Known limit" section stating GitHub cannot require the review agent's approval. `CLAUDE.md` step 5 keeps main's wording ("rules, CONTRIBUTING.md, SCHEMA.md, conformance.py or docs/REVIEW.md") and adds one sentence defining "rules" as that list, which includes everything in CODEOWNERS and a few paths beyond it. REVIEW.md also gets two reviewer-level rules that are part of this proposal: an unmarked absence claim above provisional is a blocking finding (section B of the review), and "the owner merges nothing that has no posted verdict" in the Known limit. It also gets the validator-covers list completed (N25, publish gate, taxonomy, challenge checks, N26), a sentence that the PR gate has two checks and the publish gate sits on top of it, and a sentence that because `site.yaml` and `review.yaml` are owner-only, a PR that publishes a subject is reviewed by the agent (which writes `review.yaml`, per PUBLISH_GATE.md) and merged by the owner. `README-deploy.md` and `method/index.html` each get one line aligned with this. No validator change.
Additions beyond CODEOWNERS: `build/taxonomy.yaml`, `method/index.html`, `netlify.toml` and the licence files. CODEOWNERS is owner-only and is not edited here; the owner may decide to add these paths to it or to drop them from the list.

## 4. What it does not change
No claim, state, anchor or log in any dig; no validator behaviour; nothing in `docs/PUBLISH_GATE.md`, `GOVERNANCE.md`, `SCHEMA_PROPOSALS.md` or CODEOWNERS. It narrows nothing that main's rules already reserve to the owner. Main's "How this fits the publish gate (reconciled 2026-10-02)" section and its N25 bullet are kept verbatim.

## 5. Impact on all 15 digs
Documentation only (no validator change; the owner-only list is a procedural rule enforced by agents following CLAUDE.md and by CODEOWNERS plus branch protection, see the Known limit). Validator before and after is the same on every dig: main 0 errors, 93 warnings; this branch 0 errors, 93 warnings (full-output diff empty); per-dig table in `docs/proposals/validator-thread-links.md` section 5 applies unchanged. Migration: none. Effect on process: a PR that adds a subject to `publish` (for example the vaccines-autism dig) is merged by the owner, not by the agent, because it changes `build/site.yaml` and `review.yaml`; this already matches CODEOWNERS and GOVERNANCE.
**Every new-dig PR becomes owner-merged, not only publish PRs.** A new dig must add a taxonomy entry (`build/taxonomy.yaml`; `check_taxonomy` and `review_dig.py` require it), carries a `pending` `review.yaml` written by `review_dig.py --write`, and usually adds `docs/reviews/*` rounds. Under the list each of those is owner-only. CODEOWNERS already does this for `review.yaml` and `docs/`; `taxonomy.yaml` is what this proposal adds. Agents may still merge a PR that only changes claims, logs, sources or other files inside an existing dig.

## 6. Alternatives considered
- **Do nothing:** "rules" stays undefined for the agent.
- **Point agents at CODEOWNERS only:** one source of truth, but the review agent is told to read only the PR, the repository and REVIEW.md, and CODEOWNERS enforcement needs a branch protection setting (the known limit).
- **PR #4's original shorter list:** rejected, it lowers the bar (section 1).
- **A validator check that fails a PR touching owner-only paths without an owner label:** needs CI context and a rule change; out of scope; could be proposed later.

## 7. Neutrality check
The list is by path, not by topic, direction or author. Applied to two digs pointing in different directions, `gulf-of-tonkin` and `incandescent-lamp`: an edit to either dig's claims is a content change merged by the agent on APPROVE; an edit to either dig's `review.yaml` or its entry in `build/site.yaml` is escalated. Both behave identically.

## 8. Owner choices (not decided here)
- **`build/taxonomy.yaml`:** (a) add to CODEOWNERS, so the whole new-dig flow needs the owner (consistent, one source of truth, more owner merges); (b) drop it from the list, so agents can add taxonomy entries (fewer owner merges; the taxonomy then changes without owner review, though it decides where a dig appears).
- **`method/index.html`, `netlify.toml`, `LICENSE*`:** in the list here, not in CODEOWNERS. They change rarely, so adding them to CODEOWNERS is cheap; dropping them from the list is also defensible, since none is a rule. The licence files state the terms of the content.
- **`README-deploy.md` and `CNAME`:** in neither the list nor CODEOWNERS. `README-deploy.md` holds the instructions for the branch protection that makes the gate hold, and `CNAME` sets the public domain; whether either is owner-only is for the owner. Also uncovered and not rules: `README.md`, root `index.html`, `build/ideas.yaml`, `build/definitions/`, `build/nodes/`, `build/imports/`, `questions/`.
- `docs/proposals/topic-admission.md` on main says "the existing T1 to T4 thread rules"; that is Proposal A's concern and is not edited here.

## 9. Independent assessment and decision
Independent assessment: docs/reviews/assessment-topic-proposal-pr4-pr6.md, section 3 (required change B). Second assessment (head b5306bc): meets with specific changes, addressed in the following commit. Re-assessment of the revised text: pending. Owner decision: pending.
