# How a change gets posted: the review gate

Decided by the owner, 2026-10-02. Nothing reaches `main` (and so the public site) without passing
two separate checks: the **validator** for the mechanical rules, and an **independent review agent**
for the judgment rules a script cannot decide.

## The flow

1. **Branch.** All work goes on a branch: `dig/<subject>`, `fix/<subject>`, `bounty/<id>` or
   `process/<topic>`. Nobody pushes to `main` directly, people or agents.
2. **Validate.** Run `python3 build/conformance.py --base origin/main` locally. Zero errors before a
   pull request is opened.
3. **Pull request.** Open a PR into `main` using the template. CI runs the validator again.
4. **Independent review.** A separate review agent reviews the PR (protocol below). It must not be
   the agent that wrote the change, and it is given only the PR, the repository and this file, never
   the author's conversation or notes. It posts its review on the PR.
5. **Verdict.**
   - `APPROVE`: the review agent merges the PR (squash merge). The site then deploys from `main`.
   - `REQUEST CHANGES`: the author fixes on the same branch and the PR is reviewed again by a fresh
     reviewer. Fixes are new commits and new log entries, never rewrites of reviewed history.
   - `ESCALATE`: the agent does not merge and flags the owner on the PR. Used when the change alters
     rules or the method itself, or when the reviewer cannot check what it needs to.
6. **Record.** The review stays on the PR permanently. Rejected and superseded reviews are kept.

## What the review agent checks

The validator already covers states, classes, weights, required fields, Rules 9 and 12, append-only
logs, threads (T1, T2, T4) and transmission chains (X1 to X4). The reviewer covers what it cannot:

**A. Anchors say what the claims say (the core check).**
- Open a sample of the cited sources yourself: at least three, and every anchor of every claim that is
  `refuted`, carries a `headline_claim`, or has `evidential_weight: 5`. Read the passage.
- For each, record: source opened (yes/no), passage found (yes/no), matches the claim (yes/partly/no).
- A source you cannot open is reported as "not checked", never as a pass.

**B. Weights and states are honest.**
- `anchor_checked: primary` only where the primary document was actually read (look for the `# V:` line).
- Claims resting on absence are marked `absence_anchor: true` and held at provisional.
- Each `refutation_class` meets its bar: `fabrication` needs evidence of deliberate invention;
  `institutional_propaganda` needs an anchored institutional campaign; otherwise use a weaker class.
- `established` without a primary read is flagged for re-anchoring, not downgraded.

**C. Nothing borrows weight.**
- No claim is supported by how many people believe it, by prestige, or by a thread or transmission chain.
- One source is not doing the work of several (citation insularity). Flag claims that share a single anchor.

**D. Every side dug to the same standard.**
- In priority or blame disputes, each claimant faced the same bar. Note any claimant held to a lighter
  or heavier standard.

**E. Surface text is plain and true.**
- `headline`, `search_summary`, `plain_stakes` and similar lines state no more than the claims support,
  and contain no hype.
- Quotations from sources are short and attributed.

**F. The record is intact.**
- Corrections are new log entries; no reviewed content was silently changed.
- The log says what was read and what was blocked.

## Review format (post on the PR)

```
VERDICT: APPROVE | REQUEST CHANGES | ESCALATE
Reviewer: <agent/model>, independent of the author: yes
Validator: <errors>, <warnings>

Sources opened: N of M cited
| claim | source | opened | passage found | matches |

Findings (each with the claim id and the rule):
- [blocking] ...
- [non-blocking] ...

Not checked, and why:
- ...
```

Any `[blocking]` finding means REQUEST CHANGES. Non-blocking findings may be merged and fixed in a
follow-up PR, which is opened before merging.

## What only the owner does

- Changes to these rules, to `CONTRIBUTING.md`, `SCHEMA.md` or `conformance.py` are reviewed by an
  agent but **escalated** to the owner, not merged by the agent. (A rule change reviewed only by
  agents could lower the bar for itself.)
- Branch protection on `main` is a repository setting the owner turns on (see `README-deploy.md`).

## How this fits the publish gate (reconciled 2026-10-02)
Two controls work together and neither replaces the other.
- **This file (the PR gate)** decides how a change reaches `main`: on a branch, validated, reviewed by a separate agent, merged only on APPROVE. Nobody pushes to `main`.
- **The publish gate** ([`PUBLISH_GATE.md`](PUBLISH_GATE.md)) decides what appears on the site: a subject listed under `publish` in `build/site.yaml` needs `build/subjects/<subject>/review.yaml` with a status of `passed` or `passed_with_open_items`; the validator and the site build refuse it otherwise.
When a PR adds a subject to `publish`, the independent review agent is the reviewer for the publish gate. It does the checks above, then writes the verdict into `review.yaml` (status, `reviewed_by`, `reviewed_on`, `notes`, `open_items`) in the same PR. `python3 build/tools/review_dig.py <subject>` gives it a mechanical first pass. The author never writes their own `passed`.
The challenge rules ([`CHALLENGES.md`](CHALLENGES.md)) decide what public submissions get examined. A change a challenge produces goes through this file like any other change.

