# Proposal: a list of what each dig leaves unsettled, and dig tickets for it (GT1 to GT9)

Status: DRAFT proposal under docs/SCHEMA_PROPOSALS.md. Not in force. Needs an independent assessment, then the owner's final approval.

Author: an agent. All commands were run on 2026-10-02 in `/home/user/strata` on branch `claude/jolly-hopper-ira8mk` (merged state of `main`, 15 digs), and read-only on `origin/dig/vaccines-autism` (a 16th dig, commit 9a90bf0, not on `main`). Nothing in the repository was changed except this file. GitHub issue creation was not tried and is not assumed to work from this environment; section 2 shows a dry run instead.

Revision 2, 2026-10-02: answers the independent assessment (`scratchpad/assessment-gap-tickets.md`, verdict "meets the standards with specific changes", required changes R1 to R12). Section 10 lists each change and where it is made. This file stays on the branch `claude/jolly-hopper-ira8mk` for now; it should go out as its own `process/gap-tickets` pull request, not bundled with the other proposals on this branch (R11).

**Naming.** "Open question" is already a Stratah object (Q-001 and Q-002 under `/questions/`, the `open-question.md` form, label `open-question-proposal`; SCHEMA, Terminology), and `/questions/` pages carry hand-written "Open gaps" lists (G-01 and so on). To avoid a third meaning, this proposal calls the generated section **"Unsettled in this dig"**, the page **/frontier/**, the record a **gap record**, and the ticket title **"Unsettled in dig: <subject> / <claim-id>"**. (R1)

Owner principle (conversation, 2026-10-02): "there will always be gaps; our system needs to be transparent about them and open a dig ticket for them." Owner constraint (added by the coordinator, 2026-10-02): "tickets can only be issued by registered accounts." Section 3.4a states how I read that constraint. It is an interpretation for the owner to confirm.

This is the first concrete step of the "frontier map" and "donated agents" ideas in `docs/FUTURE.md` (and `build/ideas.yaml`: `frontier-map`, `donated-agents`). It builds the list and the tickets only. It does not build the gap node, outside-agent intake, or claiming.

## Summary

- Every `searched_gap` claim already says what was tried, what would change it and (almost always) a next step. Today that is visible only as one collapsed claim among many, and each has a "Start this step" link that creates a ticket only if someone clicks.
- Proposal: (a) a generated, deterministic **gap list** with one record per `searched_gap` claim, shown as an "Unsettled in this dig" section on each dig page and as a `/frontier/` page; (b) a **dig ticket** for each open gap on a published dig **that the independent reviewer has listed as ticketable**, created by a script run only in a workflow the owner enables, locked on creation, deduplicated by a marker, closed when the claim stops being a gap.
- **No claim-schema change. No validator change.** The list is derived from fields that already exist. The one new convention is an optional `ticketable_gaps:` list in a dig's `review.yaml`, written by the reviewer (3.3); conformance already ignores unknown keys in that file (checked: 0 errors with the key added to a copy).
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

**1.3 A second, hand-written gap list already exists (R1).** `questions/casket-letters/index.html` and `questions/eikon-basilike/index.html` (the former "bounties", now `/questions/`) carry **12** hand-written "Open gaps": G-01 to G-05 for casket and G-01 to G-07 for eikon (checked by grep of the page source). They are not in any `claims.yaml` (the dig files only refer to them in prose), have no "Start this step" link, and would get no record, ticket or `/frontier/` entry. The same two subjects therefore show two different lists: 1 and 2 `searched_gap` claims in the digs against 5 and 7 gaps on the question pages. **Scope decision:** v1 generates only from `claims.yaml`, so the G-gaps stay out. They are named here so nobody takes `/frontier/` for the whole picture; `/frontier/` and each dig page must link to the question page when one exists, and bringing the G-gaps into the one list (by filing each as a claim, or by generating the question page from the same records) is a separate step for the owner (O12).

This is a usability and transparency failure of the system, not a wrong finding: the data is honest; the page makes it hard to see and the tooling does not act on it.

## 2. The evidence

- Counts and ids: section 1.1 (scratchpad script `count.py`, output reproduced in Appendix A).
- Page evidence: section 1.2 (built site in the scratchpad; counts of "Start this step" and `class="pill s-searched_gap"` per page by grep).
- Gap list generated for all digs, deterministically (two runs, `cmp` identical), and a **dry run of the ticket script** (revised; Appendix A and B). On `main`: 35 gap records, **16 gaps are eligible** (published, not structural, not a live News Review), 7 are held because the dig is not published, 12 because the dig is a live News Review. **With the reviewer-list rule below, 0 tickets would be created today**, because no `review.yaml` lists any gap; the 16 are what a reviewer could list. Dry run with `--show-eligible` (pretends everything eligible was listed): 16 would be created. Branch tree: 41 records, 16 eligible, 25 held.
- Tests (new, `test_gaps.py`, Appendix C, run in the scratchpad: 7 tests, OK): deterministic output; no ticket without a reviewer listing; idempotent rerun (16 created then `create 0, dup 16`); unpublish closes a dig's tickets generically; a missing `claims.yaml` closes nothing and flags; reopen only for tickets the generator closed; a removed claim closes as `not_planned`; the label `dig:start` is never emitted.
- Validator: `python3 build/conformance.py` on this tree: "15 subjects and 107 shared nodes checked: 0 errors, 93 warnings". The script reads files only (`git status` clean). With `ticketable_gaps: [lamp-davy-dates]` added to a copy of `incandescent-lamp/review.yaml`, conformance still reports 0 errors, 93 warnings, and the dry run then creates exactly 1 ticket. See section 5.
- Not tested, because it cannot be from here: creating an issue on GitHub; the label and lock calls; reopen and close calls; a workflow run; `gh api --paginate --slurp` against a repository with more than 100 issues (the flag is documented in `gh api --help`, from the assessment); how the dig-agent workflow treats a generated ticket. Those statements are from reading `.github/workflows/dig-agent.yml`, `docs/DIG_AGENT.md` and GitHub's published behaviour, and are marked as such.

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

**The `anchor.type` values the derivation depends on (R7).** `build/SCHEMA.md` N25 lists the type as a free text ("primary_text, material, dataset, search-record, ..."). The derivation reads exactly two values, `documented-absence` (a record documented as lost or never made; used by `apollo-original-sstv-tapes-lost`, `tonkin-original-text-missing`) and `needs-primary-anchor` (a primary text not yet opened; the three Teti gaps). These are conventions in today's files, not defined in SCHEMA.md. Other values seen on gap claims (`search-record`, `absence-in-searched-record`, `searched-absence`, `method-horizon`, `stated-limit`, `retracted-reanalysis`, `residual`) fall through to `searched_not_found` or are covered by `gap_type`. The SCHEMA paragraph in 3.5 defines the two values it reads. A classification is never changed by editing `anchor.type` for display: the anchor type is an evidence field, and a reviewer who disagrees with an obstacle kind says so in the review, not by editing the anchor. `contested` is untested on `main` (0 of 35 gap claims have `disputed_by` or `positions`); the vaccines branch has 1.

**Honest limits of the derivation.** The owner's list has six kinds: access, lost record, unasked, contested, method limit, not yet dug. Two things follow.
1. 27 of 35 records fall in `searched_not_found`, which is the real state ("looked in the places named; nothing found there") and does not say whether the cause is access, a lost record, or a question nobody asked. Splitting it needs a judgement per claim, which I will not invent. I do not add a field to do it (see 3.5). The rule is stated so a reader can see it is a rule, and a reviewer can challenge a classification by changing the claim's `anchor.type`.
2. `unasked` is not derivable from a `searched_gap` at all: an unasked question has no claim. It is left out of v1 and is a later step (the `gap` node in FUTURE.md).

### 3.2 Where it is shown

(a) **Each dig page: an "Unsettled in this dig" section**, placed after "Where it stands" and before the claims. For each open gap: the statement, what was tried, the next step, the kind of gap in words, what it could move, and the existing "Start this step" and "Challenge or add evidence" links. Fixed text at the top: "These are the questions this dig looked into and could not settle. An unsettled question is not evidence for or against anything. Some cannot be closed by more digging; those are marked, and they are not failures." Structural gaps are included and carry the `gap_reason` instead of a next step. If the dig has a page under `/questions/`, the section links to it and says it has its own list. If a dig has no claims file the section says "No claims have been filed for this dig yet, so none are listed." Order: claim order in the file, never by popularity, topic or visits.

(b) **`/frontier/`**: all open gaps of all published digs, grouped by area (from taxonomy) and then by obstacle, with the same record fields and a link to the dig page claim. **No counts per area or per obstacle are shown** (R8): a total per group invites ranking topics by their number of gaps, which GT8 forbids, and counts mostly measure how many gaps an author chose to file. Within a group the order is dig order then claim order. The page opens with a note that it lists only generated gaps and links to the `/questions/` pages. Whether the page is public is an owner choice (O5).

(c) The "Start this step" link on a claim that has an open ticket is unchanged in v1 (it cannot know about tickets at build time). Its text is unchanged.

### 3.3 The dig ticket

A GitHub issue per open gap, created by `build/tools/gap_tickets.py` (Appendix B; split into a records module `build/tools/gaps.py`, used by `build_site.py`, and the ticket script, when applied). Everything below is implemented in the Appendix B script and covered by Appendix C unless it says otherwise.

- **Dry run by default.** Without `--create` it prints counts per subject, held reasons and sample payloads, and touches nothing. `--create` needs `--repo` and a token; the workflow passes it only when the repository variable `GAP_TICKETS` is `on` (O1).
- **Which gaps get a ticket (R5).** A gap gets a ticket only if all of these hold: the dig is published (in `build/site.yaml` `publish` with a `review.yaml` status the gate accepts); the gap is not structural (unless listed and the owner agrees, O3); the dig is not a live News Review (`event_status: live`); and **the independent reviewer has listed the claim id** under `ticketable_gaps:` in the dig's `review.yaml`. The author never writes it (the same rule as `review.yaml`). Default is none: **today 0 tickets would be created**. Reason: the script cannot detect a private or living person in claim text, so the check is a person reading each gap, recorded where the review is recorded. Real cases a reviewer must decide: `mcafee-cause-independent-review` (its statement and anchor mention that "the widow" asked for another autopsy of a deceased public figure; whether to repeat that in a ticket is a reviewer judgment); `va-thompson-subgroup-real` (branch, unpublished: concerns a named federal scientist's statement and a result about a racial subgroup; it should not be ticketed without a close read). Listing one gap does not list another. Unlisting a claim id makes its ticket close generically (below).
- **Dedupe by marker, not by label (R3).** The first line of every ticket body is the hidden marker `<!-- gap:<subject>:<claim-id> -->`. Each run lists **all** issues in the repository (state all, `gh api --paginate --slurp`, flattened; the flag is needed because without it each page is a separate JSON array and parsing fails beyond 100 issues), skips pull requests, and finds markers in bodies, whatever labels the issue carries. Removing the `gap` label therefore cannot cause a duplicate. The marker is in the body, not a label, because 7 of 35 markers exceed GitHub's 50-character label limit (longest 59).
- **Concurrency.** The workflow has `concurrency: {group: gap-tickets, cancel-in-progress: false}`, so two runs never read an empty list at once.
- **Lock is mandatory (R2).** A generated ticket is locked immediately after creation. Reason: when a collaborator adds `dig:start`, the dig agent reads the issue and its comments; on an unlocked ticket any registered account could post instructions first. If the lock call fails, the script closes the new ticket as `not_planned` and **exits with an error** (the job fails, nothing further is created). Each run also audits all open generated tickets and locks any that are not. There is a short window between creation and lock (two calls, no agent can start in it because `dig:start` is never added by the system). A locked ticket takes no outside comments; an outsider with a lead on a gap has the challenge form (for disputing a stated claim) and a pull request. A separate "lead on a gap" form is not in this proposal.
- **Close, reopen, hold (R4).** The script closes a ticket only on evidence:
  - the claim id is in a subject whose `claims.yaml` loads and the id is gone or no longer `searched_gap`: close with `state_reason: not_planned` when the id is gone (removed or renamed), and the page shows the claim's new state when it exists. The comment names the subject and claim id. (`completed` is not used by the script: whether a gap was answered is a reviewer's reading, and a person can re-close a ticket as completed.)
  - the dig is no longer published, or the claim is no longer listed, or the dig became live: close as `not_planned` with a generic comment that repeats no claim text, so a dig that failed re-review does not keep its claims public in tickets.
  - **a missing or unreadable `claims.yaml`, or a renamed subject folder, closes nothing**: the tickets are reported as "flagged" and a person looks. (Before this revision a vanished file would have closed all of a dig's tickets; tested.)
  - **Closing cap:** more than `--max-close` (default 5) closes in one run stops the run with an error.
  - **Reopen:** a ticket the generator closed carries the label `gap-closed`. If its gap is eligible again (claim is a gap again, dig republished, listed again) the script reopens it and removes the label, with a comment. A ticket closed by a person, without that label, is left closed and reported; the generator never overrides a person.
- **Structural gaps.** No ticket by default. If the reviewer lists one and the owner allows it (O3), the body says it cannot be closed by a find; it is closed by the owner or reviewer as `not_planned` with "structural: kept as a recorded limit". It carries the label `gap:method_limit` like any other method-limit gap (a separate `gap:structural` label is dropped as a duplicate).
- **Rate and volume.** At most `--max-create` (default 10) per run, 3 seconds apart, and no more while 30 generated tickets are open (`--max-open`). The workflow runs on `workflow_dispatch` and on push to `main` when `build/subjects/**` or `build/site.yaml` changes.
- **Text and names (R6).** Every field is copied from the published claim, in its own wording: the statement, the anchor description as "What was tried (as published)", `next_step`, `would_change_if`, and the dig page URL with the claim anchor. The fixed sentence "searched in the places named; nothing found there" is gone: it was wrong for `casket-no-computed-study-found` (two web searches, "no wider search yet") and `lamp-lodygin-ge-sale` (sources only seen in search results). The derived kind is stated as "Kind of gap (derived)", and for `searched_not_found` reads "not found in what was read; see 'What was tried' for how far the search went". The title is a fixed pattern with ids only. No submitter text enters a ticket. Naming policy is applied by the reviewer's listing, not by the script (NEWS_REVIEW rule 1 and AGENT_RULES apply to the source claim text).
- **Labels.** `gap`, `generated`, `gap:<obstacle>`, and `gap-closed` (set and removed by the generator). Never `dig:start` (asserted in the script and tested). Labels must exist or be created on first use; see 3.7.
- **Incentive.** A gap now produces a page entry and, if listed, a ticket, so an author could file `proposed` to avoid attention or file more gaps to gain it (lamp has 9 of the 16 eligible). The reviewer-list rule removes the automatic link between number of gaps and number of tickets; the reviewer's checks of anchors (Rule 9, absence caps) still decide how a claim is filed. This is a risk, not a solved problem.

### 3.4 How a ticket connects to the existing dig-agent flow

The body reproduces the `dig-step.yml` fields in the layout GitHub gives a submitted form: `### Subject`, `### Claim ID`, `### The step`, `### Notes for the agent (optional)`. The existing workflow `.github/workflows/dig-agent.yml` runs when an issue has the label `dig:start`, on `opened` or `labeled`, and its prompt reads "a subject, optionally a claim ID, and one step". So:
1. The script creates the ticket without `dig:start` and locks it. The agent does not run.
2. A collaborator who wants the step worked adds the label `dig:start`. That is a `labeled` event by that person. By `docs/DIG_AGENT.md`, only users with write access reach the agent. **That check is made by `claude-code-action`, not by anything in `dig-agent.yml`** (the workflow only tests for the label); I could not read the action's source here, so this is from its documentation and is unverified. Today the only collaborator is the owner (read from the repository, section 3.7), so the owner is the only person who can add the label.
3. The agent works the step and opens a draft pull request exactly as today; the pull request goes through `docs/REVIEW.md` (conformance, a separate review agent, merge only on APPROVE).
4. The two paths are equivalent: "Start this step" on the page still opens a pre-filled form, and a generated ticket is the same form filled in by the system.
Why the label is not added automatically: an issue created with `GITHUB_TOKEN` does not trigger other workflows (per GitHub's documentation; not tested here), but if the owner ever designates a personal account or token for creation, `opened` plus `dig:start` would start an agent run on every generated ticket. The script therefore refuses to emit `dig:start`.
**Noise from the existing form (stated, not new).** `dig-step.yml` applies `dig:start` automatically, so any registered account that submits the form starts a workflow job, which then fails the action's permission check (wasted runner minutes, no agent work, no write). This exists today; this proposal neither causes nor fixes it. Generated tickets avoid it because they do not carry `dig:start`.

**Permission model.** Creating tickets: the owner-enabled workflow only (3.4a). Triggering an agent: collaborators with write access only (unchanged). Later, donated agents: out of scope here. A donated agent would use a fork and a pull request, as in FUTURE.md; this proposal only supplies the work orders, and the work-order list is the public `/frontier/` page and the tickets.

### 3.4a Registered accounts: the owner's constraint

Owner constraint: "tickets can only be issued by registered accounts." **My interpretation, for the owner to confirm:**
1. **Human-originated tickets** (challenge, topic or idea suggestion, dig step, News Review). Generated gap tickets are locked, so there is no outside comment route on them require a signed-in GitHub account. GitHub already enforces this for issues. **Stratah creates no anonymous channel**: no email intake, no unauthenticated form, no anonymous API or webhook. Stratah runs no accounts of its own; GitHub's account is the registration. This proposal adds none.
2. **System-generated gap tickets** are created only by the owner-enabled workflow, under the repository's automation identity (`github-actions[bot]` with `GITHUB_TOKEN`, or an account the owner designates), and carry the label `generated`. No outside account can create one through the script or the workflow: the workflow has `workflow_dispatch` (write access needed to run it) and a push-to-`main` trigger only, and no `issues` or `issue_comment` trigger an outsider could fire. The script in `--create` mode reads its repository and token from the workflow environment and takes no input from an issue.
3. **Triggering the dig agent stays limited to collaborators with write access** (`docs/DIG_AGENT.md`). A registered account alone cannot start an agent run.
4. **Options** for what "registered" requires. A and B and C are about human submissions; D is about who issues system tickets:
   - **A. Any GitHub account (default; what GitHub requires).** No extra work. Anyone with an account can open a challenge or suggestion; they are identifiable by their GitHub login and everything is public.
   - **B. Account age or verified email.** GitHub cannot enforce this on issues natively. A workflow on `issues: opened` could read the author's `created_at` through the users API and label `new-account`. It cannot read email verification (not exposed by the public API). Cost: one more workflow and API call per issue, false positives against genuine new contributors, and a risk of drift toward an automated decline, which `docs/CHALLENGES.md` C7 forbids (automation never admits or declines). At most it could label for a reviewer.
   - **C. Collaborator allow-list.** Already how the agent is triggered. For challenges and suggestions it would contradict GOVERNANCE ("anyone, if it names one claim and gives a source we can check").
   - **D. An accountable identity for system tickets.** A stricter reading of "registered" is that even system tickets must be issued by a named, owner-registered account, not an anonymous bot: the owner's own account, or a named GitHub App the owner registers. Issues created with `GITHUB_TOKEN` are attributed to `github-actions[bot]`, not to the person who clicked "Run workflow", so the bot reading loses who enabled it. D needs a secret (a personal access token or App credentials). Cost and effect: the created issue then fires `issues: opened`, which is safe here (no `dig:start`, no `challenge` label, so no workflow acts; checked by reading the three workflows) but would start a job if the label were ever added by the script (it is asserted never to be). A PAT is tied to a person and needs rotation. **Whether the bot counts as "registered" is the owner's call (O7).**
   - **Recommendation:** A for submissions, with B only as an optional label if abuse appears; C for agent triggers (already in force); D for system tickets if "registered" means accountable. Reason: A meets the human reading at no cost, D is the choice if the owner means an accountable identity for system tickets (otherwise the bot is acceptable once the owner confirms in writing that a workflow identity counts), the admission test (S1 to S5) judges the content so account age adds nothing the test does not check, and B or C for public challenges would narrow who can challenge a finding, which the owner's own principle (GOVERNANCE) says to avoid.
5. **What a registered account does not buy.** It confers no weight on content. A count of tickets, accounts, comments or reactions carries no weight (`docs/CHALLENGES.md` C1). Account creation on GitHub is free and unlimited, so an account gives identification, not trust or rate limiting. An account is not required to **read** gaps: `/frontier/`, the dig page sections and the YAML are public without sign-in.
6. **Existing forms that already satisfy it** (checked in `.github/ISSUE_TEMPLATE`): `config.yml` sets `blank_issues_enabled: false` (this removes the form path only: a signed-in account can still create an arbitrary issue through the REST API; it is still no anonymous channel) and its only contact link is a documentation page (no email address); `challenge.yml`, `dig-step.yml`, `news-review.yml` and `open-question.md` are GitHub issue templates, so submission needs a signed-in account; the "Start this step" link (`dig_actions.py`) and the "Challenge or add evidence" link (`build_site.py`) are `issues/new` URLs on GitHub, which sends a signed-out visitor to sign in; the Ideas page sends people to `issues_url` (`issues/new/choose`). The `challenge-intake.yml` workflow runs on issues, so it only sees account-originated tickets. I did not test the forms on GitHub (FUTURE.md notes that cannot be done from here). Pull requests, the other human route in, also need an account. Anything enabled later (GitHub Discussions, an email address in a contact link) would break the constraint and needs this proposal's path.
7. **Harassment and abuse.** Accounts are identifiable, which deters some abuse and lets the owner block or report an account; they do not stop it. Generated tickets carry no submitter text, and the person-risk is mainly in comments. See section 8.

### 3.5 Schema change: none to claims; one text addition to SCHEMA.md; one optional review key

No new claim field, no new claim rule, no validator change. Two text changes need the owner (changes to `SCHEMA.md` are escalated, `CLAUDE.md`):

1. **A "Gap list" paragraph in `build/SCHEMA.md`. This is the first place SCHEMA.md defines `gap_type` and `gap_reason` (R7).** Today they appear only in `build/conformance.py` lines 190 to 197 (a structural gap needs `gap_reason` instead of `next_step`; any other `gap_type` is an error) and in `docs/AGENT_RULES.md` line 26. SCHEMA rule 3 reads "`searched_gap` needs `next_step`" with no structural exception, which contradicts the validator. The paragraph therefore documents existing behaviour, not a new rule, and the same edit reconciles rule 3 ("or, for `gap_type: structural`, a `gap_reason`"). Proposed text:

> **Gap list (added under docs/proposals/gap-tickets.md).** A claim in state `searched_gap` names what would close it in `next_step`, or, when `gap_type: structural`, why nothing can close it in `gap_reason` (as `conformance.py` already requires). The gap list is generated from these claims: subject, claim id, `statement`, `anchor.description`, `next_step` or `gap_reason`, `would_change_if`, and a derived kind of obstacle: `method_limit` (`gap_type: structural`), `contested` (the claim has `disputed_by` or `positions`), `lost_record` (`anchor.type: documented-absence`, a record documented as lost or never made), `access` (`anchor.type: needs-primary-anchor`, a primary text not yet opened), `not_yet_dug` (the dig's `dig_status` is `parked` or `pilot_draft`), otherwise `searched_not_found`; first match wins, in that order. It adds no field. A gap confers no weight, and absence stays capped at provisional.

2. **An optional `ticketable_gaps:` list in a dig's `review.yaml`** (claim ids the independent reviewer has read and allows to become public tickets). Not validated; conformance ignores unknown keys in that file (checked). Written only by the reviewer. A validator check that each id is a `searched_gap` claim is possible but not proposed.

Not proposed, so the owner can see what was left out: an explicit `obstacle:` field (would let authors split `searched_not_found`, needs a validator check and a migration of 35 claims); a `closes:` key on log entries; a shared `gap` node. Each is a later proposal with its own failure case.

**Reconciling `grandfathered` (R10).** `CLAUDE.md` names only `passed` and `passed_with_open_items` as statuses that allow publishing. `conformance.py:636`, `build_site.py:185` and `docs/PUBLISH_GATE.md` (lines 6 and 13) also accept `grandfathered`, and four published digs (casket-letters, eikon-basilike, gulf-of-tonkin, mcafee-and-surfside) hold it, with the record saying partial review and no independent reviewer. This proposal does not decide it. It needs its own owner-escalated change to `CLAUDE.md` or to the gate. It matters for the numbers: under the code reading 16 gaps are eligible; under the `CLAUDE.md` reading only `incandescent-lamp` (9) qualifies, so **16 becomes 9** (the 7 from the four grandfathered digs drop out, and flydubai's 12 stay held because it is live). Recommendation in O8: ticket nothing from a grandfathered dig until the two agree.

### 3.6 Exact change list (when applied; nothing is applied now)

New files: `build/tools/gaps.py` (records, from Appendix B), `build/tools/gap_tickets.py` (tickets), `build/tools/test_gaps.py` (Appendix C; also added as a step to `deploy.yml` so GT1, GT4, GT6 are tested on every push, R8), `.github/workflows/gap-tickets.yml` (below), one added section in `build/SCHEMA.md`, one paragraph in `docs/DIG_AGENT.md`. Changed: `build/tools/build_site.py` (sketch below). Not changed: `build/conformance.py`, any `claims.yaml`. GT1 to GT9: GT1, GT4, GT6 and GT9 are tested by `test_gaps.py`; GT2, GT3, GT5 and GT8 are display rules that only a reviewer reading the generated pages enforces, and no validator enforces any of them.

`.github/workflows/gap-tickets.yml` (sketch):
```yaml
name: Gap tickets
on:
  workflow_dispatch:
  push: {branches: [main], paths: ['build/subjects/**', 'build/site.yaml']}
permissions: {contents: read, issues: write}
concurrency: {group: gap-tickets, cancel-in-progress: false}
jobs:
  tickets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: python3 -m pip install --quiet pyyaml
      - name: Tests
        run: python3 -m unittest build/tools/test_gaps.py
      - name: Dry run (always)
        run: python3 build/tools/gap_tickets.py
      - name: Create and close (only if the owner turned it on)
        if: ${{ vars.GAP_TICKETS == 'on' }}
        env: {GH_TOKEN: '${{ secrets.GITHUB_TOKEN }}'}
        run: python3 build/tools/gap_tickets.py --create --repo "$GITHUB_REPOSITORY"
```
Owner setup: create labels `gap`, `generated`, `gap-closed`, `gap:<obstacle>` in advance (the REST create-issue call may create missing labels itself for a user with push access; unverified, test once by hand); the explicit `permissions:` block above is enough for create, comment, close and lock.

`build_site.py` sketch (not applied):
```python
import gaps as _gaps
GAPS = _gaps.records(ROOT)                      # all digs, same code path as the ticket script
def unsettled_html(sub):
    rs = [r for r in GAPS if r["subject"] == sub]
    if not rs:
        return '<section id="unsettled"><h2>Unsettled in this dig</h2><p>No claims have been filed for this dig yet, so none are listed.</p></section>' if no_claims(sub) else ""
    ... intro paragraph (fixed text), then per record: question, tried, next_step or gap_reason, obstacle text,
    would_change_if, could_move links, and _da.start_link(sub, claim) ...
# in the dig page body: body += unsettled_html(sub)   (after assessment, before the claims)
# new page: write("frontier/index.html", ...) grouped by AREAS[area]["name"] then obstacle, with no counts; add "/frontier/" to urls[]
```
Only published digs are rendered; the same records feed the ticket script.

### 3.7 GitHub-native structure: what to use, and what stays in YAML

The owner asked whether GitHub's own features manage gap questions better than a script. **What I could verify** (read-only GitHub tools, session limited to `ev-aan/strata`, which is the checkout's remote; the code points at `ev-aan/stratah`, which the repository search lists as a public personal-account repo with 2 open issues, and which I could not query directly. I assume the two are the same repository under an old and a new name; **unverified**):
- It is a **personal-account** repository (`user:ev-aan`), not an organization.
- `list_issue_types` returns three default types: Task, Bug, Feature (no custom types). `list_issue_fields` returns an empty list (no custom issue fields).
- The labels `gap`, `dig:start` and `challenge` **do not exist** in the repository. This matters now: the forms name `dig:start` and `challenge` as labels, and `dig-agent.yml` fires only on `dig:start`. Whether GitHub applies a label named in an issue form when the label does not exist is **unverified** (and the REST create-issue call may create missing labels itself for a user with push access, also unverified); test once by hand. If it does not, the "Start this step" flow and challenge intake do not trigger until the owner creates the labels. FUTURE.md already lists "labels created in advance" as owner work; this is the evidence that it is needed, and it is independent of this proposal.
- One issue exists (#5, a follow-up to PR #4). No sub-issues, projects or milestones were read.
- (From the assessment's read-only checks, not re-run by me.) The public repository has its **wiki enabled** and Discussions off; the only collaborator is the owner (admin). So today the owner alone can run the new workflow and add `dig:start`.

Everything else below is **unverified** from this environment (I did not create anything) and comes from GitHub's documentation as I know it; the owner or the assessor should check it on GitHub before relying on it.

| Feature | Use for gaps? | What I can say |
|---|---|---|
| **(a) Issue, one per open gap, marker in body** | **Yes (the proposal's ticket).** | Works on a personal repo today. Verified: issues are available and a ticket can carry labels and a body. The marker gives a stable key the generator can find without a database. |
| **(b) Sub-issues: a parent per dig, a sub-issue per gap** | **Yes, optional, recommended as the default structure.** | The `sub_issue_write` tool exists in this session (verified that the tool exists, not that it works on this repo). Sub-issues are a GitHub feature for repositories generally, including personal ones (unverified). Limits as I recall them: about 100 sub-issues per parent, nesting up to 8 levels (unverified); the dig is one level deep, so no limit is near (max 12 gaps in a dig now). The parent is one issue per published dig, the "prime question", titled by the dig's headline question, with the marker `<!-- dig:<subject> -->`. The generator links each gap ticket to its dig's parent with the API (`POST /repos/{r}/issues/{parent}/sub_issues` with the child's issue id, not number). The parent then shows "n of m done" and the dig's open gaps in one place. Cost: one more object to keep in sync, one more API call per ticket, and a parent that is never "closed" while the dig is live. If linking fails, the ticket is still valid. |
| **(c) Labels** | **Yes, for type, area, obstacle, generated.** | Must be created by the owner (they do not exist now). Proposed: `gap`, `generated`, `gap-closed`, `gap:<obstacle>` (6; `gap:method_limit` covers structural gaps, so there is no separate `gap:structural`); the existing form labels `challenge`, `news-review`, `dig:start`, `open-question-proposal`; and `area:<id>` from `build/taxonomy.yaml` (12 areas, 7 in use) so the Frontier groups map to issue filters. About 30 labels; one-time owner setup. Labels are a filter, not a record: the generator re-applies the labels it owns each run, and does not touch others. |
| **(d) Projects (v2)** | **Optional view, not a store.** | A board, table or roadmap with custom fields (subject, area, obstacle, status) over the same issues. Auto-add by a built-in project workflow or an `actions/add-to-project` step. Owner must create the project, the fields and the workflow. A user-owned project cannot be written with `GITHUB_TOKEN`; it needs a personal access token or a GitHub App with project scope (unverified), which is a new secret and a new risk. Projects are private-by-default UI, not a public page; `/frontier/` stays the public view. Good for the owner's triage ("what is open, in review, done") and for the project-board item already in FUTURE.md. |
| **(e) Milestones** | **No (v1).** | A milestone is a date-driven bucket. Gaps have no due dates and "a milestone per dig" duplicates the parent issue. Use only if the owner wants a release-like target such as "dig reaches review". |
| **(f) Issue types and issue fields** | **Not now; an organization might unlock them (uncertain).** | Verified: only Task, Bug, Feature exist and no fields exist; that three default types appear on a user-owned repository sits oddly with "types are an organization feature", so I label that claim uncertain and it is not a reason either way. Custom issue types (for example Gap, Challenge, Topic, News Review) and custom issue fields (subject, obstacle, area as typed, filterable fields, also readable through `list_issues` `field_filters`) are managed at organization level (unverified). Moving the repository to an organization (the owner's possible future) would let type replace the `gap` label and fields replace `gap:<obstacle>` and `area:` labels, with no change to the YAML or the generator beyond which API call sets them. Until then, labels do the same job. Recommend not moving only for this. |
| **(g) Discussions** | **Yes for open conversation and ideas; never for evidence.** | A place for "what should we dig next" and general talk, separate from tickets. Submissions of evidence still go through the challenge form and S1 to S5 (`docs/CHALLENGES.md`); a discussion is not a challenge and carries no weight. Needs a signed-in account (consistent with GT7). Owner must enable it per repository (unverified); off today as far as I know. Enabling it is a new public surface, so it needs the owner's decision (O9). |
| **(h) YAML as source, issues and projects as mirrors** | **Required.** | See the rule below. |
| **(i) Do not use** | | **Wiki:** edits are not reviewed through a pull request and fall outside `docs/REVIEW.md`. **The wiki is enabled on the public repository today** (from the assessment); whether outside accounts can edit it depends on a setting I cannot read. Owner action, independent of this proposal: turn it off or restrict it to collaborators (O11). **Anything that keeps findings outside the repository** (a project's custom text fields as the record, issue comments as the answer, Discussions as a verdict, an external tracker): it cannot be reviewed, diffed or published by the gate. A gap's answer is a claim in YAML that passed review; the ticket only points at it. |

**Why YAML stays the single source of truth (no drift).** The record of a gap is the claim in `claims.yaml` (reviewed, append-only log, publish gate). A ticket, a sub-issue link, a label and a project card are **derived mirrors** that the generator can rebuild from the YAML at any time. Rules:
- The generator owns the title, the generated body and the labels `gap`, `generated`, `gap-closed`, `gap:*`. **It does not compare or restore edits** (the earlier draft said it would; that was not implemented and is dropped, R4): on a user-owned repository only the owner and collaborators can edit another account's issue, and an overwrite could erase a legitimate annotation. Human comments, assignees and other labels are never touched.
- Status flows one way: YAML to ticket. Closing a ticket by hand does not change the claim, and the generator does not reopen a ticket a person closed; it reports it ("flagged"). It reopens only a ticket **it** closed (label `gap-closed`) whose gap is eligible again. A ticket cannot close a gap.
- Anything a person adds in a ticket (a source, an answer) is not part of the record until it passes the challenge test or a dig step and a reviewed pull request.
- A generated parent or project card carries no information the YAML lacks.

**Recommended default structure** (for the owner to choose; nothing here is built):
1. The proposal's ticket per open gap on a published dig (3.3), labelled `gap`, `generated`, `gap:<obstacle>`, `area:<area>`; owner creates the labels first.
2. **Defer** a parent issue per published dig with sub-issues: it needs its own marker, close rule and rename handling that the script does not have. Add later if the owner wants the "prime question and sub-questions" view, after checking sub-issues by hand on this repository.
3. **Defer** a Project board (new token, new sync surface); the label filters and `/frontier/` do the job first.
4. **Discussions:** not yet. Leave them off until the tickets are stable; if enabled later, keep them apart from evidence and link the S1 to S5 rule.
5. No milestones, no wiki, no custom types or fields until an organization move is decided on its own merits.

## 4. Rules (GT1 to GT9)

- **GT1** The gap list has one record per `searched_gap` claim, derived only from existing fields, in a fixed order, and is the same for every dig. (Tested.)
- **GT2** A gap confers no weight. A gap, its count, its age or its ticket never changes a claim's state, confidence, evidential or adoption weight. Absence stays capped at provisional. (Display rule.)
- **GT3** Structural gaps are shown and labelled as limits, not as failures or as work to do. (Display rule.)
- **GT4** A ticket is generated only for a published, non-live dig and only for a claim the independent reviewer listed; never from submitter text; never labelled `dig:start`; always locked; and never created by an automated step that outside accounts can trigger. (Tested, except the trigger rule, which is a property of the workflow file.)
- **GT5** A dig with no claims file shows "no claims filed yet", never "no gaps". (Display rule.)
- **GT6** One ticket per marker `gap:<subject>:<claim-id>`, found by marker in the body, never by label; reruns never duplicate; a ticket is closed only on evidence (the claim is gone or no longer a gap, or the dig is withdrawn or unlisted), never on a missing or unreadable file, and not more than the per-run cap. (Tested.)
- **GT7** Human tickets need a signed-in GitHub account; Stratah opens no anonymous channel and runs no accounts; only collaborators with write access can start the dig agent (checked by the action, not the workflow).
- **GT8** The list is ordered by file order, never by popularity, topic or traffic. No page shows counts per area or obstacle or ranks topics by their number of gaps. (Display rule.)
- **GT9** A generated ticket is never the record: it mirrors the YAML. A ticket cannot close a gap, and a person's close is not overridden. (Tested for the reopen case.)

Enforcement, stated honestly (R8): `test_gaps.py` is added to CI (`deploy.yml` and the new workflow) and covers GT1, GT4, GT6 and GT9. GT2, GT3, GT5, GT7 and GT8 are not enforced by any validator or test; they are held by the reviewer who reads the generated pages and by the workflow file's triggers.

## 5. What it does not change

Claim states, confidence, evidential and adoption weights; the publish gate (`docs/PUBLISH_GATE.md`; `review.yaml` is still written only by the independent reviewer); Rule 9 (refutation); absence caps (`absence_anchor: true` stays capped at provisional); anchors (N25); append-only logs; the challenge admission test S1 to S5; the independent review path of `docs/REVIEW.md`; who may merge. The proposed `ticketable_gaps` key is a reviewer's record, not a finding, and changes no review verdict. A ticket does not admit evidence: anything submitted through a ticket's follow-up goes through the same S1 to S5 test. It does not alter what any existing finding says, so no logged review is needed for existing digs (SCHEMA_PROPOSALS point 4).

## 6. Impact on the 15 digs (and the vaccines dig)

Generated list per dig, from the run in Appendix A. "Tickets" is what the reviewer could list (eligible), under the code reading of the publish gate; with the reviewer-list rule **none is created until a reviewer lists it**. Only published digs get a page entry, a `/frontier/` entry and tickets.

| Dig | Area | Gap records | Obstacle | Published | Eligible for a ticket if listed |
|---|---|---|---|---|---|
| apollo-landings | science_nature | 1 | lost_record 1 | no (parked) | 0 |
| casket-letters | history | 1 | searched_not_found | yes (grandfathered) | 1 |
| chemtrails | science_nature | 0 (no claims file) | | no | 0 |
| congress-promise-vote | politics | 2 | not_yet_dug 2 | no | 0 |
| dyatlov-pass | history | 0 (no claims file) | | no | 0 |
| eikon-basilike | history | 2 | searched_not_found 2 | yes (grandfathered) | 2 |
| flood-myths-worldwide | religion_myth | 0 (no claims file) | | no | 0 |
| flydubai-fz1073 | current_events | 12 | searched_not_found 12 | yes (live) | 0 (held: live News Review) |
| gulf-of-tonkin | politics | 3 | lost_record 1, searched_not_found 2 | yes (grandfathered) | 3 |
| incandescent-lamp | technology | 9 | searched_not_found 9 | yes (passed with open items) | 9 |
| mcafee-and-surfside | current_events | 1 | searched_not_found | yes (grandfathered) | 1 (needs a close read, 3.3) |
| proto-indo-european | language | 1 | method_limit (structural) | no | 0 |
| teti-pyramid-texts | archaeology_texts | 3 | access 3 | no | 0 |
| votes-2009-present | politics | 0 (no claims file) | | no | 0 |
| votes-johnson-tonkin | politics | 0 (no claims file) | | no | 0 |
| vaccines-autism (branch) | not in `taxonomy.yaml` on this tree | 6 | contested 1, method_limit 1, searched_not_found 4 | no | 0 |

Totals: 35 records on `main` (13 in `current_events`, 9 `technology`, 5 `politics`, 3 each `history` and `archaeology_texts`, 1 each `science_nature` and `language`); 16 gaps are eligible (9 if `grandfathered` digs are excluded, as `CLAUDE.md` reads, 3.5), and **0 tickets are created until a reviewer lists them**. The two `/questions/` pages' 12 G-gaps are in none of these numbers (1.3). The apollo row: its one gap has `anchor.type: documented-absence`, so the derivation returns `lost_record` before the parked-dig test; that is the stated order, and the page would show "lost record" for a parked dig. `searched_not_found` is the honest default and is not a claim that these are access problems.

Migration for each dig: none. No file in any dig changes. **Validator unaffected: no validator change.** `python3 build/conformance.py` before: 15 subjects, 107 nodes, 0 errors, 93 warnings; after (no file in `build/` changes): the same, because the script only reads. The tests in `build/tools/test_gaps.py` cover the new tooling, not the validator. The per-area counts above are for this proposal's reader; `/frontier/` does not show them (3.2).

## 7. Alternatives considered

- **A. Do nothing: keep only the per-claim button.** Rejected: the failure case stands (68 buttons, no overview, duplicates possible, no trail). It is cheap, and still available if the owner prefers.
- **B. Manual issue creation by the owner or agents.** Works at 16 gaps; does not scale and gives no dedupe, so a rerun after a fresh dig duplicates. Rejected as the standing method; usable for the first run if the owner prefers to review each ticket (the dry run supports that).
- **C. One tracking issue per dig.** Fewer tickets (about 6 now) and lower volume, but one issue cannot be closed per gap, cannot be picked up by the dig-agent workflow (one subject, one claim, one step), and a long checklist drifts out of date. Kept as a fallback for volume (O3).
- **D. A GitHub Project board.** Good for ordering and status, already listed in FUTURE.md; but it needs issues to hold, is private to GitHub's UI, and does not render a public page. Compatible with this design as a later view of the same tickets, not a replacement.
- **H. Tickets issued under the owner's own account or a named App.** Covered as option D in 3.4a; not an alternative to tickets but a choice of identity.
- **E. Show the list on the pages but create no tickets.** Meets transparency but not the owner's second half ("open a dig ticket"). It is the safe first step: GT1 to GT3 can ship with no workflow at all. Recommended order if the owner wants to go slowly: pages first, tickets later.
- **G. GitHub-native features instead of, or beyond, plain issues** (sub-issues, Projects, issue types and fields, milestones, Discussions): assessed in 3.7. Used as mirrors or views of the YAML where they help (sub-issues, labels, optionally a project, Discussions for talk); not used as the record, and not adopted where they need an organization or a new token.
- **F. A persistent closed-gap record (a `closes:` log key or a closed-gaps file).** Better than a ticket trail but adds a field and a validator check. Left for a later proposal.

## 8. Neutrality check and risks

**Neutrality.** The list is generated for every dig by the same code. Nothing reads the topic, the direction of the finding or the dig's popularity; the only inputs are the claim's own fields. Test on two digs that point in different directions, using the dry-run output (Appendix A): `gulf-of-tonkin` (politics, `popular_claims: true`, a charged "bait order" question) and `incandescent-lamp` (technology, a priority dispute). `tonkin-bait-order` and `lamp-swan-1850s` both produced a ticket with the same title pattern, the same labels (`gap`, `generated`, `gap:searched_not_found`), the same fields in the same order, and the same sentence that an unsettled question is not evidence either way. Both are "searched, not found", so that test mostly shows the template is uniform (the assessor's point). Charged cases, re-run in this revision: `mcafee-cause-independent-review` (a deceased public figure and what "the widow" asked for) generates the same kind of ticket from the claim's own words, and is **exactly the case the reviewer-list rule is for**: the code cannot tell it needs a close read, a person must. `casket-no-computed-study-found` and `lamp-lodygin-ge-sale` now carry the claim's own account of how little was searched instead of a fixed sentence (Appendix A shows the first). `va-thompson-subgroup-real` (branch) is held as unpublished; a reviewer should not list it without a close read (a named federal scientist's statement, a racial subgroup). What a reviewer checks for each gap: no private or living person identified beyond the published role, no speculation about belief or ethnicity, the ticket reads the same as the page. Tonkin's gap asks whether a document shows an order to provoke; the ticket carries the claim's own "no such document found" statement and does not take a side. The vaccines dig (medicine, charged) produced its records by the same code: 6 records, including one `contested` and one `method_limit` (`va-small-effect-not-excludable`), held because the dig is not published. A structural gap that cuts against a popular claim and one that cuts for it are treated identically: both are limits, shown with their `gap_reason`.

**Where the design could still favour something, and the safeguards.**
- *Ticket spam and volume for the owner.* 16 tickets now (two runs); the creation cap, the one-ticket-per-marker rule and the held rules bound growth. The reviewer-list rule, the cap of 10 creates per run and the cap of 30 open generated tickets bound it. Eligible gaps follow dig size, not significance (lamp is 9 of 16): the list is by author choice of how many gaps to file, and the proposal says so rather than rank. If volume becomes a burden the owner can drop to alternative C per dig (O3).
- *Harassment through public tickets about named people.* A generated ticket repeats published text only and names no private individual by the existing rules, but it moves a claim to a more visible place. Mitigations: the live-event hold (12 flydubai gaps include conspiracy-framed questions such as `fz1073-event-simulated`; the dig names no private person, by its guardrails); only reviewer-listed gaps get a ticket (R5); generated tickets are locked on creation, mandatory, so public comments cannot become a stream about a person and cannot plant instructions for the dig agent (R2); evidence goes through the challenge form. Accounts are identifiable, so the owner can block or report an abusive account; this is not prevention. Residual risk: a claim naming a public figure by their public role is in the ticket as it is on the page.
- *Gaming the list to attract attention.* A gap exists only when a reviewed dig records one with an anchor description; submitting a ticket, a comment or an account cannot create or reorder a gap. Counts and age do not rank anything (GT8) and carry no weight (CHALLENGES C1). Residual risk: a flood of challenges to push a claim into `searched_gap`; that would still need an admitted challenge and a logged revision.
- *A gap that cannot be closed.* Structural gaps get no ticket by default; if the owner marks one, it is closed by the owner or reviewer as "structural: kept as a recorded limit", labelled `gap:method_limit` so it is not counted as overdue work. A gap that cannot be closed because a source is permanently inaccessible stays `searched_gap` with its next step updated (a new claim revision and log entry), and the ticket stays open or is closed with a comment that names that revision; the owner decides which (O2).
- *An unknown is not evidence.* Every ticket and page states it; absence stays capped at provisional (GT2).
- *Prompt injection.* The ticket text comes from our own reviewed claims. The new risk was comments: when a collaborator adds `dig:start` the agent reads the issue and its comments, and on an unlocked ticket any registered account could have commented first. Locking (mandatory, GT4) removes that. Fetched pages remain a risk of the same size as today's "Start this step" (the agent's rules say to treat source text as data); not made worse, not solved.
- *Gap list is not the whole picture.* The `/questions/` pages hold 12 hand-written gaps outside the list (1.3); the section and `/frontier/` say so and link to them.
- *Attention effects.* No per-area counts (GT8); an author's choice of how many gaps to file drives volume, so listing by a reviewer rather than automatically is the bound.

## 9. Owner choices (separate from the proposal's rules)

Each line gives the choice and the **assessor's recommendation, as a recommendation only; nothing is decided**.

- **O1. Enable the creation workflow** (`GAP_TICKETS` = `on`). Recommendation: **not yet.** Ship the page sections first (alternative E); enable only after the lock, concurrency, reviewer-list and wording changes (R2 to R6) are in and a reviewer has read the dry run. Until then the workflow only dry-runs.
- **O2. Labels.** Recommendation: create `gap`, `generated`, `gap-closed` and `gap:<obstacle>` (no `gap:structural`). A gap that stays open because a source is permanently inaccessible: keep it open with an updated next step (a closed ticket hides a live gap).
- **O3. Which gaps get tickets.** Recommendation: published, non-structural, non-live **and reviewer-listed**; leave the 12 flydubai gaps out for now; no tickets for structural gaps (they show on the pages as recorded limits); a tracking issue per dig is the fallback for volume.
- **O4. Who may trigger agents.** Recommendation: unchanged, collaborators with write access (today only the owner). The earlier "triage-level helper" option does not exist on a personal-account repository (GitHub's permission model, from the assessment; unverified here) and is dropped until an organization move.
- **O5. Whether `/frontier/` is public.** Recommendation: public, without per-area or per-obstacle counts, and with the note and links to the `/questions/` pages (R1) so it is not read as the whole picture.
- **O6. Lock generated tickets.** Recommendation and proposal: mandatory, not optional (R2).
- **O7. The registered-account reading** (3.4a). Recommendation: confirm option A for human submissions; for system tickets choose D (a named, owner-registered identity) if "registered" means accountable, otherwise confirm in writing that the workflow bot counts.
- **O8. `grandfathered` digs.** Recommendation: hold tickets for them until `CLAUDE.md` and `docs/PUBLISH_GATE.md` agree (a separate owner-escalated reconciliation, 3.5). They are 7 of the 16 eligible gaps and their reviews are partial with no independent reviewer. Pages may show their gaps now.
- **O9. Discussions.** Recommendation: not yet.
- **O10. Edited generated tickets, parent issues, Project.** Recommendation: flag only, do not overwrite (and the proposal no longer implements overwrite); no parent issues and no Project yet.
- **O11. Create the missing labels now**, independent of this proposal: `dig:start` and `challenge` are verified missing, so the "Start this step" and challenge flows may not trigger; test once with the owner's own submission. Also disable or restrict the repository wiki (enabled, outside the review path).
- **O12. The 12 hand-written G-gaps on `/questions/`.** Options: leave them as they are (v1); file each as a claim so it is in the list; or generate the question pages from the same records. No recommendation beyond: decide before `/frontier/` is described as complete.

## 10. Revision 2: what changed, by assessor requirement

| Requirement | Change | Where |
|---|---|---|
| R1 second gap list, naming collision | 1.3 added; section, page, ticket title and record renamed; O12 | header, 1.3, 3.2, 3.3 |
| R2 lock mandatory, no comment route | lock is hard-fail, audited each run; comment route removed | 3.3, 3.4a, GT4 |
| R3 concurrency, slurp, dedupe by marker | all three in script and workflow | 3.3, 3.6, Appendix B |
| R4 unpublish, missing file, rename, reopen, cap, `not_planned`, 3.7 claims | specified, implemented, tested; restore claim deleted | 3.3, 3.7, Appendix B and C |
| R5 reviewer-listed gaps | `ticketable_gaps` in `review.yaml`; default none; today 0 tickets | 3.3, 3.5, 8 |
| R6 claim's own wording, URL | fixed sentence removed; page URL added | 3.3, Appendix A |
| R7 SCHEMA paragraph is the first definition | stated; rule 3 reconciled; `anchor.type` values defined | 3.1, 3.5 |
| R8 enforcement, area totals | CI step; unenforced rules named; no totals on `/frontier/`; incentive note | 3.2, 3.3, 4 |
| R9 fix 3.7 | triage option dropped, wiki enabled noted, `gap:structural` dropped, label auto-create marked unverified | 3.7, O4, O11 |
| R10 `grandfathered` | needs owner-escalated reconciliation; 16 becomes 9 | 3.5, 6, O8 |
| R11 own branch | stated; file not moved | header |
| R12 Appendix A refreshed, dry run re-run | Appendices A, B, C regenerated from the revised script | Appendices |
| Option D, action-side permission check, `dig-step.yml` noise | added | 3.4, 3.4a |

## Appendix A. Dry-run evidence (revised; scratchpad, not in the repo)

`python3 gap_tickets.py --root /home/user/strata --sample 0` (default: only reviewer-listed gaps; none are listed yet):
```
gap records: 35  |  eligible (published, not structural, not live): 16  |  listed by a reviewer: 0
per subject: records / would create / held
  apollo-landings                1 /   0 /   1
  casket-letters                 1 /   0 /   1
  congress-promise-vote          2 /   0 /   2
  eikon-basilike                 2 /   0 /   2
  flydubai-fz1073               12 /   0 /  12
  gulf-of-tonkin                 3 /   0 /   3
  incandescent-lamp              9 /   0 /   9
  mcafee-and-surfside            1 /   0 /   1
  proto-indo-european            1 /   0 /   1
  teti-pyramid-texts             3 /   0 /   3
by obstacle: {'lost_record': 2, 'searched_not_found': 27, 'not_yet_dug': 2, 'method_limit': 1, 'access': 3}
would create 0, already ticketed 0, would reopen 0, would close 0, flagged 0, held 35
held reasons: {'dig not published': 7, 'not listed by the reviewer (review.yaml ticketable_gaps)': 16, 'live News Review': 12}
```

Same with `--show-eligible` (dry run only; pretends the reviewer listed every eligible gap):
```
gap records: 35  |  eligible (published, not structural, not live): 16  |  listed by a reviewer: 0
per subject: records / would create / held
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
would create 16, already ticketed 0, would reopen 0, would close 0, flagged 0, held 19
held reasons: {'dig not published': 7, 'live News Review': 12}
```

Branch tree (`git archive origin/dig/vaccines-autism build`), `--show-eligible`:
```
gap records: 41  |  eligible (published, not structural, not live): 16  |  listed by a reviewer: 0
would create 16, already ticketed 0, would reopen 0, would close 0, flagged 0, held 25
held reasons: {'dig not published': 13, 'live News Review': 12}
```
Obstacle counts on the branch tree: lost_record 2, searched_not_found 31, not_yet_dug 2, method_limit 2, access 3, contested 1.

Gap claims counted by parsing every claims.yaml (`count.py`): 35 on main plus 6 on the branch, as in section 1.1. `build_site.py` output: 6 excavation(s); "Start this step" per published page: casket 7, eikon 11, flydubai 18, tonkin 17, lamp 9, mcafee 6.

Sample tickets, as the revised script generates them (each is the claim's own wording; `generated` label present; page URL; locked on creation, not shown in the payload). A charged case, a case whose search was shallow, and the two neutrality-test cases:

```
TITLE: Unsettled in dig: mcafee-and-surfside / mcafee-cause-independent-review
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:mcafee-and-surfside:mcafee-cause-independent-review -->
Generated by Stratah from the claim on its dig page. Marker: `gap:mcafee-and-surfside:mcafee-cause-independent-review`. Page: https://stratah.org/digs/surfside-collapse-john-mcafee-death-no-link-nist-failure-began-early-june-2021/#mcafee-cause-independent-review

### Subject

mcafee-and-surfside

### Claim ID

mcafee-cause-independent-review

### The step

Find whether a second autopsy was done or refused (AFP says the widow requested one and further checks); read the court ruling for what it says about requests made; log every hit and miss.

### Notes for the agent (optional)

Statement (as published): No independent examination of the cause of McAfee's death, separate from the Spanish authorities' own autopsy and inquiry, has been found.

What was tried (as published): AFP reports the widow asked for further checks and another autopsy; the court's ruling is quoted as finding nothing in the final autopsy that questioned the original conclusions. No independent review was found in what was read.

Kind of gap (derived): not found in what was read; see 'What was tried' for how far the search went.

Would change if (as published): an independent autopsy report or review is published

An unsettled question is not evidence for or against anything; absence stays capped at provisional. The text above is copied from the published claim; nothing here comes from a submitter. This ticket is locked. To send it to the dig agent, a collaborator adds the label `dig:start`.
```

```
TITLE: Unsettled in dig: casket-letters / casket-no-computed-study-found
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:casket-letters:casket-no-computed-study-found -->
Generated by Stratah from the claim on its dig page. Marker: `gap:casket-letters:casket-no-computed-study-found`. Page: https://stratah.org/digs/casket-letters-mary-queen-of-scots-no-originals-survive-copies-translations/#casket-no-computed-study-found

### Subject

casket-letters

### Claim ID

casket-no-computed-study-found

### The step

Search Google Scholar, Cryptologia and Digital Scholarship in the Humanities; ask the 2023 decipherment team. NARROWED (finding F7): manual comparisons do exist (Bresslau 1882, Sepp); what is unfound is a systematic computed comparison across all surviving French text.

### Notes for the agent (optional)

Statement (as published): No computational style comparison of the casket texts against Mary's authenticated French letters has been published, in two web searches.

What was tried (as published): Two web searches by the open question author found no such study; no wider search yet.

Kind of gap (derived): not found in what was read; see 'What was tried' for how far the search went.

Would change if (as published): a published computed comparison being found

An unsettled question is not evidence for or against anything; absence stays capped at provisional. The text above is copied from the published claim; nothing here comes from a submitter. This ticket is locked. To send it to the dig agent, a collaborator adds the label `dig:start`.
```

```
TITLE: Unsettled in dig: gulf-of-tonkin / tonkin-bait-order
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:gulf-of-tonkin:tonkin-bait-order -->
Generated by Stratah from the claim on its dig page. Marker: `gap:gulf-of-tonkin:tonkin-bait-order`. Page: https://stratah.org/digs/gulf-of-tonkin-incident-no-second-attack-august-4-1964/#tonkin-bait-order

### Subject

gulf-of-tonkin

### Claim ID

tonkin-bait-order

### The step

Read SNIE 50-2-64 and the NSA's remaining declassified Tonkin documents (about 140 released in 2005); search each for provocation or bait language; log every hit and every miss.

### Notes for the agent (optional)

Statement (as published): No document read or reported so far shows an order to provoke the 2 August clash by sending the Maddox in as bait.

What was tried (as published): Text searches of the Hanyok study found no mention of bait; its only uses of "provocation" concern the Aug 4 incident as the pretext for the Resolution and September 1964 patrols. Prados's essay and the tape commentary say the Maddox's mission was to record North Vietnamese radio and radar emissions expected to rise after a 34-A raid (so the patrol was coordinated with the raids), and that the mission commander "had been briefed in Taiwan previously that there would be" no attack and was unaware of the raids. None describes an order to provoke.

Kind of gap (derived): not found in what was read; see 'What was tried' for how far the search went.

Would change if (as published): a document ordering or planning the Maddox patrol as a provocation is found

An unsettled question is not evidence for or against anything; absence stays capped at provisional. The text above is copied from the published claim; nothing here comes from a submitter. This ticket is locked. To send it to the dig agent, a collaborator adds the label `dig:start`.
```

```
TITLE: Unsettled in dig: incandescent-lamp / lamp-swan-1850s
LABELS: ['gap', 'generated', 'gap:searched_not_found']
<!-- gap:incandescent-lamp:lamp-swan-1850s -->
Generated by Stratah from the claim on its dig page. Marker: `gap:incandescent-lamp:lamp-swan-1850s`. Page: https://stratah.org/digs/incandescent-lamp/#lamp-swan-1850s

### Subject

incandescent-lamp

### Claim ID

lamp-swan-1850s

### The step

Search Swan's papers (Tyne and Wear Archives) and the 1929 memoir by his children (not on archive.org) for contemporaneous records.

### Notes for the agent (optional)

Statement (as published): Joseph Swan's experiment with a carbonised-paper arch in a vacuum "about twenty years ago" (that is, about 1860) is known only from his own lecture of 20 October 1880. No record from the 1850s or early 1860s was found.

What was tried (as published): Swan, lecture of 20 Oct 1880, Chemical News 42 (5 Nov 1880), pp. 227-230, read: 'an experiment which I tried about twenty years ago'; the carbon arch 'became red-hot' and bent until it broke. Nothing contemporary found.

Kind of gap (derived): not found in what was read; see 'What was tried' for how far the search went.

Would change if (as published): a dated notebook, letter or society report from 1850-1865 is found

An unsettled question is not evidence for or against anything; absence stays capped at provisional. The text above is copied from the published claim; nothing here comes from a submitter. This ticket is locked. To send it to the dig agent, a collaborator adds the label `dig:start`.
```

## Appendix B. `build/tools/gap_tickets.py` (proposed, NOT applied; written in the scratchpad)

One file here for review; when applied it splits into `gaps.py` (`records`, `obstacle`) and `gap_tickets.py` (`ticket`, `plan`, `main`). The `--create` path (GitHub calls: list, create, lock, close, reopen) was never run. The `plan` logic and the payloads are what the tests exercise.

```python
#!/usr/bin/env python3
"""gap_tickets.py (PROPOSED, not applied). Generates the GAP LIST from claims.yaml and, from it, dig-ticket payloads.

DRY-RUN BY DEFAULT: prints what it would do. It only talks to GitHub with --create, which the workflow passes
only when the owner has set the repository variable GAP_TICKETS=on. Deterministic: same tree, same output.
Usage: gap_tickets.py [--root DIR] [--existing issues.json] [--json] [--show-eligible] [--create --repo OWNER/REPO]
       [--max-create N] [--max-close N] [--max-open N]
"""
import argparse, glob, json, os, re, subprocess, sys, time
import yaml

PUBLISHED_OK = {"passed", "passed_with_open_items", "grandfathered"}   # same set as build_site.py and conformance.py
LOCK_REQUIRED = True   # not an option: see proposal 3.3 (the dig agent reads ticket comments)
OBSTACLE_TEXT = {
    "access": "a source exists but has not been opened",
    "lost_record": "the record is documented as lost or missing",
    "contested": "informed sources disagree and the dispute is recorded",
    "method_limit": "the method cannot settle it (structural; not a failure)",
    "not_yet_dug": "the dig is parked or a draft; the question has not been worked",
    "searched_not_found": "not found in what was read; see 'What was tried' for how far the search went",
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
        rvd = load(os.path.join(os.path.dirname(p), "review.yaml")) or {}
        rv = rvd.get("status")
        listed = set(rvd.get("ticketable_gaps") or [])   # written by the independent reviewer, never the author
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
                "live_event": d.get("event_status") == "live", "listed": cid in listed,
                "url": f"https://{cfg.get('domain', 'stratah.org')}/digs/{d.get('url_slug') or sub}/#{cid}",
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
    body = (f"<!-- {r['marker']} -->\nGenerated by Stratah from the claim on its dig page. Marker: `{r['marker']}`. Page: {r['url']}\n\n"
            f"### Subject\n\n{r['subject']}\n\n### Claim ID\n\n{r['claim_id']}\n\n### The step\n\n{step}\n\n"
            f"### Notes for the agent (optional)\n\n"
            f"Statement (as published): {r['question']}\n\nWhat was tried (as published): {r['tried']}\n\n"
            f"Kind of gap (derived): {OBSTACLE_TEXT[r['obstacle']]}.\n\nWould change if (as published): {r['would_change_if']}\n\n"
            f"An unsettled question is not evidence for or against anything; absence stays capped at provisional. "
            f"The text above is copied from the published claim; nothing here comes from a submitter. "
            f"This ticket is locked. To send it to the dig agent, a collaborator adds the label `dig:start`.\n")
    labels = ["gap", "generated", f"gap:{r['obstacle']}"]
    assert "dig:start" not in labels   # only a collaborator adds dig:start; a generated ticket never starts the agent
    return {"title": f"Unsettled in dig: {r['subject']} / {r['claim_id']}", "labels": labels, "body": body}

def hold_reason(r):
    if not r["published"]: return "dig not published"
    if r["structural"]: return "structural, not marked for a ticket"
    if r["live_event"]: return "live News Review"
    if not r["listed"]: return "not listed by the reviewer (review.yaml ticketable_gaps)"
    return None

def plan(recs, existing, subjects_ok=None, ignore_list=False):
    """existing: [{number,state,body,labels:[names]}]. Returns dict of actions. Never closes on missing evidence."""
    seen = {}
    for i in existing:
        m = re.search(r"<!-- (gap:[^ ]+) -->", i.get("body") or "")
        if m: seen[m.group(1)] = i
    now = {r["marker"]: r for r in recs}
    subjects_ok = subjects_ok if subjects_ok is not None else {r["subject"] for r in recs}
    out = {"create": [], "dup": [], "reopen": [], "close": [], "flag": [], "held": [], "eligible": []}
    for r in recs:
        why = hold_reason(r)
        if why == "not listed by the reviewer (review.yaml ticketable_gaps)":
            out["eligible"].append(r)
            if ignore_list: why = None
        if why: out["held"].append((r, why))
        if why:   # a held gap that already has an open ticket (dig unpublished, live, unlisted): close generically
            t = seen.get(r["marker"])
            if t and t.get("state") == "open": out["close"].append((r["marker"], t, "not_planned", "held"))
            continue
        t = seen.get(r["marker"])
        if not t: out["create"].append(r)
        elif t.get("state") == "open": out["dup"].append(r)
        elif "gap-closed" in (t.get("labels") or []): out["reopen"].append((r["marker"], t))
        else: out["flag"].append((r["marker"], "closed by hand; gap still open; left closed"))
    for m, t in seen.items():
        if t.get("state") != "open" or m in now: continue
        sub = m.split(":")[1]
        if sub not in subjects_ok:      # claims.yaml missing or unreadable: never close on missing evidence
            out["flag"].append((m, "claims.yaml for this subject missing or unreadable; nothing closed")); continue
        out["close"].append((m, t, "not_planned", "claim id gone"))
    return out

def subjects_with_claims(root):
    ok = set()
    for p in glob.glob(os.path.join(root, "build", "subjects", "*", "claims.yaml")):
        try:
            if (load(p) or {}).get("claims"): ok.add(p.split(os.sep)[-2])
        except Exception: pass
    return ok

def gh(args, data=None):
    return subprocess.run(["gh"] + args, input=data, capture_output=True, text=True, check=True).stdout

def list_issues(repo):
    pages = json.loads(gh(["api", "--paginate", "--slurp", f"repos/{repo}/issues?state=all&per_page=100"]))
    out = []
    for pg in pages:
        for i in pg:
            if "pull_request" in i: continue
            out.append({"number": i["number"], "state": i["state"], "body": i.get("body"), "locked": i.get("locked"),
                        "labels": [l["name"] for l in i.get("labels", [])]})
    return out

def lock(repo, n):
    gh(["api", "-X", "PUT", f"repos/{repo}/issues/{n}/lock"])

def close(repo, n, reason, text):
    gh(["api", f"repos/{repo}/issues/{n}/comments", "-f", f"body={text}"])
    gh(["api", "-X", "PATCH", f"repos/{repo}/issues/{n}", "-f", "state=closed", "-f", f"state_reason={reason}"])
    gh(["api", f"repos/{repo}/issues/{n}/labels", "-f", "labels[]=gap-closed"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--existing")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--show-eligible", action="store_true", help="dry run only: pretend the reviewer listed every eligible gap")
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--repo")
    ap.add_argument("--max-create", type=int, default=10)
    ap.add_argument("--max-close", type=int, default=5)
    ap.add_argument("--max-open", type=int, default=30)
    ap.add_argument("--sample", type=int, default=3)
    a = ap.parse_args()
    if a.create and a.show_eligible: sys.exit("--show-eligible is dry run only")
    recs = records(a.root)
    existing = json.load(open(a.existing)) if a.existing else []
    if a.create and not a.existing: existing = list_issues(a.repo)
    P = plan(recs, existing, subjects_with_claims(a.root), ignore_list=a.show_eligible)
    if a.json: print(json.dumps(recs, indent=1)); return
    from collections import Counter
    print(f"gap records: {len(recs)}  |  eligible (published, not structural, not live): {len(P['eligible']) + sum(1 for r in recs if hold_reason(r) is None)}  |  listed by a reviewer: {sum(r['listed'] for r in recs)}")
    print("per subject: records / would create / held")
    for s in sorted({r['subject'] for r in recs}):
        print(f"  {s:28} {sum(r['subject']==s for r in recs):3} / {sum(r['subject']==s for r in P['create']):3} / {sum(h[0]['subject']==s for h in P['held']):3}")
    print("by obstacle:", dict(Counter(r['obstacle'] for r in recs)))
    print(f"would create {len(P['create'])}, already ticketed {len(P['dup'])}, would reopen {len(P['reopen'])}, would close {len(P['close'])}, flagged {len(P['flag'])}, held {len(P['held'])}")
    print("held reasons:", dict(Counter(w for _, w in P['held'])))
    for m, why in P["flag"]: print("FLAG", m, why)
    for r in P["create"][:a.sample]:
        t = ticket(r); print("\n--- sample ticket ---\nTITLE:", t["title"], "\nLABELS:", t["labels"], "\n" + t["body"])
    if not a.create: return
    if len(P["close"]) > a.max_close: sys.exit(f"refusing to close {len(P['close'])} tickets in one run (cap {a.max_close}); a person must look")
    open_now = sum(1 for i in existing if i["state"] == "open" and "generated" in i["labels"])
    for i in existing:                                  # audit: every generated ticket must be locked
        if "generated" in i["labels"] and i["state"] == "open" and not i.get("locked"): lock(a.repo, i["number"])
    for r in P["create"][:min(a.max_create, max(0, a.max_open - open_now))]:
        t = ticket(r)
        made = json.loads(gh(["api", f"repos/{a.repo}/issues", "--input", "-"], json.dumps(t)))
        try: lock(a.repo, made["number"])
        except Exception as e:                          # lock is mandatory: no unlocked generated ticket may stay open
            gh(["api", "-X", "PATCH", f"repos/{a.repo}/issues/{made['number']}", "-f", "state=closed", "-f", "state_reason=not_planned"])
            sys.exit(f"lock failed on #{made['number']}; closed it and stopped: {e}")
        time.sleep(3)
    for m, t in P["reopen"]:
        gh(["api", "-X", "PATCH", f"repos/{a.repo}/issues/{t['number']}", "-f", "state=open"])
        gh(["api", "-X", "DELETE", f"repos/{a.repo}/issues/{t['number']}/labels/gap-closed"])
        gh(["api", f"repos/{a.repo}/issues/{t['number']}/comments", "-f", "body=Reopened: this claim is a searched gap again."])
    for m, t, reason, why in P["close"]:
        sub, cid = m.split(":")[1:3]
        text = ("Closed: this gap is no longer listed (dig not published, not listed, or live)." if why == "held"
                else f"Closed: `{cid}` is no longer in `{sub}` as a searched gap. If the claim still exists its new state is on the dig page.")
        close(a.repo, t["number"], reason, text)
if __name__ == "__main__": main()
```

## Appendix C. `build/tools/test_gaps.py` (proposed, NOT applied) and its output

```python
import json, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gap_tickets as g
ROOT = os.environ.get("GAP_ROOT", ".")

def listed(recs): 
    for r in recs: r["listed"] = True
    return recs

class T(unittest.TestCase):
    def setUp(self):
        self.recs = g.records(ROOT)
        self.ok = g.subjects_with_claims(ROOT)
    def ex(self, recs, state="open", labels=("gap", "generated")):
        return [{"number": i + 1, "state": state, "body": g.ticket(r)["body"], "labels": list(labels)} for i, r in enumerate(recs)]
    def test_deterministic(self):
        self.assertEqual(json.dumps(g.records(ROOT)), json.dumps(self.recs))
    def test_nothing_without_reviewer_list(self):
        self.assertEqual(g.plan(self.recs, [], self.ok)["create"], [])
    def test_idempotent_and_never_dig_start(self):
        recs = listed(self.recs); P = g.plan(recs, [], self.ok); n = len(P["create"]); self.assertGreater(n, 0)
        for r in P["create"]: self.assertNotIn("dig:start", g.ticket(r)["labels"])
        P2 = g.plan(recs, self.ex(P["create"]), self.ok); self.assertEqual((len(P2["create"]), len(P2["dup"])), (0, n))
    def test_unpublish_closes_generically(self):
        recs = listed(self.recs); made = g.plan(recs, [], self.ok)["create"]
        for r in recs:
            if r["subject"] == "gulf-of-tonkin": r["published"] = False
        P = g.plan(recs, self.ex(made), self.ok)
        self.assertEqual(sorted(m.split(":")[1] for m, *_ in P["close"]), ["gulf-of-tonkin"] * 3)
    def test_missing_claims_file_closes_nothing(self):
        recs = listed(self.recs); made = g.plan(recs, [], self.ok)["create"]
        left = [r for r in recs if r["subject"] != "incandescent-lamp"]
        P = g.plan(left, self.ex(made), self.ok - {"incandescent-lamp"})
        self.assertEqual(P["close"], []); self.assertEqual(len(P["flag"]), 9)
    def test_reopen_only_generator_closed(self):
        recs = listed(self.recs); made = g.plan(recs, [], self.ok)["create"]
        P = g.plan(recs, self.ex(made, "closed", ("gap", "generated", "gap-closed")), self.ok); self.assertEqual(len(P["reopen"]), len(made))
        P = g.plan(recs, self.ex(made, "closed"), self.ok); self.assertEqual((len(P["reopen"]), len(P["flag"])), (0, len(made)))
    def test_removed_claim_closes_not_planned(self):
        recs = listed(self.recs); made = g.plan(recs, [], self.ok)["create"]
        P = g.plan([r for r in recs if r["marker"] != made[0]["marker"]], self.ex(made), self.ok); self.assertTrue(all(c[2] == "not_planned" for c in P["close"])); self.assertGreaterEqual(len(P["close"]), 1)
if __name__ == "__main__": unittest.main(verbosity=1)
```

Run as `GAP_ROOT=/home/user/strata python3 test_gaps.py -v`:
```
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
  return yaml.safe_load(open(p, encoding="utf-8")) if os.path.exists(p) else None
ok
test_idempotent_and_never_dig_start (__main__.T.test_idempotent_and_never_dig_start) ... ok
test_missing_claims_file_closes_nothing (__main__.T.test_missing_claims_file_closes_nothing) ... ok
test_nothing_without_reviewer_list (__main__.T.test_nothing_without_reviewer_list) ... ok
test_removed_claim_closes_not_planned (__main__.T.test_removed_claim_closes_not_planned) ... ok
test_reopen_only_generator_closed (__main__.T.test_reopen_only_generator_closed) ... ok
test_unpublish_closes_generically (__main__.T.test_unpublish_closes_generically) ... ok
----------------------------------------------------------------------
Ran 7 tests in 5.256s
OK
```
