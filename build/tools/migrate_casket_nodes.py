#!/usr/bin/env python3
"""One-off pilot, run once from the commit before the migration: move the Casket Letters timeline into shared nodes with places and objects.
Places are given only where Henderson (1889) names the place; coordinates come from OpenStreetMap Nominatim (a gazetteer, orientation only)
at the precision stated. Events with no place named in the text read have none. Merges: the same event shown in two panels."""
import os, re, sys, subprocess, yaml
sys.path.insert(0, os.path.dirname(__file__))
from nodes import NODES_DIR, ROOT
from migrate_tonkin_nodes import slug, strip_date, src_list, dump, node, TODAY

SUB = "build/subjects/casket-letters/timeline.yaml"
NOM = "OpenStreetMap Nominatim lookup, retrieved 2026-10-02 (a gazetteer, orientation only; not a source for the event)"

PLACES = {
    "edinburgh": {"name": "Edinburgh (Kirk o' Field, Old Town)", "lat": 55.9496, "lon": -3.1915, "precision": "city", "source": NOM + "; OSM relation 8341994",
                  "note": "City-level point for the Old Town. Henderson places Kirk-o'-Field in Edinburgh; the exact site is not marked here."},
    "carberry": {"name": "Carberry Hill, East Lothian", "lat": 55.9160, "lon": -3.0206, "precision": "region", "uncertainty_km": 2,
                 "source": NOM + "; the point is Carberry Tower (OSM way 170342435), used as a nearby proxy because Carberry Hill itself was not found",
                 "note": "Approximate: within about 2 km."},
    "york": {"name": "York", "lat": 53.9591, "lon": -1.0815, "precision": "city", "source": NOM + "; OSM node 20913294"},
    "westminster": {"name": "Westminster, London", "lat": 51.4994, "lon": -0.1245, "precision": "site", "source": NOM + "; OSM relation 1567699 (Palace of Westminster)",
                    "note": "Henderson says only 'Westminster'; the building is not stated, so this is the area."},
    "hatfield": {"name": "Hatfield House, Hertfordshire", "lat": 51.7605, "lon": -0.2088, "precision": "site", "source": NOM + "; OSM way 24232910"},
    "london": {"name": "London (the Record Office)", "lat": 51.5074, "lon": -0.1278, "precision": "city", "source": NOM + "; OSM relation 175342",
               "note": "Henderson says 'the Record Office' without an address; the point is the city only."},
}
# event id -> place key (only where Henderson's text read names the place)
PLACE_OF = {"k1": "edinburgh", "b1": "edinburgh", "k4": "carberry", "b3": "carberry", "k8": "york", "b8": "york", "k9": "westminster", "b9": "westminster"}
MERGE = {"b1": "k1", "b2": "k3", "b3": "k4", "b4": "k5", "b7": "k7", "b8": "k8"}   # same event shown in two panels. k9 and b9 are NOT merged: their dates differ.
ABOUT_CASKET = {"k5", "k6", "k7", "k9", "k11", "k12", "b5", "b6", "b9"}


def main():
    G = yaml.safe_load(subprocess.run(["git", "show", "HEAD:" + SUB], cwd=ROOT, capture_output=True, text=True).stdout)
    text = subprocess.run(["git", "show", "HEAD:" + SUB], cwd=ROOT, capture_output=True, text=True).stdout
    ids, made = {}, {}
    OBJ = "object-casket-and-letters-1567"
    for e in G["events"]:
        if e["id"] in MERGE:
            continue
        ids[e["id"]] = f"casket-{str(e['time'])[:10]}-{slug(strip_date(e['label']), 6)}"
    ids["k9"] = "casket-1568-12-westminster-conference-examines-the-letters"
    ids["b9"] = "casket-1568-12-westminster-examination-collation-minute"
    ids["k6"] = "casket-1567-12-letters-probably-shown-to-the-nobles-and-parliament"
    for e in G["events"]:
        if e["id"] in MERGE:
            ids[e["id"]] = ids[MERGE[e["id"]]]
    for e in G["events"]:
        if e["id"] in MERGE:
            continue
        extra = {}
        pk = PLACE_OF.get(e["id"]) or next((PLACE_OF[m] for m, t in MERGE.items() if t == e["id"] and m in PLACE_OF), None)
        if pk:
            extra["place"] = PLACES[pk]
        if e["id"] in ABOUT_CASKET:
            extra["about"] = [OBJ]
        why = f"Created from the Casket Letters timeline, event {e['id']}."
        dups = [m for m, t in MERGE.items() if t == e["id"]]
        if dups:
            why += f" Merged with {', '.join(dups)} (the same event drawn in the detail panel)."
        if e["id"] == "k6":
            extra["related"] = [ids["b5"], ids["b6"]]
            why += " Overlaps the 4 Dec and 15 Dec events (b5, b6), which are kept as their own nodes."
        if e["id"] == "k9":
            extra["related"] = [ids["b9"]]
            why += " NOT merged with b9: this one is dated 7-14 Dec 1568 and b9 9-14 Dec 1568. The two dates are unreconciled in the original timeline; both are kept."
        if e["id"] == "b9":
            extra["related"] = [ids["k9"]]
            why += " NOT merged with k9 (see there)."
        made[ids[e["id"]]] = node(ids[e["id"]], "event", e, G, extra, why)
    # the objects
    h = G["sources"]["s_hend"]
    hsrc = [{"title": h["title"], "url": h["url"], "authenticity": h["authenticity"]}]
    made[OBJ] = {"id": OBJ, "rev": 1, "type": "object", "label": "The silver casket and the letters in it (the originals are lost)", "time": "1567-06-20T12:00:00Z", "precision": "day",
                 "kind": "analysis", "status": "single", "what": "The casket said to hold the letters from Mary to Bothwell and other documents. Its first documented holder is Morton, in Morton's own declaration; its later holders are Moray, then Gowrie, then probably Arran, after which the originals disappear (Henderson). The originals are lost: only copies, translations and printed versions survive (claim casket-originals-lost).",
                 "object": {"class": "casket with documents", "material": "silver (casket)", "held_now": {"status": "lost", "note": "Not located. See claim casket-originals-lost."}},
                 "sources": hsrc, "created": TODAY,
                 "history": [{"rev": 1, "date": TODAY, "change": "Created as the object that the custody events (about) point to."}]}
    COP = "object-casket-french-copies-letters-3-to-6"
    made[COP] = {"id": COP, "rev": 1, "type": "object", "label": "French copies of Casket Letters 3 to 6", "time": "1889-01-01T00:00:00Z", "precision": "year", "kind": "analysis", "status": "single",
                 "what": "Henderson (1889): French copies of Letters 3 and 5 are in the Record Office and of Letters 4 and 6 at Hatfield. Copies of Letters 7 and 8 exist only in Scots or Latin forms (see claim casket-four-french-copies-survive).",
                 "object": {"class": "manuscript copies", "held_now": {"status": "not established", "as_of": "1889", "note": "1889 is the latest source read. Where the copies are held now has not been checked in the holdings of The National Archives or Hatfield House."}},
                 "sources": hsrc, "created": TODAY,
                 "history": [{"rev": 1, "date": TODAY, "change": "Created as the object that the 1889 location events point to. Present location is a stated gap."}]}
    for nid, pk, lab, cop in (("casket-1889-copies-of-letters-4-and-6-at-hatfield", "hatfield", "1889: French copies of Letters 4 and 6 are at Hatfield (Henderson)", "4 and 6"),
                              ("casket-1889-copies-of-letters-3-and-5-in-the-record-office", "london", "1889: French copies of Letters 3 and 5 are in the Record Office (Henderson)", "3 and 5")):
        made[nid] = {"id": nid, "rev": 1, "type": "event", "label": lab, "time": "1889-01-01T00:00:00Z", "precision": "year", "kind": "analysis", "status": "single",
                     "what": f"Henderson, The Casket Letters (1889), p. 68: copies of the French versions of Letters {cop} are held there. Where they are today has not been checked.",
                     "sources": hsrc, "place": PLACES[pk], "about": [COP], "created": TODAY,
                     "history": [{"rev": 1, "date": TODAY, "change": "Created from claim casket-four-french-copies-survive and Henderson p. 68 (as of 1889)."}]}
    for nid, n in made.items():
        dump(os.path.join(NODES_DIR, nid + ".yaml"), n)
    head = text.partition("\nevents:")[0]
    head = head.replace("\nlanes:", """
  - id: later
    title: "Panel C: 1889, where Henderson found the French copies (one tick per year)"
    start: "1888-06-01T00:00:00Z"
    end:   "1889-12-31T00:00:00Z"
    tick_years: 1
    lanes: [texts]
lanes:""", 1)
    ev = []
    for e in G["events"]:
        r = {"id": e["id"], "panel": e["panel"], "lane": e["lane"], "node": ids[e["id"]], "rev": 1}
        ev.append(r)
    for nid, lane in (("casket-1889-copies-of-letters-4-and-6-at-hatfield", "texts"), ("casket-1889-copies-of-letters-3-and-5-in-the-record-office", "texts")):
        ev.append({"id": "h" + nid.split("-letters-")[1][0], "panel": "later", "lane": lane, "node": nid, "rev": 1})
    body = "\nevents:\n" + "".join("  - " + yaml.safe_dump(r, default_flow_style=True, width=1000, sort_keys=False).strip() + "\n" for r in ev)
    open(os.path.join(ROOT, SUB), "w", encoding="utf-8").write(head + body)
    print(len(made), "nodes:", sum(1 for n in made.values() if n["type"] == "object"), "objects;", sum(1 for n in made.values() if n.get("place")), "with a place")
    for nid in sorted(made): print("  ", nid)


if __name__ == "__main__":
    main()
