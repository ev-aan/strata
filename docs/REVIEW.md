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
logs, thread links TH1, TH2 and TH4 (across all subjects), transmission chains X1 to X4, and the
provisional cap on claims marked `absence_anchor: true`. It cannot tell whether a claim *should* have
been marked as resting on absence, so the reviewer checks that (B below). The reviewer covers what the
validator cannot:

**A. Anchors say what the claims say (the core check).**
- Open a sample of the cited sources yourself: at least three, and every anchor of every claim that is
  `refuted`, carries a `headline_claim`, or has `evidential_weight: 5`. Read the passage.
- For each, record: source opened (yes/no), passage found (yes/no), matches the claim (yes/partly/no).
- A source you cannot open is reported as "not checked", never as a pass.

**B. Weights and states are honest.**
- `anchor_checked: primary` only where the primary document was actually read (look for the `# V:` line).
- Any claim whose support is "no record was found" is marked `absence_anchor: true` and held at
  provisional. An unmarked absence claim above provisional is a blocking finding.
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

## What only the owner merges (the gate itself)

A change to any of these is reviewed by an agent but **escalated** to the owner, never merged by an
agent, because a gate reviewed only by agents could lower its own bar:

- `docs/REVIEW.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `build/SCHEMA.md`, `method/index.html` (the rules)
- `build/conformance.py` and anything under `build/tools/` (the checks)
- `.github/` (CI workflows, PR and issue templates) and `netlify.toml` (deploys)

If a PR touches any of these alongside content, the whole PR is escalated.

## Known limit (stated, not hidden)

GitHub cannot require the review agent's approval: the agent posts its verdict as a comment, so
branch protection can require a pull request and a passing `conformance` check, but not the review
itself. The review step holds because agents follow `CLAUDE.md` and the owner merges nothing that has
no posted verdict. Branch protection on `main` is a setting the owner turns on (see `README-deploy.md`).
