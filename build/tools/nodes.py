#!/usr/bin/env python3
"""Shared nodes: one YAML file per dated artifact (event, document, image, recording, dataset) in build/nodes/.

A dig's timeline.yaml refers to a node instead of copying it:
    - {id: e2, panel: overview, lane: ships, node: tonkin-1964-08-02-maddox-warning-shots, rev: 1, note: "optional dig-specific reading"}
`resolve_timeline` expands such events in memory so renderers see ordinary events. Nothing is written back.
A node holds only what its sources show. What a dig makes of it (claims, readings) stays in the dig, in `note` and in the claims.
See build/SCHEMA.md, section "Nodes"."""
import os, glob, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NODES_DIR = os.path.join(ROOT, "build", "nodes")
TYPES = {"event", "document", "image", "recording", "dataset", "object"}
KINDS = {"data", "document", "official", "witness", "analysis", "media"}
STATUSES = {"single", "reported", "disputed", "inferred"}


def usage():
    """node id -> list of subjects whose timeline.yaml refers to it."""
    use = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "build", "subjects", "*", "timeline.yaml"))):
        sub = f.split(os.sep)[-2]
        for e in (yaml.safe_load(open(f, encoding="utf-8")) or {}).get("events", []):
            if e.get("node") and sub not in use.setdefault(e["node"], []):
                use[e["node"]].append(sub)
    return use


def load_nodes():
    out, use = {}, usage()
    for f in sorted(glob.glob(os.path.join(NODES_DIR, "*.yaml"))):
        n = yaml.safe_load(open(f, encoding="utf-8")) or {}
        n["_file"] = f
        out[n.get("id", os.path.basename(f)[:-5])] = n
    for k, n in out.items():
        n["_used_by"] = use.get(k, [])
    return out


def iso_key(s):
    """Sortable (year, month, day) of an ISO date, with negative years as BCE as written. Returns None if it is not a date."""
    import re
    m = re.match(r"^(-?\d{4,})(?:-(\d\d))?(?:-(\d\d))?(?:T.*)?$", str(s))
    return (int(m.group(1)), int(m.group(2) or 1), int(m.group(3) or 1)) if m else None


def assess(n):
    """Independence of a node's sources (schema v0.5). Sources that derive from the same origin count once.
    Returns {independent, read, declared, label}: label is single_origin | independent | multiple_unverified | no_source."""
    srcs = n.get("sources") or []
    derive = {s["origin"]: s.get("derives_from") for s in srcs if s.get("origin")}

    def root(o):
        seen = set()
        while derive.get(o) and o not in seen:
            seen.add(o)
            o = derive[o]
        return o

    roots, read, declared = {}, set(), True
    for i, s in enumerate(srcs):
        if s.get("origin"):
            r = root(s["origin"])
        else:
            r, declared = f"undeclared:{i}", False
        roots.setdefault(r, False)
        if s.get("access") == "read":
            roots[r] = True
    if not srcs:
        label = "no_source"
    elif len(roots) == 1:
        label = "single_origin"
    else:
        label = "independent" if declared else "multiple_unverified"
    return {"independent": len(roots), "read": sum(1 for v in roots.values() if v), "declared": declared, "label": label}


def resolve_timeline(T, nodes=None):
    """Return T with node references expanded into ordinary events (and node sources added to T['sources'])."""
    nodes = nodes if nodes is not None else load_nodes()
    srcs = T.setdefault("sources", {})
    events = []
    for e in T.get("events", []):
        nid = e.get("node")
        if not nid:
            events.append(e)
            continue
        n = nodes.get(nid)
        if n is None:
            raise SystemExit(f"timeline event {e.get('id')} refers to unknown node `{nid}`")
        ids = []
        for i, s in enumerate(n.get("sources") or []):
            k = f"n:{nid}:{i}"
            srcs[k] = {"title": s.get("title", ""), "url": s.get("url", ""), "authenticity": s.get("authenticity", "")}
            ids.append(k)
        r = {"id": e["id"], "panel": e.get("panel"), "lane": e.get("lane"), "node": nid,
             "time": n["time"], "precision": n.get("precision", "day"), "kind": n.get("kind", "analysis"),
             "status": n.get("status", "single"), "sources": ids, "label": n.get("label", nid)}
        for k in ("place", "about"):
            if n.get(k):
                r[k] = n[k]
        for k in ("end", "alt_time", "alt_tag", "alt_note", "link"):
            if n.get(k) is not None:
                r[k] = n[k]
        if n.get("media") and n["media"].get("file") and not r.get("link"):
            r["link"] = n["media"]["file"]
        detail = " ".join(str(n.get("what", "")).split())
        if e.get("note"):
            detail = (detail + " " + " ".join(str(e["note"]).split())).strip()
        r["detail"] = detail
        r["shared_by"] = n.get("_used_by", [])
        if n.get("window"):
            r["window"] = n["window"]
        r["date_basis"] = n.get("date_basis", "")
        r["corro"] = assess(n)
        events.append(r)
    T["events"] = events
    return T
