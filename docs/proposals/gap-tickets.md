# Proposal: open-question list and dig tickets (GT1 to GT8)

Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.

Author: an agent. All commands were run on 2026-10-02 in `/home/user/strata` on branch `claude/jolly-hopper-ira8mk` (merged state of `main`, 15 digs), and read-only on `origin/dig/vaccines-autism` (a 16th dig, commit 9a90bf0, not on `main`). Nothing in the repository was changed except this file. GitHub issue creation was not tried and is not assumed to work from this environment; section 2 shows a dry run instead.

Owner principle (conversation, 2026-10-02): "there will always be gaps; our system needs to be transparent about them and open a dig ticket for them." Owner constraint (added by the coordinator, 2026-10-02): "tickets can only be issued by registered accounts." Section 3.4a states how I read that constraint. It is an interpretation for the owner to confirm.

This is the first concrete step of the "frontier map" and "donated agents" ideas in `docs/FUTURE.md` (and `build/ideas.yaml`: `frontier-map`, `donated-agents`). It builds the list and the tickets only. It does not build the gap node, outside-agent intake, or claiming.

## Summary

- Every `searched_gap` claim already says what was tried, what would change it and (almost always) a next step. Today that is visible only as one collapsed claim among many, and each has a "Start this step" link that creates a ticket only if someone clicks.
- Proposal: (a) a generated, deterministic **gap list** with one record per `searched_gap` claim, shown as an "Open questions" section on each dig page and as a `/frontier/` page; (b) one **dig ticket** per open gap on a published dig, created by a script run only in a workflow the owner enables, deduplicated by a marker, closed when the claim stops being a gap.
- **No schema change. No validator change.** The list is derived from fields that already exist.
- Gaps carry no weight. Absence stays capped at provisional. Nothing about claim states, the publish gate or Rule 9 changes.

## 1. The failure case

Gaps are recorded well and are then hard to find, hard to act on as a set, and leave no trail when closed.

**1.1 What exists today, counted.** I read every `build/subjects/*/claims.yaml` (script in scratchpad, YAML parsed, not grepped) and `claims.yaml` on `origin/dig/vaccines-autism`. `state: searched_gap` appears on **35 claims in 10 digs on `main`** and **6 on the vaccines dig** (41 in all). `docs/FUTURE.md` says "23 claims across 9 excavations (22 open with a next_step, 1 structural)"; that figure is out of date (the flydubai and lamp digs were added after it). Of the 41: 39 have a `next_step`; 2 are `gap_type: structural` with a `gap_reason` and no `next_step`.

| Subject | Gap claim ids | next_step | structural | Published (site.yaml) |
|---|---|---|---|---|
| apollo-landings | apollo-original-sstv-tapes-lost | yes | no | no (parked) |
| casket-letters | casket-no-computed-study-found | yes | no | yes |
| congress-promise-vote | pv-barragan-prevote-commitment; pv-inducement-both | yes, yes | no | no (pilot draft) |
| eikon-basilike | eikon-no-computed-study-found; eikon-style-singles-out-gauden | yes, yes | no | yes |
| flydubai-fz1073 | fz1073-descent-magnitude; -weapon-not-established; -omani-nationality-unconfirmed; -how-assigned-gap; -no-findings-yet; -motive-not-established; -timing-convenient; -event-simulated; -arranged-or-allowed; -masks-clean-cabin; -surgeon; -extra-pilots-statistics (12) | yes (12) | no | yes (live News Review) |
| gulf-of-tonkin | tonkin-original-text-missing; tonkin-aug1964-debate-no-doubt-voiced; tonkin-bait-order | yes (3) | no | yes |
| incandescent-lamp | lamp-davy-dates; -de-la-rue-1840; -lodygin-ge-sale; -edison-bought-woodward; -swan-1850s; -swan-litphil-date; -sprengel-link; -goebel-rohde; -latimer-edison-role (9) | yes (9) | no | yes |
| mcafee-and-surfside | mcafee-cause-independent-review | yes | no | yes |
| proto-indo-european | pre-pie-ancestor | **no** | **yes** | no |
| teti-pyramid-texts | pt-373-gatekeeper-identity; pt-304-daughter-of-anubis-identity; teti-hieroglyphic-text-not-in-record | yes (3) | no | no |
| vaccines-autism (branch) | va-whole-schedule-gap; va-fully-unvaccinated-gap; va-thompson-subgroup-real; va-rise-remainder-unexplained; va-causes-largely-unknown; va-small-effect-not-excludable | yes (5), **no (1)** | **1** (va-small-effect-not-excludable) | no (review passed_with_open_items, not in `publish`) |

Five of the 15 digs on `main` have no `claims.yaml` at all (`chemtrails`, `dyatlov-pass`, `flood-myths-worldwide`, `votes-2009-present`, `votes-johnson-tonkin`: log or data files only). A gap list built from claims shows zero for them; that must read as "no claims filed yet", never as "no gaps" (section 4, GT5).

**1.2 What a reader or contributor can and cannot do today.** I ran `python3 build/tools/build_site.py <scratch dir>` (output: "6 excavation(s)") and read the generated pages.
- A reader sees, per dig, one summary line such as "Claims so far: 1 refuted, 15 established, 1 contested, 1 proposed, 3 searched gap." (Tonkin page). The three gap claims are further down, each a collapsed "Evidence and limits" block. There is no list of what is open, no grouping by why it is open, and no page across digs. `/frontier/` does not exist; the site has `/digs/`, `/areas/`, `/ideas/`, `/news/`, `/start/`.
- "Start this step" appears on **68** claims across the six published pages (casket 7, eikon 11, flydubai 18, tonkin 17, lamp 9, mcafee 6), because it is shown for any claim with a `next_step`, not only gaps. Only 28 of those 68 are `searched_gap`. The link opens a pre-filled `dig-step.yml` issue (`build/tools/dig_actions.py`). **No ticket exists unless someone clicks**, and nothing stops two people opening two tickets for the same step: there is no marker and no check.
- No view tells the owner how much open work there is, which gaps are structural, or which have been open longest.
- **A closed gap leaves no trail.** When a claim leaves `searched_gap`, the dig log (append-only) may say so in prose, but nothing links the question to its answer. `git log -S"searched_gap" -- build/subjects` finds the commits that touched the word, not the closed questions.
- Structural gaps read as failures: nothing on a page says that "cannot be closed by more digging" is a different thing from "not yet looked". `proto-indo-european` (parked, unpublished) and `va-small-effect-not-excludable` are the cases. Neither would be published today without that being said.

This is a usability and transparency failure of the system, not a wrong finding: the data is honest; the page makes it hard to see and the tooling does not act on it.

## 2. The evidence

- Counts and ids: section 1.1 (scratchpad script `count.py`, output reproduced in Appendix A).
- Page evidence: section 1.2 (built site in the scratchpad; counts of "Start this step" and `class="pill s-searched_gap"` per page by grep).
- Gap list generated for all digs, deterministically (two runs, `cmp` identical), and a **dry run of the ticket script** (Appendix A and B). Dry-run result on `main`: 35 gap records, **16 tickets would be created**, 19 held (7 because the dig is not published, 12 because the dig is a live News Review the owner has not listed). On the vaccines branch tree: 41 records, still 16 would be created, 25 held (13 not published, 12 live event).
- Idempotence test: I fed the script the 16 payloads it had produced, as "existing issues", plus one extra marker for a claim that does not exist. Result: `create 0, dup 16, close ['gap:gulf-of-tonkin:tonkin-old-closed-claim']`. A rerun creates nothing new, and a ticket whose claim left the list is queued to be closed.
- Validator: `python3 build/conformance.py` on this tree: "15 subjects and 107 shared nodes checked: 0 errors, 93 warnings". The script reads files only (`git status` clean). See section 5.
- Not tested, because it cannot be from here: creating an issue on GitHub; the label and lock calls; a workflow run; how the dig-agent workflow treats a generated ticket. Those statements are from reading `.github/workflows/dig-agent.yml`, `docs/DIG_AGENT.md` and GitHub's published behaviour, and are marked as such.

## 3. The proposed change, exactly

### 3.1 The gap list (generated, deterministic)

One record per `searched_gap` claim, derived only from existing fields. Same tree gives the same list.

| Field | Source | Note |
|---|---|---|
| `marker` | `gap:<subject>:<claim-id>` | stable key; never reused |
| `subject`, `claim_id`, `area` | folder, claim `id`, `build/taxonomy.yaml` | area is the primary area |
| the question | claim `statement` | as published |
| what was tried | `anchor.description` (type is usually `search-record`) | as published |
| `next_step` | claim `next_step` | already required by SCHEMA rule 3 |
| kind of obstacle | derived, see below | |
| what it could move | claim `would_change_if`, plus ids of other claims in the same dig whose text names this id, plus `(headline)` if it is the headline claim | 14 of 35 have a named claim; the rest rest on `would_change_if` alone |
| status | `open` while the claim is `searched_gap`; `closed` when it is not | closed records carry the closing claim id (3.3) |

**Kind of obstacle (derived, in this order, first match wins):** `method_limit` if `gap_type: structural`; `contested` if the claim has `disputed_by` or `positions`; `lost_record` if `anchor.type` is `documented-absence`; `access` if `anchor.type` is `needs-primary-anchor`; `not_yet_dug` if the dig's `dig_status` is `parked` or `pilot_draft`; otherwise `searched_not_found`.

Result on `main`: searched_not_found 27, access 3, lost_record 2, not_yet_dug 2, method_limit 1 (31 / 3 / 2 / 2 / 2 plus 1 contested on the vaccines branch).

**Honest limits of the derivation.** The owner's list has six kinds: access, lost record, unasked, contested, method limit, not yet dug. Two things follow.
1. 27 of 35 records fall in `searched_not_found`, which is the real state ("looked in the places named; nothing found there") and does not say whether the cause is access, a lost record, or a question nobody asked. Splitting it needs a judgement per claim, which I will not invent. I do not add a field to do it (see 3.5). The rule is stated so a reader can see it is a rule, and a reviewer can challenge a classification by changing the claim's `anchor.type`.
2. `unasked` is not derivable from a `searched_gap` at all: an unasked question has no claim. It is left out of v1 and is a later step (the `gap` node in FUTURE.md).

### 3.2 Where it is shown

(a) **Each dig page: an "Open questions" section**, placed after "Where it stands" and before the claims. For each open gap: the question, what was tried, the next step, the kind of obstacle in words, what it could move, and the existing "Start this step" and "Challenge or add evidence" links. Fixed text at the top of the section: "These are the questions this dig looked into and could not settle. An open question is not evidence for or against anything. Some cannot be closed by more digging; those are marked, and they are not failures." Structural gaps are included and carry the `gap_reason` instead of a next step. If a dig has no claims file the section says "No claims have been filed for this dig yet, so no open questions are listed." Order inside the section: by claim order in the file, never by popularity, topic or number of visits.

(b) **`/frontier/`**: all open gaps of all published digs, grouped by area (from taxonomy) and then by obstacle, with the same record fields and a link to the dig page claim. Counts are shown as plain totals per group, with no ranking. Whether the page is public is an owner choice (O5).

(c) The "Start this step" link on a claim that has an open ticket is unchanged in v1 (it cannot know about tickets at build time). Its text is unchanged.

### 3.3 The dig ticket

A GitHub issue per open gap, created by `build/tools/gap_tickets.py` (Appendix B; split into a records module `build/tools/gaps.py`, used by `build_site.py`, and the ticket script, when applied).

- **Dry run by default.** Without `--create` it prints counts per subject, held reasons and sample payloads, and touches nothing. `--create` needs `--repo` and a token; the workflow passes it only when the repository variable `GAP_TICKETS` is `on` (an owner setting, O1).
- **Which gaps get a ticket.** Only if the dig is published (in `build/site.yaml` `publish` and `review.yaml` status in `passed`, `passed_with_open_items` or `grandfathered`; the same test as `build_site.py` and `conformance.py`), the gap is not structural unless the owner marks it, and the dig is not a live News Review unless the owner lists it. `CLAUDE.md` names only `passed` and `passed_with_open_items`; the code also accepts `grandfathered` (four published digs have it). The proposal follows the code and flags the difference for the assessor.
- **Dedupe.** The first line of the body is a hidden marker `<!-- gap:<subject>:<claim-id> -->`. Before creating, the script lists issues with label `gap` (state all, paginated) and parses markers. An existing marker, open or closed, means no new ticket. The marker is in the body and not a label because 7 of 35 markers are longer than GitHub's 50-character label limit (longest 59).
- **Close.** If an open ticket's marker is no longer in the list (the claim is no longer `searched_gap`, or it was removed), the script comments with the subject and claim id and closes it as completed. The comment links the claim on the dig page. If the claim id still exists, the closing claim is that id (its new state is shown on the page); if the id is gone, the comment says so and a maintainer links the replacement. A closed ticket is the persistent trail (the ticket plus the dig's append-only log entry); the page does not list closed questions in v1 (see 3.5 and alternative F).
- **Structural gaps.** No ticket by default. If the owner marks one, the ticket says in its body that it cannot be closed by a find; it is closed by the owner or reviewer with the comment "structural: kept as a recorded limit", and it carries the label `gap:structural` so it is never counted as overdue work.
- **Rate limits.** At most `--max-create` (default 10) tickets per run, 3 seconds apart, so a first run of 16 takes two runs; GitHub applies secondary limits to bursts of content creation. The workflow runs on `workflow_dispatch` and on push to `main` when `build/subjects/**` or `build/site.yaml` changes, never on a schedule more often than daily.
- **Text and names.** Every field in a ticket is copied from the published page. No submitter text enters it. The title is the fixed pattern `Open question: <subject> / <claim-id>` (no statement text, no name). The existing naming rules apply because the source text already passed them (NEWS_REVIEW rule 1: no private individuals; the flydubai guardrails). Because a ticket repeats a claim in a new, more visible place, a ticket for any gap whose claim names a living private individual is not generated; the script cannot detect that, so the holds above (unpublished, live event, structural) are the safeguard and a reviewer checks the dry-run output before the owner switches creation on (O1). This is a limit of the design, listed again in section 8.
- **Labels.** `gap`, `generated`, `gap:<obstacle>`, optionally `gap:structural`. Never `dig:start` (asserted in the script).

### 3.4 How a ticket connects to the existing dig-agent flow

The body reproduces the `dig-step.yml` fields in the layout GitHub gives a submitted form: `### Subject`, `### Claim ID`, `### The step`, `### Notes for the agent (optional)`. The existing workflow `.github/workflows/dig-agent.yml` runs when an issue has the label `dig:start`, on `opened` or `labeled`, and its prompt reads "a subject, optionally a claim ID, and one step". So:
1. The script creates the ticket without `dig:start`. The agent does not run.
2. A collaborator who wants the step worked adds the label `dig:start`. That is a `labeled` event by that person. By `docs/DIG_AGENT.md`, only users with write access reach the agent; anyone else's labelling is ignored by the action. Triage permission lets someone add labels in GitHub; whether `claude-code-action` accepts a triager is stated by the action, not tested here, and should be checked before relying on it (O4).
3. The agent works the step and opens a draft pull request exactly as today; the pull request goes through `docs/REVIEW.md` (conformance, a separate review agent, merge only on APPROVE).
4. The two paths are equivalent: "Start this step" on the page still opens a pre-filled form, and a generated ticket is the same form filled in by the system.
Why the label is not added automatically: an issue created with `GITHUB_TOKEN` does not trigger other workflows (per GitHub's documentation; not tested here), but if the owner ever designates a personal account or token for creation, `opened` plus `dig:start` would start an agent run on every generated ticket. The script therefore refuses to emit `dig:start`.
**Permission model.** Creating tickets: the owner-enabled workflow only (3.4a). Triggering an agent: collaborators with write access only (unchanged). Later, donated agents: out of scope here. A donated agent would use a fork and a pull request, as in FUTURE.md; this proposal only supplies the work orders, and the work-order list is the public `/frontier/` page and the tickets.

### 3.4a Registered accounts: the owner's constraint

Owner constraint: "tickets can only be issued by registered accounts." **My interpretation, for the owner to confirm:**
1. **Human-originated tickets** (challenge, topic or idea suggestion, dig step, News Review, a comment on a gap ticket) require a signed-in GitHub account. GitHub already enforces this for issues. **Stratah creates no anonymous channel**: no email intake, no unauthenticated form, no anonymous API or webhook. Stratah runs no accounts of its own; GitHub's account is the registration. This proposal adds none.
2. **System-generated gap tickets** are created only by the owner-enabled workflow, under the repository's automation identity (`github-actions[bot]` with `GITHUB_TOKEN`, or an account the owner designates), and carry the label `generated`. No outside account can create one through the script or the workflow: the workflow has `workflow_dispatch` (write access needed to run it) and a push-to-`main` trigger only, and no `issues` or `issue_comment` trigger an outsider could fire. The script in `--create` mode reads its repository and token from the workflow environment and takes no input from an issue.
3. **Triggering the dig agent stays limited to collaborators with write access** (`docs/DIG_AGENT.md`). A registered account alone cannot start an agent run.
4. **Options** for what "registered" requires:
   - **A. Any GitHub account (default; what GitHub requires).** No extra work. Anyone with an account can open a challenge or suggestion; they are identifiable by their GitHub login and everything is public.
   - **B. Account age or verified email.** GitHub cannot enforce this on issues natively. A workflow on `issues: opened` could read the author's `created_at` through the users API and label `new-account`. It cannot read email verification (not exposed by the public API). Cost: one more workflow and API call per issue, false positives against genuine new contributors, and a risk of drift toward an automated decline, which `docs/CHALLENGES.md` C7 forbids (automation never admits or declines). At most it could label for a reviewer.
   - **C. Collaborator allow-list.** Already how the agent is triggered. For challenges and suggestions it would contradict GOVERNANCE ("anyone, if it names one claim and gives a source we can check").
   - **Recommendation:** A for submissions, with B only as an optional label if abuse appears; C for agent triggers (already in force). Reason: A meets the constraint as written at no cost, the admission test (S1 to S5) judges the content so account age adds nothing the test does not check, and B or C for public challenges would narrow who can challenge a finding, which the owner's own principle (GOVERNANCE) says to avoid.
5. **What a registered account does not buy.** It confers no weight on content. A count of tickets, accounts, comments or reactions carries no weight (`docs/CHALLENGES.md` C1). An account is not required to **read** gaps: `/frontier/`, the dig page sections and the YAML are public without sign-in.
6. **Existing forms that already satisfy it** (checked in `.github/ISSUE_TEMPLATE`): `config.yml` sets `blank_issues_enabled: false` and its only contact link is a documentation page (no email address); `challenge.yml`, `dig-step.yml`, `news-review.yml` and `open-question.md` are GitHub issue templates, so submission needs a signed-in account; the "Start this step" link (`dig_actions.py`) and the "Challenge or add evidence" link (`build_site.py`) are `issues/new` URLs on GitHub, which sends a signed-out visitor to sign in; the Ideas page sends people to `issues_url` (`issues/new/choose`). The `challenge-intake.yml` workflow runs on issues, so it only sees account-originated tickets. I did not test the forms on GitHub (FUTURE.md notes that cannot be done from here). Pull requests, the other human route in, also need an account. Anything enabled later (GitHub Discussions, an email address in a contact link) would break the constraint and needs this proposal's path.
7. **Harassment and abuse.** Accounts are identifiable, which deters some abuse and lets the owner block or report an account; they do not stop it. Generated tickets carry no submitter text, and the person-risk is mainly in comments. See section 8.

### 3.5 Schema change: none

No new field, no new rule, no change to `build/SCHEMA.md` text beyond one added section "Gap list" that restates what exists (next_step required for a gap; structural gaps carry `gap_type: structural` and `gap_reason`). Proposed text:

> **Gap list (added under docs/proposals/gap-tickets.md).** The gap list is generated from claims in state `searched_gap`: subject, claim id, statement, `anchor.description`, `next_step` (or `gap_reason` when `gap_type: structural`), `would_change_if`, and a derived kind of obstacle (`method_limit`, `contested`, `lost_record`, `access`, `not_yet_dug`, `searched_not_found`; first match wins, in that order). It adds no field and no rule. A gap confers no weight, and absence stays capped at provisional.

Not proposed, so the owner can see what was left out: an explicit `obstacle:` field (would let authors split `searched_not_found`, needs a validator check and a migration of 35 claims); a `closes:` key on log entries (would let the page show closed questions); a shared `gap` node. Each is a later proposal with its own failure case.

### 3.6 Exact change list (when applied; nothing is applied now)

New files: `build/tools/gaps.py` (records, from Appendix B), `build/tools/gap_tickets.py` (tickets), `build/tools/test_gaps.py` (tests: deterministic, held rules, idempotence, no `dig:start`), `.github/workflows/gap-tickets.yml` (below), one added section in `build/SCHEMA.md`, one paragraph in `docs/DIG_AGENT.md`. Changed: `build/tools/build_site.py` (sketch below). Not changed: `build/conformance.py`, any `claims.yaml`.

`.github/workflows/gap-tickets.yml` (sketch):
```yaml
name: Gap tickets
on:
  workflow_dispatch:
  push: {branches: [main], paths: ['build/subjects/**', 'build/site.yaml']}
permissions: {contents: read, issues: write}
jobs:
  tickets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m pip install --quiet pyyaml
      - name: Dry run (always)
        run: python3 build/tools/gap_tickets.py
      - name: Create and close (only if the owner turned it on)
        if: ${{ vars.GAP_TICKETS == 'on' }}
        env: {GH_TOKEN: '${{ secrets.GITHUB_TOKEN }}'}
        run: python3 build/tools/gap_tickets.py --create --repo "$GITHUB_REPOSITORY"
```
Owner setup: create labels `gap`, `generated`, `gap:*` in advance (FUTURE.md already lists labels as needed); Actions "Read and write permissions" for issues.

`build_site.py` sketch (not applied):
```python
import gaps as _gaps
GAPS = _gaps.records(ROOT)                      # all digs, same code path as the ticket script
def open_questions_html(sub):
    rs = [r for r in GAPS if r["subject"] == sub]
    if not rs:
        return '<section id="open-questions"><h2>Open questions</h2><p>No claims have been filed for this dig yet, so none are listed.</p></section>' if no_claims(sub) else ""
    ... intro paragraph (fixed text), then per record: question, tried, next_step or gap_reason, obstacle text,
    would_change_if, could_move links, and _da.start_link(sub, claim) ...
# in the dig page body: body += open_questions_html(sub)   (after assessment, before the claims)
# new page: write("frontier/index.html", ...) grouped by AREAS[area]["name"] then obstacle; add "/frontier/" to urls[]
```
Only published digs are rendered; the same records feed the ticket script.

### 3.7 GitHub-native structure: what to use, and what stays in YAML

The owner asked whether GitHub's own features manage gap questions better than a script. **What I could verify** (read-only GitHub tools, session limited to `ev-aan/strata`, which is the checkout's remote; the code points at `ev-aan/stratah`, which the repository search lists as a public personal-account repo with 2 open issues, and which I could not query directly. I assume the two are the same repository under an old and a new name; **unverified**):
- It is a **personal-account** repository (`user:ev-aan`), not an organization.
- `list_issue_types` returns three default types: Task, Bug, Feature (no custom types). `list_issue_fields` returns an empty list (no custom issue fields).
- The labels `gap`, `dig:start` and `challenge` **do not exist** in the repository. This matters now: the forms name `dig:start` and `challenge` as labels, and `dig-agent.yml` fires only on `dig:start`. If a label does not exist, GitHub does not apply it from a form (**unverified behaviour**, from GitHub's documentation as I recall it), so the "Start this step" flow and challenge intake may not trigger until the owner creates the labels. FUTURE.md already lists "labels created in advance" as owner work; this is the evidence that it is needed, and it is independent of this proposal.
- One issue exists (#5, a follow-up to PR #4). No sub-issues, projects or milestones were read.

Everything else below is **unverified** from this environment (I did not create anything) and comes from GitHub's documentation as I know it; the owner or the assessor should check it on GitHub before relying on it.

| Feature | Use for gaps? | What I can say |
|---|---|---|
| **(a) Issue, one per open gap, marker in body** | **Yes (the proposal's ticket).** | Works on a personal repo today. Verified: issues are available and a ticket can carry labels and a body. The marker gives a stable key the generator can find without a database. |
| **(b) Sub-issues: a parent per dig, a sub-issue per gap** | **Yes, optional, recommended as the default structure.** | The `sub_issue_write` tool exists in this session (verified that the tool exists, not that it works on this repo). Sub-issues are a GitHub feature for repositories generally, including personal ones (unverified). Limits as I recall them: about 100 sub-issues per parent, nesting up to 8 levels (unverified); the dig is one level deep, so no limit is near (max 12 gaps in a dig now). The parent is one issue per published dig, the "prime question", titled by the dig's headline question, with the marker `<!-- dig:<subject> -->`. The generator links each gap ticket to its dig's parent with the API (`POST /repos/{r}/issues/{parent}/sub_issues` with the child's issue id, not number). The parent then shows "n of m done" and the dig's open gaps in one place. Cost: one more object to keep in sync, one more API call per ticket, and a parent that is never "closed" while the dig is live. If linking fails, the ticket is still valid. |
| **(c) Labels** | **Yes, for type, area, obstacle, generated.** | Must be created by the owner (they do not exist now). Proposed: `gap`, `generated`, `gap:<obstacle>` (6), `gap:structural`; the existing form labels `challenge`, `news-review`, `dig:start`, `open-question-proposal`; and `area:<id>` from `build/taxonomy.yaml` (12 areas, 7 in use) so the Frontier groups map to issue filters. About 30 labels; one-time owner setup. Labels are a filter, not a record: the generator re-applies the labels it owns each run, and does not touch others. |
| **(d) Projects (v2)** | **Optional view, not a store.** | A board, table or roadmap with custom fields (subject, area, obstacle, status) over the same issues. Auto-add by a built-in project workflow or an `actions/add-to-project` step. Owner must create the project, the fields and the workflow. A user-owned project cannot be written with `GITHUB_TOKEN`; it needs a personal access token or a GitHub App with project scope (unverified), which is a new secret and a new risk. Projects are private-by-default UI, not a public page; `/frontier/` stays the public view. Good for the owner's triage ("what is open, in review, done") and for the project-board item already in FUTURE.md. |
| **(e) Milestones** | **No (v1).** | A milestone is a date-driven bucket. Gaps have no due dates and "a milestone per dig" duplicates the parent issue. Use only if the owner wants a release-like target such as "dig reaches review". |
| **(f) Issue types and issue fields** | **Not now; an organization would unlock them.** | Verified: only Task, Bug, Feature exist and no fields exist. Custom issue types (for example Gap, Challenge, Topic, News Review) and custom issue fields (subject, obstacle, area as typed, filterable fields, also readable through `list_issues` `field_filters`) are managed at organization level (unverified). Moving the repository to an organization (the owner's possible future) would let type replace the `gap` label and fields replace `gap:<obstacle>` and `area:` labels, with no change to the YAML or the generator beyond which API call sets them. Until then, labels do the same job. Recommend not moving only for this. |
| **(g) Discussions** | **Yes for open conversation and ideas; never for evidence.** | A place for "what should we dig next" and general talk, separate from tickets. Submissions of evidence still go through the challenge form and S1 to S5 (`docs/CHALLENGES.md`); a discussion is not a challenge and carries no weight. Needs a signed-in account (consistent with GT7). Owner must enable it per repository (unverified); off today as far as I know. Enabling it is a new public surface, so it needs the owner's decision (O9). |
| **(h) YAML as source, issues and projects as mirrors** | **Required.** | See the rule below. |
| **(i) Do not use** | | **Wiki:** edits are not reviewed through a pull request and fall outside `docs/REVIEW.md`. **Anything that keeps findings outside the repository** (a project's custom text fields as the record, issue comments as the answer, Discussions as a verdict, an external tracker): it cannot be reviewed, diffed or published by the gate. A gap's answer is a claim in YAML that passed review; the ticket only points at it. |

**Why YAML stays the single source of truth (no drift).** The record of a gap is the claim in `claims.yaml` (reviewed, append-only log, publish gate). A ticket, a sub-issue link, a label and a project card are **derived mirrors** that the generator can rebuild from the YAML at any time. Rules:
- The generator owns the title, the generated part of the body (between the marker and the end), and the labels `gap`, `generated`, `gap:*`, `area:*`. On each run it compares them with the YAML; if they differ because a person edited them, it **restores the generated text and leaves a comment** noting the edit and the restore (or, if the owner prefers, only flags it; O10). Human comments, assignees and other labels are never touched.
- Status flows one way: YAML to ticket. Closing a ticket by hand does not change the claim; the next run reopens it if the claim is still `searched_gap` (with a comment), or confirms the close if it is not. A ticket cannot close a gap.
- Anything a person adds in a ticket (a source, an answer) is not part of the record until it passes the challenge test or a dig step and a reviewed pull request.
- A generated parent or project card carries no information the YAML lacks.

**Recommended default structure** (for the owner to choose; nothing here is built):
1. The proposal's ticket per open gap on a published dig (3.3), labelled `gap`, `generated`, `gap:<obstacle>`, `area:<area>`; owner creates the labels first.
2. One **parent issue per published dig**, with each gap ticket as a sub-issue, if the owner wants the "prime question and its sub-questions" view; skip it first and add it later if sub-issues work as expected on this repository (check on one by hand first).
3. A **Project board** over the issues (fields: subject, area, obstacle, status) as the owner's triage view only, added after the tickets exist and only if the owner accepts a token for it. Without it, the label filters and `/frontier/` do the job.
4. **Discussions** for ideas and conversation, separate from tickets, if the owner wants open talk.
5. No milestones, no wiki, no custom types or fields until an organization move is decided on its own merits.

## 4. Rules (GT1 to GT8)

- **GT1** The gap list has one record per `searched_gap` claim, derived only from existing fields, in a fixed order, and is the same for every dig.
- **GT2** A gap confers no weight. A gap, its count, its age or its ticket never changes a claim's state, confidence, evidential or adoption weight. Absence stays capped at provisional.
- **GT3** Structural gaps are shown and labelled as limits, not as failures or as work to do.
- **GT4** A ticket is generated only for a published dig, never from submitter text, never labelled `dig:start`, and never created by an automated step that outside accounts can trigger.
- **GT5** A dig with no claims file shows "no claims filed yet", never "no gaps".
- **GT6** One ticket per marker `gap:<subject>:<claim-id>`; reruns never duplicate; a ticket is closed when the claim leaves `searched_gap`, with a comment naming the claim.
- **GT7** Human tickets need a signed-in GitHub account; Stratah opens no anonymous channel and runs no accounts; only collaborators with write access can start the dig agent.
- **GT8** The list is ordered by file order, never by popularity, topic or traffic. No page ranks topics by their number of gaps.

## 5. What it does not change

Claim states, confidence, evidential and adoption weights; the publish gate (`docs/PUBLISH_GATE.md`; `review.yaml` is still written only by the independent reviewer); Rule 9 (refutation); absence caps (`absence_anchor: true` stays capped at provisional); anchors (N25); append-only logs; the challenge admission test S1 to S5; the independent review path of `docs/REVIEW.md`; who may merge. A ticket does not admit evidence: anything submitted through a ticket's follow-up goes through the same S1 to S5 test. It does not alter what any existing finding says, so no logged review is needed for existing digs (SCHEMA_PROPOSALS point 4).

## 6. Impact on the 15 digs (and the vaccines dig)

Generated list per dig, from the run in Appendix A. "Section shown" is what the dig page would carry if the dig were published; only published digs get a page, a `/frontier/` entry and tickets.

| Dig | Area | Gap records | Obstacle | Published | Tickets would be created |
|---|---|---|---|---|---|
| apollo-landings | science_nature | 1 | lost_record 1 | no (parked) | 0 |
| casket-letters | history | 1 | searched_not_found | yes | 1 |
| chemtrails | science_nature | 0 (no claims file) | | no | 0 |
| congress-promise-vote | politics | 2 | not_yet_dug 2 | no | 0 |
| dyatlov-pass | history | 0 (no claims file) | | no | 0 |
| eikon-basilike | history | 2 | searched_not_found 2 | yes | 2 |
| flood-myths-worldwide | religion_myth | 0 (no claims file) | | no | 0 |
| flydubai-fz1073 | current_events | 12 | searched_not_found 12 | yes (live) | 0 (held: live News Review) |
| gulf-of-tonkin | politics | 3 | lost_record 1, searched_not_found 2 | yes | 3 |
| incandescent-lamp | technology | 9 | searched_not_found 9 | yes | 9 |
| mcafee-and-surfside | current_events | 1 | searched_not_found | yes | 1 |
| proto-indo-european | language | 1 | method_limit (structural) | no | 0 |
| teti-pyramid-texts | archaeology_texts | 3 | access 3 | no | 0 |
| votes-2009-present | politics | 0 (no claims file) | | no | 0 |
| votes-johnson-tonkin | politics | 0 (no claims file) | | no | 0 |
| vaccines-autism (branch) | not in `taxonomy.yaml` on this tree | 6 | contested 1, method_limit 1, searched_not_found 4 | no | 0 |

Totals: 35 records on `main` (13 in `current_events`, 9 `technology`, 5 `politics`, 3 each `history` and `archaeology_texts`, 1 each `science_nature` and `language`); 16 tickets would be created if every published, non-live dig were ticketed now. The apollo row: its one gap has `anchor.type: documented-absence`, so the derivation returns `lost_record` before the parked-dig test; that is the stated order, and the page would show "lost record" for a parked dig. `searched_not_found` is the honest default and is not a claim that these are access problems.

Migration for each dig: none. No file in any dig changes. **Validator unaffected: no validator change.** `python3 build/conformance.py` before: 15 subjects, 107 nodes, 0 errors, 93 warnings; after (no file in `build/` changes): the same, because the script only reads. The tests in `build/tools/test_gaps.py` cover the new tooling, not the validator.

## 7. Alternatives considered

- **A. Do nothing: keep only the per-claim button.** Rejected: the failure case stands (68 buttons, no overview, duplicates possible, no trail). It is cheap, and still available if the owner prefers.
- **B. Manual issue creation by the owner or agents.** Works at 16 gaps; does not scale and gives no dedupe, so a rerun after a fresh dig duplicates. Rejected as the standing method; usable for the first run if the owner prefers to review each ticket (the dry run supports that).
- **C. One tracking issue per dig.** Fewer tickets (about 6 now) and lower volume, but one issue cannot be closed per gap, cannot be picked up by the dig-agent workflow (one subject, one claim, one step), and a long checklist drifts out of date. Kept as a fallback for volume (O3).
- **D. A GitHub Project board.** Good for ordering and status, already listed in FUTURE.md; but it needs issues to hold, is private to GitHub's UI, and does not render a public page. Compatible with this design as a later view of the same tickets, not a replacement.
- **E. Show the list on the pages but create no tickets.** Meets transparency but not the owner's second half ("open a dig ticket"). It is the safe first step: GT1 to GT3 can ship with no workflow at all. Recommended order if the owner wants to go slowly: pages first, tickets later.
- **G. GitHub-native features instead of, or beyond, plain issues** (sub-issues, Projects, issue types and fields, milestones, Discussions): assessed in 3.7. Used as mirrors or views of the YAML where they help (sub-issues, labels, optionally a project, Discussions for talk); not used as the record, and not adopted where they need an organization or a new token.
- **F. A persistent closed-gap record (a `closes:` log key or a closed-gaps file).** Better than a ticket trail but adds a field and a validator check. Left for a later proposal.

## 8. Neutrality check and risks

**Neutrality.** The list is generated for every dig by the same code. Nothing reads the topic, the direction of the finding or the dig's popularity; the only inputs are the claim's own fields. Test on two digs that point in different directions, using the dry-run output (Appendix A): `gulf-of-tonkin` (politics, `popular_claims: true`, a charged "bait order" question) and `incandescent-lamp` (technology, a priority dispute). `tonkin-bait-order` and `lamp-swan-1850s` both produced a ticket with the same title pattern, the same labels (`gap`, `generated`, `gap:searched_not_found`), the same fields in the same order, and the same fixed sentence that a gap is not evidence either way. Tonkin's gap asks whether a document shows an order to provoke; the ticket carries the claim's own "no such document found" statement and does not take a side. The vaccines dig (medicine, charged) produced its records by the same code: 6 records, including one `contested` and one `method_limit` (`va-small-effect-not-excludable`), held because the dig is not published. A structural gap that cuts against a popular claim and one that cuts for it are treated identically: both are limits, shown with their `gap_reason`.

**Where the design could still favour something, and the safeguards.**
- *Ticket spam and volume for the owner.* 16 tickets now (two runs); the creation cap, the one-ticket-per-marker rule and the held rules bound growth. A ticket per gap is bounded by the number of gaps, which only grows with published digs. If volume becomes a burden the owner can drop to alternative C per dig (O3).
- *Harassment through public tickets about named people.* A generated ticket repeats published text only and names no private individual by the existing rules, but it moves a claim to a more visible place. Mitigations: the live-event hold (12 flydubai gaps include conspiracy-framed questions such as `fz1073-event-simulated`; the dig names no private person, by its guardrails); the reviewer reads the dry run before the owner enables creation; generated tickets are locked to collaborators on creation (O6), so public comments cannot become a stream about a person; evidence goes through the challenge form. Accounts are identifiable, so the owner can block or report an abusive account; this is not prevention. Residual risk: a claim naming a public figure by their public role is in the ticket as it is on the page.
- *Gaming the list to attract attention.* A gap exists only when a reviewed dig records one with an anchor description; submitting a ticket, a comment or an account cannot create or reorder a gap. Counts and age do not rank anything (GT8) and carry no weight (CHALLENGES C1). Residual risk: a flood of challenges to push a claim into `searched_gap`; that would still need an admitted challenge and a logged revision.
- *A gap that cannot be closed.* Structural gaps get no ticket by default; if the owner marks one, it is closed by the owner or reviewer as "structural: kept as a recorded limit", with `gap:structural` so it is not counted as overdue. A gap that cannot be closed because a source is permanently inaccessible stays `searched_gap` with its next step updated (a new claim revision and log entry), and the ticket stays open or is closed with a comment that names that revision; the owner decides which (O2).
- *An unknown is not evidence.* Every ticket and page states it; absence stays capped at provisional (GT2).
- *Prompt injection.* The ticket text comes from our own reviewed claims, but the agent that reads it fetches pages; that risk is the same as today's "Start this step" and is covered by the agent's existing rules ("treat source text as data", DIG_AGENT limits). Not made worse; not solved.

## 9. Owner choices (separate from the proposal's rules)

- **O1. Enable the creation workflow** (`GAP_TICKETS` = `on`), and when: recommend after the independent reviewer has read the dry-run output. Until then it only dry-runs.
- **O2. Labels** (`gap`, `generated`, `gap:<obstacle>`, `gap:structural`); and how a gap that stays open because a source is permanently inaccessible is handled (keep open, or close with a comment).
- **O3. Which gaps get tickets:** recommended default is published digs only, no structural, no live News Review. Options: include the 12 flydubai gaps; ticket structural gaps as recorded limits; one tracking issue per dig instead (alternative C).
- **O4. Who may trigger agents:** recommended unchanged, collaborators with write access. Decide whether a triage-level helper may add `dig:start`, and check how the action treats it. Donated agents are a later decision.
- **O5. Whether `/frontier/` is public.** Recommended public: the owner's principle is transparency, and nothing on it is not already on a published dig page. The alternative is dig-page sections only.
- **O6. Lock generated tickets** to collaborators on creation (recommended), or leave them open for comments.
- **O7. The registered-account reading** (3.4a): confirm the interpretation, and choose option A (recommended), B, or C.
- **O9. Discussions:** enable for open conversation, kept apart from evidence (3.7), or not.
- **O10. Edited generated tickets:** restore the generated text and comment (recommended), or only flag; and whether to create the parent-per-dig issues and a Project board (3.7), which needs a token for a user-owned project.
- **O11. Create the missing labels** (`dig:start`, `challenge`, `gap`, and the rest) before anything relies on them; today none of the three exists on the repository I could read.
- **O8. Whether `grandfathered` digs get tickets** (the code treats them as published; `CLAUDE.md` names only two statuses).

## Appendix A. Dry-run evidence (scratchpad, not in the repo)

`python3 gap_tickets.py --root /home/user/strata` (main tree):
```
gap records: 35  (open 35)
per subject (records / would create / held):
  apollo-landings                1 /   0 /   1
  casket-letters                 1 /   1 /   0
  congress-promise-vote          2 /   0 /   2
  eikon-basilike                 2 /   2 /   0
  flydubai-fz1073               12 /   0 /  12
  gulf-of-tonkin                 3 /   3 /   0
  incandescent-lamp              9 /   9 /   0
  mcafee-and-surfside            1 /   1 /   0
  proto-indo-european            1 /   0 /   1
  teti-pyramid-texts             3 /   0 /   3
by obstacle: {'lost_record': 2, 'searched_not_found': 27, 'not_yet_dug': 2, 'method_limit': 1, 'access': 3}
would create 16, already ticketed 0, would close 0, held 19
held reasons: {'dig not published': 7, 'live News Review, owner has not listed it': 12}

--- sample ticket ---
TITLE: Open question: casket-letters / casket-no-computed-study-found
LABELS: ['gap', 'gap:searched_not_found']
<!-- gap:casket-letters:casket-no-computed-study-found -->
Generated by Stratah from the open-question list. Marker: `gap:casket-letters:casket-no-computed-study-found`.

### Subject

casket-letters

### Claim ID

casket-no-computed-study-found

### The step

Search Google Scholar, Cryptologia and Digital Scholarship in the Humanities; ask the 2023 decipherment team. NARROWED (finding F7): manual comparisons do exist (Bresslau 1882, Sepp); what is unfound is a systematic computed comparison across all surviving French text.

### Notes for the agent (optional)

Question (as published): No computational style comparison of the casket texts against Mary's authenticated French letters has been published, in two web searches.

What was tried: Two web searches by the open question author found no such study; no wider search yet.

Why it is open: searched in the places named; nothing found there.

Would change if: a published computed comparison being found

An open question is not evidence for or against anything; absence stays capped at provisional. Text above is copied from the published page; nothing here comes from a submitter. To send this to the dig agent, a collaborator adds the label `dig:start`.


--- sample ticket ---
TITLE: Open question: eikon-basilike / eikon-no-computed-study-found
LABELS: ['gap', 'gap:searched_not_found']
<!-- gap:eikon-basilike:eikon-no-computed-study-found -->
Generated by Stratah from the open-question list. Marker: `gap:eikon-basilike:eikon-no-computed-study-found`.

### Subject

eikon-basilike

### Claim ID

eikon-no-computed-study-found

### The step

Google Scholar, Digital Scholarship in the Humanities, and the 1950s-2000s literature in The Library ('John Gauden and the Authorship of the Eikon Basilike', not yet read).

### Notes for the agent (optional)

Question (as published): No computational style study of Eikon Basilike has been published, in three web searches.

What was tried: Three web searches by the open question author found no such study.

Why it is open: searched in the places named; nothing found there.

Would change if: a published computed study being found

An open question is not evidence for or against anything; absence stays capped at provisional. Text above is copied from the published page; nothing here comes from a submitter. To send this to the dig agent, a collaborator adds the label `dig:start`.


--- sample ticket ---
TITLE: Open question: eikon-basilike / eikon-style-singles-out-gauden
LABELS: ['gap', 'gap:searched_not_found']
<!-- gap:eikon-basilike:eikon-style-singles-out-gauden -->
Generated by Stratah from the open-question list. Marker: `gap:eikon-basilike:eikon-style-singles-out-gauden`.

### Subject

eikon-basilike

### Claim ID

eikon-style-singles-out-gauden

### The step

Build such a method; Gauden's profile attracts most learned 1640s prose (F9: 17 of 31 passages from eight other clergy were 'nearest Gauden').

### Notes for the agent (optional)

Question (as published): Measured style singles out Gauden as the author: not shown.

What was tried: Not shown: no measurement singles out Gauden. The only comparison run (claim eikon-text-lacks-charles-habits) does not test Gauden.

Why it is open: searched in the places named; nothing found there.

Would change if: a method that separates Gauden from other learned clergy before it is applied to the book

An open question is not evidence for or against anything; absence stays capped at provisional. Text above is copied from the published page; nothing here comes from a submitter. To send this to the dig agent, a collaborator adds the label `dig:start`.

```

The three samples above are the first three tickets in file order (a casket and two eikon). Samples for a politics gap and a technology gap, and the held structural and parked records, follow.

Records for two held digs (JSON fields shortened):
```
{
 "marker": "gap:proto-indo-european:pre-pie-ancestor",
 "area": "language",
 "obstacle": "method_limit",
 "structural": true,
 "published": false,
 "next_step": "",
 "gap_reason": "The comparative method needs attested descendants to compare. Beyond the deepest reconstructable node there are none, so no find of the usual kind can close this.",
 "would_change_if": "",
 "could_move": [
  "indo-anatolian-node"
 ],
 "status": "open"
}
{
 "marker": "gap:apollo-landings:apollo-original-sstv-tapes-lost",
 "area": "science_nature",
 "obstacle": "lost_record",
 "structural": false,
 "published": false,
 "next_step": "Read NASA's 2009 Apollo 11 tape-search report and Goddard's tape inventory and disposal records; log what each shows about the 45 tapes and the dates.",
 "gap_reason": "",
 "would_change_if": "the 45 original tapes, or records of their disposal that contradict NASA's 2009 account, are found",
 "could_move": [],
 "status": "open"
}
```

Tickets for the neutrality test (a politics gap and a technology gap; bodies differ only in their own claim text):

```
TITLE: Open question: gulf-of-tonkin / tonkin-bait-order 
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:gulf-of-tonkin:tonkin-bait-order -->
Generated by Stratah from the open-question list. Marker: `gap:gulf-of-tonkin:tonkin-bait-order`.

### Subject

gulf-of-tonkin

### Claim ID

tonkin-bait-order

### The step

Read SNIE 50-2-64 and the NSA's remaining declassified Tonkin documents (about 140 released in 2005); search each for provocation or bait language; log every hit and every miss.

### Notes for the agent (optional)

Question (as published): No document read or reported so far shows an order to provoke the 2 August clash by sending the Maddox in as bait.

What was tried: Text searches of the Hanyok study found no mention of bait; its only uses of "provocation" concern the Aug 4 incident as the pretext for the Resolution and September 1964 patrols. Prados's essay and the tape commentary say the Maddox's mission was to record North Vietnamese radio and radar emissions expected to rise after a 34-A raid (so the patrol was coordinated with the raids), and that the mission commander "had been briefed in Taiwan previously that there would be" no attack and was unaware of the raids. None describes an order to provoke.

Why it is open: searched in the places named; nothing found there.

Would change if: a document ordering or planning the Maddox patrol as a provocation is found

An open question is not evidence for or against anything; absence stays capped at provisional. Text above is copied from the published page; nothing here comes from a submitter. To send this to the dig agent, a collaborator adds the label `dig:start`.

TITLE: Open question: incandescent-lamp / lamp-swan-1850s 
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:incandescent-lamp:lamp-swan-1850s -->
Generated by Stratah from the open-question list. Marker: `gap:incandescent-lamp:lamp-swan-1850s`.

### Subject

incandescent-lamp

### Claim ID

lamp-swan-1850s

### The step

Search Swan's papers (Tyne and Wear Archives) and the 1929 memoir by his children (not on archive.org) for contemporaneous records.

### Notes for the agent (optional)

Question (as published): Joseph Swan's experiment with a carbonised-paper arch in a vacuum "about twenty years ago" (that is, about 1860) is known only from his own lecture of 20 October 1880. No record from the 1850s or early 1860s was found.

What was tried: Swan, lecture of 20 Oct 1880, Chemical News 42 (5 Nov 1880), pp. 227-230, read: 'an experiment which I tried about twenty years ago'; the carbon arch 'became red-hot' and bent until it broke. Nothing contemporary found.

Why it is open: searched in the places named; nothing found there.

Would change if: a dated notebook, letter or society report from 1850-1865 is found

An open question is not evidence for or against anything; absence stays capped at provisional. Text above is copied from the published page; nothing here comes from a submitter. To send this to the dig agent, a collaborator adds the label `dig:start`.

```

Idempotence and close test (the 16 payloads fed back as existing issues, plus one stale marker):

```
create 0, dup 16, close ['gap:gulf-of-tonkin:tonkin-old-closed-claim']
```

Branch tree (`git archive origin/dig/vaccines-autism build`): 41 records, vaccines-autism 6 / 0 / 6, obstacle counts {lost_record 2, searched_not_found 31, not_yet_dug 2, method_limit 2, access 3, contested 1}, would create 16, held 25 (13 not published, 12 live event).

Gap claims counted by parsing every claims.yaml (`count.py`): 35 on main plus 6 on the branch, as in section 1.1. `build/tools/build_site.py` output: 6 excavation(s), 16 correction note(s); "Start this step" per published page: casket 7, eikon 11, flydubai 18, tonkin 17, lamp 9, mcafee 6.

## Appendix B. `build/tools/gap_tickets.py` (proposed, NOT applied; written in the scratchpad)

One file here for review; when applied it splits into `gaps.py` (`records`, `obstacle`) and `gap_tickets.py` (`ticket`, `plan`, `main`). `--create` was never run.

```python
#!/usr/bin/env python3
"""gap_tickets.py (PROPOSED, not applied). Generates the GAP LIST from claims.yaml and, from it, dig-ticket payloads.

DRY-RUN BY DEFAULT: prints what it would do. It only talks to GitHub with --create, which the workflow passes
only when the owner has set the repository variable GAP_TICKETS=on. Deterministic: same tree, same output.
Usage: gap_tickets.py [--root DIR] [--existing issues.json] [--json] [--create --repo OWNER/REPO] [--max-create N]
"""
import argparse, glob, json, os, re, subprocess, sys, time
import yaml

PUBLISHED_OK = {"passed", "passed_with_open_items", "grandfathered"}   # same set as build_site.py and conformance.py
OBSTACLE_TEXT = {
    "access": "a source exists but has not been opened",
    "lost_record": "the record is documented as lost or missing",
    "contested": "informed sources disagree and the dispute is recorded",
    "method_limit": "the method cannot settle it (structural; not a failure)",
    "not_yet_dug": "the dig is parked or a draft; the question has not been worked",
    "searched_not_found": "searched in the places named; nothing found there",
}

def load(p):
    return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None

def clean(s):
    return " ".join(str(s or "").split())

def obstacle(c, head):
    a = c.get("anchor") if isinstance(c.get("anchor"), dict) else {}
    t = a.get("type")
    if c.get("gap_type") == "structural": return "method_limit"
    if c.get("disputed_by") or c.get("positions"): return "contested"
    if t == "documented-absence": return "lost_record"
    if t == "needs-primary-anchor": return "access"
    if head.get("dig_status") in ("parked", "pilot_draft"): return "not_yet_dug"
    return "searched_not_found"

def records(root):
    cfg = load(os.path.join(root, "build", "site.yaml")) or {}
    published = set(cfg.get("publish") or [])
    tax = (load(os.path.join(root, "build", "taxonomy.yaml")) or {})
    out = []
    for p in sorted(glob.glob(os.path.join(root, "build", "subjects", "*", "claims.yaml"))):
        sub = p.split(os.sep)[-2]
        d = load(p) or {}
        claims = d.get("claims") or []
        rv = (load(os.path.join(os.path.dirname(p), "review.yaml")) or {}).get("status")
        area = ((tax.get("assignments") or {}).get(sub) or {}).get("area", "unassigned")
        for c in claims:
            if c.get("state") != "searched_gap": continue
            a = c.get("anchor") if isinstance(c.get("anchor"), dict) else {}
            cid = c["id"]
            moves = sorted({o["id"] for o in claims if o["id"] != cid and cid in json.dumps(o, default=str)})
            if d.get("headline_claim") == cid: moves.append("(headline)")
            out.append({
                "marker": f"gap:{sub}:{cid}", "subject": sub, "claim_id": cid, "area": area,
                "dig_title": clean(d.get("title")), "slug": d.get("url_slug"),
                "published": sub in published and rv in PUBLISHED_OK, "review_status": rv,
                "live_event": d.get("event_status") == "live",
                "question": clean(c.get("statement")), "tried": clean(a.get("description")),
                "anchor_type": a.get("type"), "next_step": clean(c.get("next_step")),
                "gap_reason": clean(c.get("gap_reason")), "structural": c.get("gap_type") == "structural",
                "obstacle": obstacle(c, d), "would_change_if": clean(c.get("would_change_if")),
                "could_move": moves, "status": "open", "closed_by": None,
            })
    return out

def ticket(r):
    """Same fields as .github/ISSUE_TEMPLATE/dig-step.yml, in the layout GitHub gives a submitted issue form."""
    step = r["next_step"] or ("(structural gap: no step can close it) " + r["gap_reason"])
    body = (f"<!-- {r['marker']} -->\nGenerated by Stratah from the open-question list. Marker: `{r['marker']}`.\n\n"
            f"### Subject\n\n{r['subject']}\n\n### Claim ID\n\n{r['claim_id']}\n\n### The step\n\n{step}\n\n"
            f"### Notes for the agent (optional)\n\n"
            f"Question (as published): {r['question']}\n\nWhat was tried: {r['tried']}\n\n"
            f"Why it is open: {OBSTACLE_TEXT[r['obstacle']]}.\n\nWould change if: {r['would_change_if']}\n\n"
            f"An open question is not evidence for or against anything; absence stays capped at provisional. "
            f"Text above is copied from the published page; nothing here comes from a submitter. "
            f"To send this to the dig agent, a collaborator adds the label `dig:start`.\n")
    labels = ["gap", "generated", f"gap:{r['obstacle']}"] + (["gap:structural"] if r["structural"] else [])
    assert "dig:start" not in labels   # only a collaborator adds dig:start; a generated ticket never starts the agent
    return {"title": f"Open question: {r['subject']} / {r['claim_id']}", "labels": labels, "body": body}

def plan(recs, existing, held_ok=()):
    """existing: list of {number,state,body}. Returns (create, skip_dup, closed_candidates, held)."""
    seen = {}
    for i in existing:
        m = re.search(r"<!-- (gap:[^ ]+) -->", i.get("body") or "")
        if m: seen[m.group(1)] = i
    now = {r["marker"]: r for r in recs}
    create, dup, held = [], [], []
    for r in recs:
        if not r["published"]: held.append((r, "dig not published")); continue
        if r["structural"] and r["marker"] not in held_ok: held.append((r, "structural, not marked for a ticket")); continue
        if r["live_event"] and r["subject"] not in held_ok: held.append((r, "live News Review, owner has not listed it")); continue
        if r["marker"] in seen: dup.append(r); continue
        create.append(r)
    close = [(m, i) for m, i in seen.items() if i.get("state") == "open" and m not in now]
    return create, dup, close, held

def gh(args, data=None):
    return subprocess.run(["gh"] + args, input=data, capture_output=True, text=True, check=True).stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--existing")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--repo")
    ap.add_argument("--max-create", type=int, default=10)
    ap.add_argument("--sample", type=int, default=3)
    a = ap.parse_args()
    recs = records(a.root)
    existing = json.load(open(a.existing)) if a.existing else []
    if a.create and not a.existing:
        existing = json.loads(gh(["api", "--paginate", f"repos/{a.repo}/issues?state=all&labels=gap&per_page=100"]))
    create, dup, close, held = plan(recs, existing)
    if a.json: print(json.dumps(recs, indent=1)); return
    from collections import Counter
    print(f"gap records: {len(recs)}  (open {sum(r['status']=='open' for r in recs)})")
    print("per subject (records / would create / held):")
    for s in sorted({r['subject'] for r in recs}):
        print(f"  {s:28} {sum(r['subject']==s for r in recs):3} / {sum(r['subject']==s for r in create):3} / {sum(r['subject']==s for r in [h[0] for h in held]):3}")
    print("by obstacle:", dict(Counter(r['obstacle'] for r in recs)))
    print(f"would create {len(create)}, already ticketed {len(dup)}, would close {len(close)}, held {len(held)}")
    for r, why in held[:0]: pass
    print("held reasons:", dict(Counter(w for _, w in held)))
    for r in create[:a.sample]:
        t = ticket(r); print("\n--- sample ticket ---\nTITLE:", t["title"], "\nLABELS:", t["labels"], "\n" + t["body"])
    if a.create:
        for r in create[:a.max_create]:
            t = ticket(r)
            made = json.loads(gh(["api", f"repos/{a.repo}/issues", "--input", "-"], json.dumps(t)))
            gh(["api", "-X", "PUT", f"repos/{a.repo}/issues/{made['number']}/lock"])  # owner choice O6: lock to collaborators
            time.sleep(3)
        for m, i in close:
            sub, cid = m.split(":")[1:3]
            gh(["api", f"repos/{a.repo}/issues/{i['number']}/comments", "-f", f"body=Closed: `{cid}` is no longer a searched gap in `{sub}`. See the claim on its dig page."])
            gh(["api", "-X", "PATCH", f"repos/{a.repo}/issues/{i['number']}", "-f", "state=closed", "-f", "state_reason=completed"])
if __name__ == "__main__": main()
```
