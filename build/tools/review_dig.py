#!/usr/bin/env python3
"""Mechanical review of one excavation before it can go live (docs/PUBLISH_GATE.md).
Usage: python3 build/tools/review_dig.py <subject> [--write]
Prints the checks. With --write it writes build/subjects/<subject>/review.yaml with status `pending` (a person or reviewing agent then verifies the
unverifiable items by hand and sets the status). A mechanical pass is necessary, not sufficient: quotes are only checked against sources stored in the
subject's own folder; everything else is listed as `needs_manual_check`."""
import os, re, sys, glob, subprocess, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(__file__))
N = lambda s: re.sub(r"\s+", " ", str(s or "")).strip()
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower())).strip()

import difflib
_CT = {}
def fuzzy(seg, corpus):
    """Best similarity (0-1) of a quoted segment to the stored source text, tolerant of OCR noise and line breaks."""
    if id(corpus) not in _CT:
        toks = corpus.split()
        idx = {}
        for i, w in enumerate(toks):
            idx.setdefault(w, []).append(i)
        _CT[id(corpus)] = (toks, idx)
    toks, idx = _CT[id(corpus)]
    q = norm(seg).split()
    if not q:
        return 0.0
    key = max(q, key=len)
    best = 0.0
    qs = " ".join(q)
    for pos in idx.get(key, [])[:60]:
        off = q.index(key)
        lo = max(0, pos - off - 3)
        win = " ".join(toks[lo: lo + len(q) + 6])
        best = max(best, difflib.SequenceMatcher(None, qs, win[: len(qs) + 20]).ratio() if win else 0)
        if best > 0.97:
            break
    return best


def main():
    sub = sys.argv[1]
    base = os.path.join(ROOT, "build", "subjects", sub)
    res = {"subject": sub, "status": "pending", "checks": [], "open_items": [], "needs_manual_check": []}
    def add(name, ok, detail=""):
        res["checks"].append({"check": name, "result": "pass" if ok else "FAIL", "detail": detail})
        if not ok: res["open_items"].append(f"{name}: {detail}")
    cp = os.path.join(base, "claims.yaml")
    if not os.path.exists(cp):
        add("claims.yaml exists", False, "no claims.yaml: nothing to publish"); out(res, sub); return
    C = yaml.safe_load(open(cp, encoding="utf-8")); claims = C.get("claims", [])
    byid = {c["id"]: c for c in claims}
    conf = subprocess.run([sys.executable, os.path.join(ROOT, "build", "conformance.py")], cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    mine = [l for l in conf if re.search(rf"\b{re.escape(sub)}\b", l)]
    errs = [l for l in mine if l.startswith("ERROR")]
    add("conformance: no errors for this subject", not errs, "; ".join(errs[:3]))
    warns = [l for l in mine if l.startswith("WARNING")]
    res["conformance_warnings"] = len(warns)
    # headline rules
    h = C.get("headline", ""); hc = byid.get(C.get("headline_claim"))
    add("headline present, 70-95 characters", bool(h) and 70 <= len(h) <= 95, f"{len(h)} characters")
    if hc:
        ok = hc["state"] in ("established", "refuted") and hc.get("confidence") == "high" and str(hc.get("anchor_checked")) == "primary"
        add("headline claim is established/refuted at high confidence with a primary check, or status is draft", ok or C.get("headline_status") == "draft",
            f"{hc['id']}: {hc['state']}, {hc.get('confidence')}, anchor_checked {hc.get('anchor_checked')}; headline_status {C.get('headline_status')}")
    else:
        add("headline_claim names a claim", False, str(C.get("headline_claim")))
    add("headline_status is draft or review before the gate passes", C.get("headline_status") in ("draft", "review", "published"), str(C.get("headline_status")))
    # assessment
    a = C.get("assessment") or {}
    add("assessment present with question, answer, headline, text, basis, would_settle", all(a.get(k) for k in ("question", "answer", "headline", "text", "basis", "would_settle")))
    add("assessment has exactly three key_points", len(a.get("key_points") or []) == 3, str(len(a.get("key_points") or [])))
    add("assessment states no percentage", "%" not in N(a) and "percent" not in N(a).lower())
    tx = yaml.safe_load(open(os.path.join(ROOT, "build", "taxonomy.yaml")))
    add("taxonomy entry (area and question types)", sub in tx.get("assignments", {}))
    # claims
    weak = [c["id"] for c in claims if c["state"] in ("established", "refuted") and str(c.get("anchor_checked")) != "primary"]
    res["established_or_refuted_without_primary_check"] = weak
    if weak: res["needs_manual_check"].append(f"{len(weak)} established/refuted claims anchored below primary: " + ", ".join(weak))
    nokind = [c["id"] for c in claims if not c.get("statement_kind")]
    add("every claim has statement_kind", not nokind, ", ".join(nokind[:5]))
    nogap = [c["id"] for c in claims if c["state"] == "searched_gap" and not (c.get("next_step") or c.get("gap_type"))]
    add("every searched gap names its next step", not nogap, ", ".join(nogap))
    # quotes against stored sources
    corpus = ""
    for f in glob.glob(os.path.join(base, "sources", "**", "*"), recursive=True):
        if f.endswith((".txt", ".md", ".yaml")) and os.path.isfile(f):
            corpus += " " + norm(open(f, encoding="utf-8", errors="ignore").read())
    found = missing = unchecked = 0; miss = []
    for c in claims:
        for field in (c.get("statement"), (c.get("anchor") or {}).get("description") if isinstance(c.get("anchor"), dict) else ""):
            txt = N(field)
            if txt.count('"') % 2:                      # unbalanced quote marks: pairing would be wrong, leave it to the manual check
                continue
            for q in re.findall(r'"([^"]{30,400})"', txt):
                if q.startswith(" ") or q.endswith(" "):
                    continue
                segs = [s for s in re.split(r"\.\.\.|\u2026|\[[^\]]*\]", q) if len(norm(s)) >= 20]
                if not segs:
                    continue
                if not corpus:
                    unchecked += 1
                else:
                    sc = min(fuzzy(s, corpus) for s in segs)
                    if sc >= 0.85:
                        found += 1
                    else:
                        missing += 1; miss.append(f"{c['id']} (match {sc:.2f}): \"{q[:70]}...\"")
    res["quotes"] = {"found_in_stored_sources": found, "not_found_in_stored_sources": missing, "no_stored_source_to_check_against": unchecked}
    if miss: res["needs_manual_check"] += ["quote not matched in stored sources (OCR noise possible): " + m for m in miss[:15]]
    if unchecked: res["needs_manual_check"].append(f"{unchecked} quotations have no stored source text here: open the cited source and check each one")
    # sources
    mp = os.path.join(base, "sources", "MANIFEST.yaml")
    add("sources manifest exists", os.path.exists(mp))
    if os.path.exists(mp):
        M = yaml.safe_load(open(mp, encoding="utf-8")); S = M.get("sources", [])
        noauth = [s.get("id") for s in S if not s.get("authenticity")]
        add("every source has an authenticity block", not noauth, ", ".join(map(str, noauth[:5])))
    add("log has entries", os.path.exists(os.path.join(base, "log.yaml")))
    add("timeline present (dates exist, so a timeline is required)", os.path.exists(os.path.join(base, "timeline.yaml")))
    res["needs_manual_check"] += ["dates, names, patent or document numbers: verify each against the source",
                                  "every refuted claim names its target and rests on material or primary-text evidence (Rule 9)",
                                  "no claim goes beyond what was read; anything not read is marked not read"]
    out(res, sub)

def out(res, sub):
    for c in res["checks"]: print(f"{c['result']:5} {c['check']}" + (f"  [{c['detail']}]" if c["detail"] and c["result"] != "pass" else ""))
    print("quotes:", res.get("quotes")); print("conformance warnings for this subject:", res.get("conformance_warnings"))
    print("needs manual check:"); [print("  -", x[:200]) for x in res["needs_manual_check"]]
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "build", "subjects", sub, "review.yaml")
        if os.path.exists(p): print("review.yaml exists; not overwritten"); return
        res["reviewed_by"] = ""; res["reviewed_on"] = ""; res["notes"] = ""
        with open(p, "w", encoding="utf-8") as f:
            f.write("# Publish-gate review record (docs/PUBLISH_GATE.md). status: pending | revisions_requested | passed | passed_with_open_items | grandfathered | failed (rounds: see docs/PUBLISH_GATE.md)\n")
            yaml.safe_dump(res, f, sort_keys=False, allow_unicode=True, width=120)
        print("wrote", p)

if __name__ == "__main__":
    main()
