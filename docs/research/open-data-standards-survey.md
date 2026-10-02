# Survey: structures in other open-data and evidence standards (2026-10-02)

Method: three readers fetched the primary documentation of 19 standards and projects; I then re-checked a sample against the original pages. This is a list of ideas, not decisions. Each item says how well it was checked.

## Checked by me against the original page
- CIDOC CRM v7.1.3 has P79, P80, P81 ("ongoing throughout") and P82 ("at some time within"); it does NOT contain P81a/b or P82a/b (a reader caught my memory of an older version being wrong).
- EDTF (loc.gov/standards/datetime): `?` uncertain, `~` approximate, `%` both; open intervals `1985-04-12/..`; sets `[1667,1668,1670..1672]`.
- Wikidata property names: P1310 "statement disputed by", P7452 "reason for preferred rank", P2241 "reason for deprecated rank", P1480 "sourcing circumstances", P1319 "earliest date" (and P1326 latest).
- ICD 203: "must not combine" a confidence level with a degree of likelihood; assumptions stated when they are the "linchpin of an argument". (Its likelihood bands, "almost no chance 01-05%" and so on, were reported by a reader; I did not find them in the PDF's text layer.)
- Frictionless Data: a resource `hash` is MD5 unless prefixed, for example `sha1:...`; so ours would be `sha256:...`.

## Read by the readers only (not re-checked)
ACLED codebook (time_precision and geo_precision 1-3; conservative fatalities rule and published imputation conventions); UCDP GED v25.1 (where_prec 1-7, date_prec 1-5 with date_start and date_end, event_clarity, low/best/high estimates); Wikidata ranks and qualifiers; Nanopublications (assertion, provenance, publication info); W3C Web Annotation selectors; PROV-O; PeriodO (authority-scoped period definitions with quoted and structured bounds); Pleiades (association certainty, attestation confidence, location accuracy); CiTO verbs; GRADE (certainty levels, five downgrading and three upgrading domains); Berkeley Protocol (six stages; source / item / content verification; chain of custody; capture fields); IFLA LRM (Work, Expression, Manifestation, Item); Frictionless Data Package and Table Schema; Datasheets for Datasets (seven sections); Crossref update types (12 listed); DataCite relation types.
Not read at all: the Admiralty/NATO A-F and 1-6 grading (FM 2-22.3 / STANAG 2511: every mirror failed; the description is from memory), the COPE retraction guidelines (403), Zenodo's concept-versus-version DOI behaviour, nanopublication signing.

## What we may be missing, ranked
Tier 1: small changes that fix real weaknesses we have already hit.
1. **A time window, not just a precision label.** Earliest and latest possible, an optional "certainly covers" core, and a note per boundary saying why (CIDOC P82/P81/P79/P80, UCDP date_start/date_end, Wikidata earliest/latest). Stored in EDTF so open ends, approximations and BCE years have one syntax. Our date_basis stays: EDTF says how fuzzy, not why. Fixes: Teti's dates (authorities differ), the Westminster 7 versus 9 December.
2. **Authority-scoped definitions** (PeriodO): "Old Kingdom" is a definition by a named authority with quoted text and structured bounds, so two scholars' versions coexist.
3. **Evidence, assumption, judgment** (ICD 203): mark each statement's kind, list the assumptions that carry an argument with "if wrong, then...", list alternatives, and keep likelihood (how probable) apart from confidence (how sure we are of the basis). Fixes mixing what a source says with our inference.
4. **Recorded reasons behind confidence** (GRADE): per claim, a short list of downgrades and upgrades by named domain (risk of bias, inconsistency, indirectness, imprecision, publication bias) with a written reason each. A checklist with reasons, not arithmetic.
5. **Attributable disputes and typed links** (Wikidata P1310, P2241, P7452; CiTO): `contested` names who disputes it; every change of state has a reason; links carry a typed verb (supports, disputes, corrects, qualifies, extends, confirms, refutes) beside established/possible; `refuted` stays visible but is left out of default views.
6. **A self-describing private release**: a `datapackage.json` (version = build id, `sha256:` hashes, sources, licences, enum constraints) and a datasheet README (coverage, what was left out, observed versus inferred, errata, maintenance).
7. **Typed corrections** (Crossref): clarification, correction, expression of concern, partial retraction, retraction, new version, each pointing at what it affects, with a published definition of each. A small subset of Crossref's twelve.

Tier 2: valuable where the case arises.
8. Work, Expression, Manifestation, Item (LRM) for disputed transmission, so independence counts Expressions, not copies (the Casket Letters).
9. Source reliability separate from item credibility (Admiralty grading; from memory) on each source edge.
10. A capture record for web and digital sources (Berkeley Protocol): captured_at, captured_by, tool, hash, archived copy, and a source / file / content verification record; required for digital sources only.
11. Anchors that survive change (Web Annotation): quote with prefix and suffix, or an image region, plus the version of the source it was made against.
12. Quantities as low, best, high with a published rule for vague amounts and a `derivation` string (UCDP, ACLED).
13. A numeric location accuracy with its method, an "at sea" and "linear feature" place type, and Pleiades' split of "is this the same place" certainty from "is the evidence good" confidence.
14. A typed `via` on derives_from (transcribed, translated, excerpted, forged) (PROV).
15. Content-hash identifiers for revisions and a stable "latest" id beside each immutable build id (nanopublications, DataCite).

## Cautions the standards themselves teach
- False precision: GRADE arithmetic, ICD percentage bands, EDTF's uncalibrated `?` and `~`, UCDP's best = sum of parts, ACLED's midpoint dates. Keep the words and the reasons; do not compute numbers a historian cannot defend.
- Rank and agreement are not evidence (Wikidata says so; Pleiades certainty is defined by commentators' agreement). Our independence count is a better base.
- Over-modelling (PROV, LRM, RDF with signing). Take the idea, not the stack.
- Born-digital rules (Berkeley) turn into padding on a 17th-century document; require them only where they apply.
- Reliability labels become halos: a reliable chronicler can still be wrong on one item.
