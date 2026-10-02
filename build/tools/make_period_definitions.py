#!/usr/bin/env python3
"""One-off: write authority-scoped period definitions (schema v0.6, N17) for the Egyptian Old Kingdom from the PeriodO dataset.
Fetches https://data.perio.do/d.json (a public dataset, about 8 MB). Each definition is kept as its authority printed it. We read PeriodO's
record of each authority, not the authority's own page, and say so. Values: `quoted` is the printed text; from_bce/to_bce are our reading of it."""
import os, json, urllib.request, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "build", "definitions")
PICK = [("p0qk76z", "p0qk76z92f9", "uee-ucla"), ("p0bd664", "p0bd66487b6", "freeman-2004"), ("p0m63nj", "p0m63njqgqx", "levantine-ceramics-project"),
        ("p0cp447", "p0cp447cfpq", "robins-2000"), ("p083p5r", "p083p5r9q68", "gates-2003"), ("p0m64td", "p0m64tdjsnt", "eamena")]
NOTES = {  # discrepancies noticed in what PeriodO prints; kept visible, nothing silently corrected
    "levantine-ceramics-project": "The printed labels are '-2663' and '-2181' and the structured years are the same numbers. Under the ISO convention used for the structured years -2663 is 2664 BCE; read here as 2663 and 2181 BCE as printed, which may be off by one year.",
    "eamena": "The start is printed '-2700' (read as 2700 BCE as printed; under the ISO convention it would be 2701 BCE). The stop is printed '2150' with the structured year +2150 (a year CE). Read here as 2150 BCE, which is almost certainly what was meant; this is our reading, not what is printed.",
}
def main():
    d = json.load(urllib.request.urlopen("https://data.perio.do/d.json", timeout=120))
    os.makedirs(OUT, exist_ok=True)
    for aid, pid, slug in PICK:
        a = d["authorities"][aid]; p = a["periods"][pid]; s = a["source"]
        sl, sp = p["start"]["label"], p["stop"]["label"]
        sy, ey = int(p["start"]["in"]["year"]), int(p["stop"]["in"]["year"])
        frm = -sy + 1 if sy < 0 else None
        to = -ey + 1 if ey < 0 else abs(ey)             # EAMENA prints +2150 for 2150 BCE
        if slug == "levantine-ceramics-project": frm, to = 2663, 2181
        if slug == "eamena": frm = 2700
        authority = {"title": s.get("title"), "creators": [c["name"] for c in s.get("creators", [])], "year_published": s.get("yearPublished")}
        for k in ("url", "id", "citation"):
            if s.get(k): authority[k if k != "id" else "worldcat"] = s[k]
        if isinstance(p.get("source"), dict) and p["source"].get("locator"): authority["locator"] = p["source"]["locator"]
        n = {"id": f"old-kingdom--{slug}", "label": p["label"], "region": "Egypt", "authority": authority,
             "quoted": {"start": sl, "stop": sp}, "from_bce": frm, "to_bce": to,
             "via": {"dataset": "PeriodO", "period_ark": f"http://n2t.net/ark:/99152/{pid}", "authority_ark": f"http://n2t.net/ark:/99152/{aid}", "dataset_url": "https://data.perio.do/d.json", "retrieved": "2026-10-02"},
             "authority_read_directly": False}
        if p.get("editorialNote"): n["editorial_note_in_periodo"] = p["editorialNote"]
        if slug in NOTES: n["note"] = NOTES[slug]
        with open(os.path.join(OUT, n["id"] + ".yaml"), "w", encoding="utf-8") as f:
            f.write("# Authority-scoped period definition (schema v0.6, N17). Kept as the authority printed it; never edited, only superseded by a new file.\n")
            yaml.safe_dump(n, f, sort_keys=False, allow_unicode=True, width=120)
        print(n["id"], frm, to)
if __name__ == "__main__":
    main()
