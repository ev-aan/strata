# Contributing to Stratah

Stratah shows the honestly weighted shape of what is known. It keeps the evidence for a belief separate from the number of people who hold it, and it stays honest about what is not yet known. Anyone can propose a dig, a test or a challenge. Every contribution has to follow the rules below. A change that breaks them is not merged, however good its conclusion looks.

The same rules are on the site at [ev-aan.github.io/stratah/method/](https://ev-aan.github.io/stratah/method/).

---

## 1. The core rules

1. **Show evidential weight and adoption weight separately. Never combine them.**
2. **Adoption is not evidence.** Counting believers never raises evidential weight.
3. **Every claim states what would change its weight.**
4. **Verify against the world, not the store.** A claim that can only be checked against other claims is unverified.
5. **Scrutiny scales with load.** The more depends on a claim, the harder it is checked.
6. **Append, never erase.** Revisions add; earlier reasoning stays visible.
7. **State the weight at all times.** "To the best of our knowledge" is required, not a hedge.
8. **Score contributors against resolved outcomes, never against agreement.**

### Refutation rules

- **Rule 9.** A refutation must name its target and rest on material or primary-text evidence. This applies in both directions. Popular belief cannot pose as evidence, and scholarly consensus cannot pose as a refutation.
- **Rule 12.** `refutation_class` may only be set on a claim whose state is `refuted`. Each class (`narrative_drift`, `misattribution`, `motivated_error`, `institutional_propaganda`, `fabrication`) has its own evidential bar.

---

## 2. Claim states and evidence classes

**States**

| State | Meaning |
|---|---|
| `established` | Anchored to the world and checked: the primary source itself was read (`anchor_checked: primary`). A well-supported claim filed before that check is re-anchored, not downgraded. |
| `proposed` | One author's reading or a new result. Capped at provisional confidence until independently reviewed. |
| `contested` | Live positions with real evidence on more than one side. |
| `refuted` | Fails against material or primary-text evidence (Rule 9). |
| `searched_gap` | We looked and do not know yet. Must name the exact next step. If the gap can never be closed by the method itself (a structural gap), it says so instead: `gap_type: structural` and a `gap_reason`. This is not a failure. |

**Evidence classes**, each with its own decay half-life:

| Class | Example | Half-life |
|---|---|---|
| `material` | An object, a measurement, a dated manuscript | 50 years |
| `primary_text` | The document itself, read directly | 40 years |
| `interpretive` | A scholar's reading of the evidence | 10 years |
| `synthetic` | Reconstructions, statistics, computed results (including ours) | 5 years |

- **Our own computed results are `synthetic`.** A model's or a script's output is never an anchor by itself. Only a match to something independent counts.
- **Fix a lazy citation by re-anchoring it to the primary source**, not by downgrading a claim that is well supported.
- **Use the one anchor format** (SCHEMA N25): a single `anchor:` mapping with `type`, `description`, and `sources` naming ids in the subject's MANIFEST. Not `anchors:` lists, not `ref:`. Every agent submitting work must follow it; conformance rejects anything else.
- **An absence anchor is capped at provisional.** "We found no record of X" is weaker than a positive observation.

---

## 3. Firewalls

- **A true story lends no weight to a neighbouring claim.** A documented forgery in 1586 is not evidence of a forgery in 1567. Mark these links `confers_weight: false`.
- **Reception and transmission go in their own records.** How a claim spread is recorded as transmission, not as support for the claim.
- **Lineages and threads confer no evidential weight** on the claims they connect.

---

## 4. Running a test or an open question

Learned the hard way on open questions Q-001 and Q-002 (formerly bounties B-001 and B-002). Every step is required.

**Before any data is collected**

1. **Check feasibility first.** Is there an oracle, something independent that could confirm an answer? Are the sources open? Is there enough text or data for the method? Log what you find, including dead ends.
2. **Write the test down first.** Record the question, the method, the corpora, the controls and what each possible result would and would not show. Do this in the log, before you run anything.
3. **Set decision thresholds from calibration, not by guessing.** In Q-001 a guessed bar of 3× could never be met even by Mary's own letters. Run the method on texts of known authorship first, then set the bar from that.

**Controls (no result counts without them)**

4. **Positive control.** The method must find a known answer it was not pointed at, for example the Pamela prayer in Sidney's *Arcadia* (Q-002).
5. **Held-out calibration.** Test the method on known material it was not built from. Leave out the whole source work, not just the passage.
6. **Genre control.** Check whether the method is detecting the author or just the type of writing. In Q-002, the Queen's letters scored as "Charles" until this was fixed.
7. **Attractor control.** Check whether a large or varied comparison corpus pulls in everything. In Q-002, 17 of 31 passages by unrelated clergy came out nearest Gauden.
8. **Report distances and ranges, not "nearest wins".** Ask whether the questioned text sits inside the candidate's own range, compared with other writers' ranges.

**Sources**

9. **Prefer clean transcriptions to scanned OCR.** If you must mix the two, say so, and normalise spelling the same way for every corpus.
10. **Use only text the candidate really wrote.** Drop ministerial drafts, editors' notes, translations and disputed attributions. List what was dropped and why.

**After the run**

11. **Publish everything:** code, corpus lists with source identifiers, fixed random seeds, raw outputs. Another person must be able to rerun it and get the same numbers.
12. **Keep failed and superseded runs on the page.** A first result that did not survive the controls stays in the log, marked as such. This is what makes the surviving result believable.
13. **Say what the result does not show,** in plain words, next to what it does.
14. **Get outside review before a claim leaves `proposed`.** A named specialist outside Stratah reviews it. Agreement with a famous scholar is not confirmation.
15. **Write plain-and-true surface lines.** No hype. "Compelling" is one bad word from clickbait.

---

## 5. Page and record conventions

Every excavation or open question page carries:

- **IDs that are never reused or renumbered:**
  - claims (C-01…)
  - findings (F1…)
  - gaps (G-01…)
  - tests (DT-…)
- **Claims with:**
  - their state
  - evidential weight and adoption weight, shown separately
  - their evidence class
  - whether the anchor was checked
  - what would change their weight
- **A divergence note:** the gap between evidence and adoption. That gap is the product.
- **An append-only excavation log** with dates. Corrections are new entries.
- **A sources list** that labels each source's evidence class.
- **Run files** next to the page, with a README giving the run order.

---

## 6. How to contribute

1. **Fork the repository** and make your changes on a branch. Nothing is pushed to `main` directly.
2. **Open a pull request** and fill in the checklist. CI runs the validator, then an independent review
   agent checks the judgment rules (anchors actually say what claims say, honest weights, no borrowed
   weight, plain surface lines) and merges only if it approves. Changes to the rules themselves are
   escalated to the owner. The full process is in [`docs/REVIEW.md`](docs/REVIEW.md).
3. **To challenge a finding or add evidence,** press "Challenge or add evidence" on the claim, or open an issue with the "Challenge a finding or submit evidence" form. A challenge must name one claim and give a source we can check; counts, reactions and repeats carry no weight. Admitted challenges are logged in the excavation's challenges ledger whichever way they come out, and declined ones are listed with the reason. The rules are in [`docs/CHALLENGES.md`](docs/CHALLENGES.md).
4. **To propose a new open question,** open an issue. Name:
   - the question
   - the oracle
   - whether the sources are open
   - the conspiracy or popular claim it touches, if any.

The public marks dig sites; contributors do the excavation.

## Licences

- Code: MIT (`LICENSE`).
- Written content: CC BY 4.0 (`LICENSE-CONTENT.md`).
- Historical sources: public domain.

## Challenges and submitted evidence

A challenge is a submission of evidence that must pass an admission test; counts, reactions and repeats carry no weight. See docs/CHALLENGES.md. Use the "Challenge or add evidence" button on a claim, which opens the structured issue form.
