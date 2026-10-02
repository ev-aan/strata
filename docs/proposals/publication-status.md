# Proposal: record whether a source is retracted, corrected or unpublished (PS1 to PS4)

Status: DRAFT proposal under `docs/SCHEMA_PROPOSALS.md`. Not in force. Needs an independent assessment, then the owner's decision.
Written by the author of the vaccines-autism dig, who first made this change directly in PR #6 without a proposal. That was against `CLAUDE.md` and `docs/SCHEMA_PROPOSALS.md`; this proposal puts it on the proper path, and PR #6 is held as a draft until it is decided.

## 1. The failure case
`build/subjects/vaccines-autism` (PR #7) cites two retracted papers as the origin of claims it examines:
- **Wakefield et al., Lancet 1998** (`src-wakefield-1998`, retracted 2010), behind `va-mmr-causes-autism` and `va-timing-shows-cause`.
- **Hooker, Transl Neurodegener 2014** (`src-hooker-2014`, retracted 2014), behind `va-thompson-subgroup-real`.

It also cites:
- **an unpublished draft:** `src-henry-ford-draft`;
- **papers with published corrections:** `src-verstraeten-2003`, `src-jain-2015`, `src-andersson-2025`.

Under the current schema the only place a retraction can be recorded is free text in a source title or a basis line. Nothing requires it to be stated, nothing shows it beside the claim that cites the paper, and the validator cannot tell a retracted source from a sound one. The owner's concern, raised while the dig was being built, is that a reader "will assume it is a legitimate study". A retracted paper appearing as an anchor with no visible status is a misleading result under the current rules.

## 2. The evidence
- **Repository search on 2026-10-02.** No field in `build/SCHEMA.md` records publication status. No rule in `build/conformance.py` checks for one. `grep -il retract` over all subjects' manifests and claims finds no structured record; the only other hit is a free-text note in `incandescent-lamp` about an author who has not retracted a book.
- **Notices read.** The notices were confirmed for each source:
  - the Lancet retraction record, PMID 20137807;
  - the Hooker retraction note, PMC4183946, read in full;
  - the errata for Verstraeten (Pediatrics 2004;113:184), Jain (JAMA 2016;315:204) and Andersson (Ann Intern Med 2025;178:1527), in Europe PMC.
- **Validator runs** with the rules below added to the current `main`:
  - current `main`: 15 subjects, 0 errors;
  - `main` plus the rules: 15 subjects, 0 errors (no subject on `main` uses the field);
  - `main` plus the rules plus PR #7: 16 subjects, 0 errors;
  - removing one `flagged_sources` entry from PR #7 gives `PS3: cites src-hooker-2014, which is retracted ...` (error).

## 3. The proposed change
**Text for `build/SCHEMA.md`** (as on branch `schema/publication-status`, PR #6):

```yaml
# on a source in sources/MANIFEST.yaml; optional unless the work is flagged
publication:
  status: published | unpublished | corrected | expression_of_concern | withdrawn | retracted
  date: 2010-02-02          # required for expression_of_concern, withdrawn, retracted
  notice: <url or citation> # required for the same three
  reason: >                 # the notice's own stated reason; "as quoted" if the notice was not read
```

**In `claims.yaml`:**
- a top-level `source_notices: [{source, notice}]` with a plain sentence for every retracted or withdrawn source, shown first on the page;
- `flagged_sources: [ids]` on any claim whose `anchor.sources` includes a flagged source, shown beside the citation.

**Validator** (`build/conformance.py`, as on PR #6):
- **PS1** `publication.status` is one of the six values (error).
- **PS2** `expression_of_concern`, `withdrawn` and `retracted` need `date` and `notice` (error).
- **PS3** a claim citing a retracted or withdrawn source in `anchor.sources` must list it in `flagged_sources` (error); for an expression of concern, a warning.
- **PS4** every retracted or withdrawn source has an entry in `source_notices` (error).

**Site** (`build/tools/build_site.py`): render `source_notices` as a banner above the assessment, and a label beside any flagged citation. This is not yet written; it would follow the decision.

## 4. What it does not change
- No claim state, weight or confidence changes.
- A retraction is recorded about the source and is never used as a refutation by itself. Rule 9 still needs a refutation to rest on material or primary-text evidence.
- No existing finding is altered. The field is optional, so subjects without it are untouched.
- It does not judge whether a retraction was right. A disputed retraction can say so in `reason`.

## 5. Impact

| subject | before | after | migration |
|---|---|---|---|
| 15 subjects on `main` | 0 errors | 0 errors | none |
| vaccines-autism (PR #7) | 0 errors | 0 errors | already carries the fields |

Future digs that cite a retracted or withdrawn work must add one notice and one flag per citing claim.

## 6. Alternatives considered
- **Do nothing.** Rejected: the failure case stands, and a retracted anchor reads as sound.
- **Free text in the title only.** Rejected: invisible beside the claim, and not checkable.
- **A new claim state "retracted".** Rejected: states describe how a claim stands against evidence, not the status of a source. One source can serve several claims, and a retracted paper can be the subject of a claim that is itself established ("the paper was retracted in 2010").
- **Down-weight claims that cite retracted sources automatically.** Rejected: it would turn a publishing event into evidential weight (rule 2) and would wrongly lower claims that are about the retraction.

## 7. Neutrality check
- **The rule ignores direction.** It looks only at a source's publication status, never at which way the citing claim points.
- **Vaccines-autism, both sides.** The two retracted sources sit on the side that claims a link. The three corrected sources (Verstraeten, Jain, Andersson) sit on the side that finds none, and are recorded the same way.
- **Gulf of Tonkin** (a dig pointing toward a documented official failure): no source there is flagged, and the result is unchanged (0 errors).
- **Synthetic test.** A retracted source cited by a claim that agrees with the scientific mainstream fires PS3 and PS4 exactly as it does for the opposing side (unit test in PR #6: a retracted `s1` cited by `c1` gives both errors).

## Decision requested
Adopt PS1 to PS4 as written; adopt with changes; or decline. If adopted, PR #6 is updated to match and becomes the change commit. If declined, PR #6 is closed, and PR #7 drops `source_notices`, `flagged_sources` and `publication`, keeping the retraction notes in its text.
