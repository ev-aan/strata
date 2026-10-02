#!/usr/bin/env python3
"""One-off schema migration of build/nodes/*.yaml to v0.5 (2026-10-02). Run once.
Adds: date_basis; per source `origin`, `derives_from`, `access`, `source_type`; graded relations.
All values are assigned by rule from what the nodes already say and are listed in each node's history as 'assigned by rule, to be reviewed'.
Each changed node gets a new rev (append-only). Timeline pins are then updated with repin_timelines.py."""
import os, re, sys, glob, yaml
sys.path.insert(0, os.path.dirname(__file__))
from nodes import NODES_DIR

SOURCES = [  # (title regex, origin, derives_from, source_type)
    (r"Henderson, The Casket Letters", "henderson-1889", None, "scholarly"),
    (r"Prados, The Gulf of Tonkin Incident", "prados-2004", None, "scholarly"),
    (r"Voteview", "voteview", "us-congress-official-record", "dataset"),
    (r"Hanyok", "hanyok-2001", None, "official_history"),
    (r"NSA SIGINT intercept reports", "nsa-sigint-intercepts-1964", None, "primary_document"),
    (r"LBJ tapes", "lbj-tapes-1964", None, "primary_document"),
    (r"Congressional Record", "us-congress-official-record", None, "official_record"),
    (r"National Security Archive posting", "nsarchive-posting-2005", "nsa-release-2005", "secondary_report"),
    (r"Senate\.gov", "senate-gov-history", None, "secondary_report"),
    (r"Council on Foreign Relations", "cfr-explainer", None, "secondary_report"),
    (r"Memorandum for the Record", "bundy-staff-memo-1964", None, "primary_document"),
    (r"Seattle Times", "seattle-times-1995", None, "news"),
    (r"To Catch a Queen", "nsa-to-catch-a-queen", None, "official_history"),
]
REL = {  # (node id, target) -> (kind, grade, why)
    ("tonkin-1964-08-07-tonkin-gulf-resolution-passes", None): ("summarises", "established", "This event is the outcome of the two chamber votes, which are their own nodes."),
    ("tonkin-1964-08-04-second-attack-reported-then-refuted", None): ("summarises", "established", "A summary of the 4 August events that this node's related nodes describe in detail."),
    ("casket-1568-12-westminster-conference-examines-the-letters", None): ("same_event", "possible", "The Westminster conference is dated 7-14 Dec 1568 here and 9-14 Dec 1568 in the related node. Unreconciled; not merged."),
    ("casket-1568-12-westminster-examination-collation-minute", None): ("same_event", "possible", "The Westminster conference is dated 9-14 Dec 1568 here and 7-14 Dec 1568 in the related node. Unreconciled; not merged."),
    ("casket-1567-12-letters-probably-shown-to-the-nobles-and-parliament", None): ("overlaps", "established", "Covers the same meetings as the 4 Dec and 15 Dec 1567 events, which are kept as their own nodes."),
}


def main():
    changed = 0
    for f in sorted(glob.glob(os.path.join(NODES_DIR, "*.yaml"))):
        n = yaml.safe_load(open(f, encoding="utf-8"))
        if n.get("date_basis"):
            continue
        what = " ".join(str(n.get("what", "")).split())
        lab = n["label"]
        db = "stated"
        if re.search(r"time not|not stated|\(inferred|inferred", lab + " " + what, re.I) or n.get("status") == "inferred":
            db = "inferred"
        elif re.match(r"^(After|Early|Late)\b", lab) or re.search(r"\bprobabl", lab, re.I) or (n.get("precision") == "approx" and re.search(r"UTC|local time|Gulf time", what)):
            db = "derived"
        n["date_basis"] = db
        for s in n.get("sources") or []:
            for rx, origin, der, st in SOURCES:
                if re.search(rx, s["title"]):
                    s["origin"], s["source_type"] = origin, st
                    if der: s["derives_from"] = der
                    break
            else:
                s["origin"] = re.sub(r"[^a-z0-9]+", "-", s["title"].lower())[:40].strip("-")
            s["access"] = "cited_only" if re.search(r"not read", s["title"] + " " + str(s.get("authenticity", "")), re.I) else "read"
        for k, v in list(n.items()):
            pass
        rel = n.get("related")
        if rel:
            kind, grade, why = REL[(n["id"], None)]
            n["related"] = [{"node": r if isinstance(r, str) else r["node"], "kind": kind, "grade": grade, "why": why} for r in rel]
        n["rev"] += 1
        n["history"].append({"rev": n["rev"], "date": "2026-10-02", "change":
            f"Schema v0.5 migration, assigned by rule and to be reviewed: date_basis `{db}`; each source given an origin, a source_type and how it was accessed"
            + ("; related links graded with a stated reason." if rel else ".")})
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("# Shared node. Append-only: a change is a new `rev` plus a `history` entry, never an overwrite. See build/SCHEMA.md, Nodes.\n")
            yaml.safe_dump(n, fh, sort_keys=False, allow_unicode=True, width=120, default_flow_style=False)
        changed += 1
    print("nodes migrated:", changed)


if __name__ == "__main__":
    main()
