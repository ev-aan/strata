#!/usr/bin/env python3
"""Make a PRIVATE data release of the nodes and claims: CSV, GeoJSON and GraphML, with a build id and SHA256 checksums.
Usage: python3 build/tools/export_release.py          (writes private/exports/<build-id>/)

Owner decision 2026-10-02: data downloads stay private for now. This tool only ever writes under private/ (git-ignored, never
published); build_site.py does not touch it, and the deploy workflow fails if the site contains any export file.
The checksum manifest is NOT signed: signing needs the owner's own key (see docs/DATA_RELEASE.md)."""
import os, sys, csv, json, glob, hashlib, shutil, subprocess, datetime, yaml
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.dirname(__file__))
from nodes import load_nodes, assess, ROOT

OUT_ROOT = os.path.join(ROOT, "private", "exports")
N = lambda s: " ".join(str(s if s is not None else "").split())

README = """STRATAH -- PRIVATE DATA RELEASE
===============================
Build {build}. Cite the build id: it identifies these exact bytes. Not for publication (owner decision 2026-10-02).
Made {when} from git commit {commit}. Conformance at build time: {conf}

WHAT THIS IS
  The shared nodes (events, documents, images, objects), the claims of every excavation, and the links between them.
  A NODE records what a source shows, with its date. It is not a verified fact. The judgement is in the claims.

READ THIS BEFORE USING IT
  1. DATES. Check `date_basis` on every node: stated, derived, publication_proxy, inferred, dataset_field. `precision` is separate (day, month, year).
  2. PLACES. Coordinates are place anchors from a gazetteer (OpenStreetMap Nominatim), not surveyed locations of an event. `place_precision`
     says how coarse they are. Nodes with no named place have none. Nothing is guessed.
  3. SOURCES AND INDEPENDENCE. `independent_origins` counts sources once per underlying record (a dataset built from an official record
     is the same origin as that record). `independence` is single_origin, independent, multiple_unverified or no_source.
  4. STATUS describes corroboration (single, reported, disputed, inferred), not truth. Claim `state` and `confidence` are the project's judgement and
     carry `anchor_checked` (no, secondary, primary): a claim whose anchor was not read directly is weak however it is worded.
  5. LINKS ARE GRADED. `grade=established` follows from a stated signal; `possible` is a lead and nothing more. Every link has a `why`.
  6. Values assigned by rule on 2026-10-02 (date_basis, source origins) are marked in each node's history as "to be reviewed".

FILES
  nodes.csv            one row per node
  node_sources.csv     one row per source of a node (origin, derives_from, source_type, access)
  node_links.csv       links between nodes: related (graded), about, evidences
  claims.csv           one row per claim of every excavation
  claim_nodes.csv      which nodes a claim names as its evidence
  nodes.geojson        nodes that have coordinates (RFC 7946)
  graph.graphml        nodes, claims and source origins with their links (Gephi, NetworkX, Cytoscape)

INTEGRITY
  SHA256SUMS.txt covers every file here:  sha256sum -c SHA256SUMS.txt
  The build id is the first 12 characters of the sha256 of the list of data-file checksums (every line of SHA256SUMS.txt except README.txt).
  {signed}
"""


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def main():
    nodes = load_nodes()
    claims = []
    for f in sorted(glob.glob(os.path.join(ROOT, "build", "subjects", "*", "claims.yaml"))):
        sub = f.split(os.sep)[-2]
        for c in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("claims", []):
            claims.append((sub, c))
    stage = os.path.join(OUT_ROOT, "_building")
    shutil.rmtree(stage, ignore_errors=True)
    os.makedirs(stage)

    # nodes.csv
    hdr = ["id", "rev", "type", "label", "time", "end", "precision", "date_basis", "kind", "status", "independent_origins", "origins_read", "independence",
           "place_name", "lat", "lon", "place_precision", "used_by", "what"]
    rows = []
    for k, n in nodes.items():
        a = assess(n)
        pl = n.get("place") or {}
        rows.append([k, n["rev"], n["type"], N(n["label"]), n["time"], n.get("end", ""), n.get("precision", ""), n.get("date_basis", ""), n.get("kind", ""), n["status"],
                     a["independent"], a["read"], a["label"], pl.get("name", ""), pl.get("lat", ""), pl.get("lon", ""), pl.get("precision", ""), " ".join(n.get("_used_by", [])), N(n.get("what", ""))])
    write_csv(os.path.join(stage, "nodes.csv"), hdr, rows)
    rows = [[k, i, s.get("origin", ""), s.get("derives_from", ""), s.get("source_type", ""), s.get("access", ""), N(s.get("title")), s.get("url", ""), N(s.get("authenticity", ""))]
            for k, n in nodes.items() for i, s in enumerate(n.get("sources") or [])]
    write_csv(os.path.join(stage, "node_sources.csv"), ["node", "n", "origin", "derives_from", "source_type", "access", "title", "url", "authenticity"], rows)
    links = []
    for k, n in nodes.items():
        for r in n.get("related") or []:
            r = r if isinstance(r, dict) else {"node": r}
            links.append([k, r["node"], "related", r.get("kind", ""), r.get("grade", ""), N(r.get("why", ""))])
        for o in n.get("about") or []:
            links.append([k, o, "about", "", "established", "event is part of this object's history"])
        for o in n.get("evidences") or []:
            links.append([k, o, "evidences", "", "established", "this artifact is evidence for that node"])
    write_csv(os.path.join(stage, "node_links.csv"), ["from", "to", "link", "kind", "grade", "why"], links)
    rows, cn = [], []
    for sub, c in claims:
        an = c.get("anchor") if isinstance(c.get("anchor"), dict) else {}
        rows.append([sub, c["id"], c["state"], c.get("statement_kind", ""), c.get("confidence", ""), c.get("evidence_class", ""), c.get("evidential_weight", ""), c.get("adoption_weight", ""), c.get("anchor_checked", ""), N(c["statement"])])
        for x in an.get("nodes") or []:
            cn.append([sub, c["id"], x["node"] if isinstance(x, dict) else x, x.get("verb", "") if isinstance(x, dict) else ""])
    write_csv(os.path.join(stage, "claims.csv"), ["subject", "id", "state", "statement_kind", "confidence", "evidence_class", "evidential_weight", "adoption_weight", "anchor_checked", "statement"], rows)
    write_csv(os.path.join(stage, "claim_nodes.csv"), ["subject", "claim", "node", "verb"], cn)

    # geojson: only nodes with coordinates
    feats = []
    for k, n in nodes.items():
        pl = n.get("place") or {}
        if pl.get("lat") is None:
            continue
        feats.append({"type": "Feature", "geometry": {"type": "Point", "coordinates": [pl["lon"], pl["lat"]]},
                      "properties": {"id": k, "label": N(n["label"]), "time": n["time"], "date_basis": n.get("date_basis", ""), "place": pl["name"], "place_precision": pl.get("precision", ""),
                                     "uncertainty_km": pl.get("uncertainty_km", ""), "coordinate_source": N(pl.get("source", ""))}})
    json.dump({"type": "FeatureCollection", "features": feats}, open(os.path.join(stage, "nodes.geojson"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # graphml
    ns = "http://graphml.graphdrawing.org/xmlns"
    ET.register_namespace("", ns)
    g = ET.Element(f"{{{ns}}}graphml")
    for kid, name, dom in (("label", "label", "node"), ("kind", "kind", "node"), ("time", "time", "node"), ("grade", "grade", "edge"), ("link", "link", "edge"), ("why", "why", "edge")):
        ET.SubElement(g, f"{{{ns}}}key", {"id": kid, "for": dom, "attr.name": name, "attr.type": "string"})
    gr = ET.SubElement(g, f"{{{ns}}}graph", {"edgedefault": "directed"})
    def node(i, label, kind, time=""):
        e = ET.SubElement(gr, f"{{{ns}}}node", {"id": i})
        for k, v in (("label", label), ("kind", kind), ("time", time)):
            ET.SubElement(e, f"{{{ns}}}data", {"key": k}).text = str(v)
    def edge(a, b, link, grade="", why=""):
        e = ET.SubElement(gr, f"{{{ns}}}edge", {"source": a, "target": b})
        for k, v in (("link", link), ("grade", grade), ("why", why)):
            ET.SubElement(e, f"{{{ns}}}data", {"key": k}).text = v
    origins = set()
    for k, n in nodes.items():
        node(k, N(n["label"]), "node:" + n["type"], n["time"])
        for s in n.get("sources") or []:
            if s.get("origin"):
                origins.add(s["origin"])
                edge(k, "origin:" + s["origin"], "sourced_from", "established", s.get("source_type", ""))
    for o in sorted(origins):
        node("origin:" + o, o, "origin")
    for sub, c in claims:
        node(f"claim:{sub}:{c['id']}", N(c["statement"])[:120], "claim:" + c["state"])
    for l in links:
        edge(l[0], l[1], l[2] + (":" + l[3] if l[3] else ""), l[4], l[5])
    for sub, cid, x, vb in cn:
        edge(f"claim:{sub}:{cid}", x, "anchored_on" + (":" + vb if vb else ""), "established", "")
    ET.ElementTree(g).write(os.path.join(stage, "graph.graphml"), encoding="utf-8", xml_declaration=True)

    # build info, readme, checksums
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    conf = subprocess.run([sys.executable, os.path.join(ROOT, "build", "conformance.py")], cwd=ROOT, capture_output=True, text=True).stdout.strip().splitlines()[-1]
    when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    signed = "The manifest is NOT signed yet: signing needs the owner's own key (see docs/DATA_RELEASE.md). Checksums prove the files match the manifest, not who made it."
    def sums():
        out = []
        for fn in sorted(os.listdir(stage)):
            if fn in ("SHA256SUMS.txt", "README.txt"):
                continue
            out.append(f"{hashlib.sha256(open(os.path.join(stage, fn), 'rb').read()).hexdigest()}  {fn}")
        return "\n".join(out) + "\n"
    s = sums()
    build = hashlib.sha256(s.encode()).hexdigest()[:12]
    open(os.path.join(stage, "README.txt"), "w", encoding="utf-8").write(README.format(build=build, when=when, commit=commit, conf=conf, signed=signed))
    s = sums() + f"{hashlib.sha256(open(os.path.join(stage, 'README.txt'), 'rb').read()).hexdigest()}  README.txt\n"
    open(os.path.join(stage, "SHA256SUMS.txt"), "w").write(s)
    final = os.path.join(OUT_ROOT, build)
    shutil.rmtree(final, ignore_errors=True)
    os.rename(stage, final)
    assert os.path.realpath(final).startswith(os.path.realpath(os.path.join(ROOT, "private"))), "exports must stay under private/"
    print(f"build {build}: {len(nodes)} nodes, {len(claims)} claims, {len(feats)} placed -> {os.path.relpath(final, ROOT)}")
    return final


if __name__ == "__main__":
    main()
