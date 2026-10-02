#!/usr/bin/env python3
"""Build build/subjects/teti-pyramid-texts/ from the verbatim import in build/imports/teti-pyramid-texts/.
Originals are untouched. Step 1: mechanical syntax repair (repair_teti.py), copied to utterances/ unchanged in content.
Step 2: a conforming claims.yaml built from the files' own claims. Nothing is added that the files do not say;
sources that the project does not accept as anchors (Wikipedia, tourism sites, AI-written encyclopaedias) are replaced
in the anchor by 'needs primary anchor' and kept under `orientation_only`."""
import os, re, sys, glob, yaml
sys.path.insert(0, os.path.dirname(__file__))
from repair_teti import repair

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMP = os.path.join(ROOT, "build", "imports", "teti-pyramid-texts")
OUT = os.path.join(ROOT, "build", "subjects", "teti-pyramid-texts")
WEAK = re.compile(r"wikipedia|madain|egypt ?fun|memphis ?tours|memphistours|dailynewsegypt|grokipedia|historyskills|pyramidofman|scribd|egyptfuntours", re.I)
N = lambda s: " ".join(str(s).split())

def slug(s): return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

def split_src(s):
    """Return (usable, weak) parts of a source string."""
    if not s: return [], []
    parts = [p.strip() for p in re.split(r";|\bAlso:", N(s)) if p.strip()]
    return [p for p in parts if not WEAK.search(p)], [p for p in parts if WEAK.search(p)]

def claim(cid, state, statement, ec, src, extra=None, positions=None, note=None, req=None):
    usable, weak = split_src(src)
    conf = {"established": "provisional", "refuted": "provisional"}.get(state, "low")
    c = {"id": cid, "state": state, "statement": N(statement),
         "evidence_class": ec, "confidence": conf,
         "evidential_weight": 1, "anchor_checked": "no",
         "adoption_weight": None, "adoption_note": "Not assessed.",
         "would_change_if": "the works named here are read and say something different, or Sethe's edition (the primary text) shows a different reading",
         "anchor": {"type": "needs-primary-anchor",
                    "description": "needs primary anchor. Named in the source file, not read here: " + ("; ".join(usable) if usable else "none usable")}}
    if weak: c["orientation_only"] = weak
    if req: c["anchor"]["required_source"] = N(req)
    if positions: c["positions"] = positions
    if note: c["note"] = N(note)
    if state == "searched_gap":
        c["next_step"] = "Obtain the named source and read it directly: " + (N(req) if req else "Sethe 1908 (page images on the Internet Archive)")
    else:
        c["next_step"] = "Read the named works directly and record each scholar's position in their own words."
    if extra: c.update(extra)
    return c

claims = []
utt_dir = os.path.join(OUT, "utterances"); os.makedirs(utt_dir, exist_ok=True)
hier = mdc = nfiles = 0
for f in sorted(glob.glob(os.path.join(IMP, "batch*", "pt_*.yaml"))):
    text = repair(f, open(f, encoding="utf-8").read())
    open(os.path.join(utt_dir, os.path.basename(f)), "w", encoding="utf-8").write(
        "# Repaired copy of build/imports/teti-pyramid-texts/%s (syntax only; see build/tools/repair_teti.py)\n" % os.path.relpath(f, IMP) + text)
    d = yaml.safe_load(text); nfiles += 1
    pt = slug(d["id"])
    pt_ = d.get("primary_text") or {}
    if (pt_.get("hieroglyphic_unicode") or {}).get("value") == "searched_gap": hier += 1
    if (pt_.get("mdc_transliteration") or {}).get("value") == "searched_gap": mdc += 1
    for dp in d.get("divergence_points") or []:
        st = dp["state"]
        ec = "material" if st == "refuted" else "interpretive"
        src = dp.get("required_source") or dp.get("source") or "; ".join(p["source"] for p in dp.get("positions", []) if isinstance(p, dict) and p.get("source")) or ""
        pos = [{"scholar": N(p.get("scholar")), "reading": N(p.get("reading"))} for p in dp.get("positions", []) if isinstance(p, dict)] or None
        ex = {}
        if st == "refuted":
            ex = {"refutes_target": N(dp["claim"]), "refutation_class": dp.get("refutation_class"), "refutation_basis": N(dp.get("refutation_basis", ""))}
        claims.append(claim(f"{pt}-{slug(dp['id'])}", st, dp["claim"], ec, src, ex, pos, dp.get("note"), dp.get("required_source")))

S = yaml.safe_load(open(os.path.join(IMP, "batch1", "subject.yaml"), encoding="utf-8"))
for sect in ("architectural_program", "teti_innovations"):
    for k, v in S[sect].items():
        ec = {"primary_text + interpretive": "interpretive"}.get(v["evidence_class"], v["evidence_class"])
        claims.append(claim(f"teti-{slug(k)}", v["state"], v["claim"], ec, v.get("source"), note=v.get("caveat")))

teti = S["chronology"]["teti_reign"]
claims.append(claim("teti-reign-conventional-dates", "proposed",
    "Teti reigned about 2345 to 2323 BCE (conventional dates, Shaw 2000), uncertain by about 10 years either way.", "synthetic", teti["source"],
    note="The file calls the 10-year range 'scholarly consensus'. Old Kingdom chronologies differ between authorities by more than that (recalled, not read here), so this stays a convention until the sources are compared."))
claims.append(claim("teti-hieroglyphic-text-not-in-record", "searched_gap",
    f"None of the {nfiles} utterance files contains the hieroglyphic text; all {hier} mark it a gap. {mdc} of {nfiles} also mark the transliteration a gap.",
    "primary_text", "Sethe, K. 1908-1910. Die altaegyptischen Pyramidentexte. Leipzig.",
    req="Sethe 1908, vol. 1 (Internet Archive page images)", extra={"gap_type": None}))
claims[-1].pop("gap_type")

head = {
 "subject": "teti-pyramid-texts",
 "title": "The Pyramid Texts of King Teti (Saqqara, about 2345 to 2323 BCE)",
 "dig_status": "open_corpus",
 "description": N("""A corpus of 19 utterance files (batch 1 and 2) on the texts carved in the burial chambers of King Teti's pyramid. Imported from an earlier chat and
   repaired so it parses. This is a record of what the source files say and where they cite their evidence. No claim here has been checked against Sethe, Allen, Faulkner or
   Mercer, and no hieroglyphic text is held. The utterance data is in utterances/. It is not published."""),
 "divergence_note": N("""The main gap is the text itself: the hieroglyphs are absent from every file. Most readings below are contested or proposed interpretations between named scholars
   (for example Allen 2005 and Faulkner 1969), kept side by side. Many anchors were Wikipedia pages or tourism sites, which are not accepted here; they are listed as orientation only and the
   claim says it needs a primary anchor. Weights sit at the floor because nothing has been read first-hand."""),
 "claims": claims}
class D(yaml.SafeDumper):
    def ignore_aliases(self, data): return True
def rep(dumper, s):
    return dumper.represent_scalar("tag:yaml.org,2002:str", s, style=">" if len(s) > 110 else None)
D.add_representer(str, rep)
with open(os.path.join(OUT, "claims.yaml"), "w", encoding="utf-8") as fh:
    fh.write("# Generated by build/tools/build_teti_subject.py from the import. Edit by adding log entries and re-anchoring claims, not by hand-editing counts.\n")
    yaml.dump(head, fh, Dumper=D, sort_keys=False, allow_unicode=True, width=130)
from collections import Counter
print("files", nfiles, "claims", len(claims), dict(Counter(c["state"] for c in claims)), "hier gaps", hier, "mdc gaps", mdc)
