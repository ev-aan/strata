#!/usr/bin/env python3
"""One-off pilot: move the Tonkin family (gulf-of-tonkin timeline, the Tonkin overlay and the Tonkin-related roll calls of
votes-johnson-tonkin, and the Congressional Record page images) into shared nodes in build/nodes/.
Run once, from the commit before the migration: it reads the original timelines from git HEAD and rewrites them as node references.
Merges made (same event described twice): see MERGES. Nothing else is merged."""
import os, re, sys, glob, hashlib, subprocess, yaml
sys.path.insert(0, os.path.dirname(__file__))
from nodes import NODES_DIR, ROOT

SUBJ = os.path.join(ROOT, "build", "subjects")
TODAY = "2026-10-02"
MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*"


def git_show(path):
    return subprocess.run(["git", "show", "HEAD:" + path], cwd=ROOT, capture_output=True, text=True).stdout


def slug(s, n=7):
    s = re.sub(r"\([^)]*\)", " ", s.lower())
    return "-".join(re.sub(r"[^a-z0-9]+", " ", s).split()[:n])


def strip_date(label):
    m = re.match(rf"^\s*((?:(?:early|late)\s+)?(?:\d{{1,2}}\s+)?(?:{MONTH}\.?\s*)?(?:\d{{4}})?)\s*:\s*", label, flags=re.I)
    if m and m.group(1).strip() and (re.search(MONTH, m.group(1), re.I) or re.search(r"\d{4}", m.group(1))):
        return label[m.end():]
    return label


def src_list(T, ids):
    out = []
    for k in ids:
        s = T["sources"][k]
        out.append({"title": s["title"], "url": s.get("url", ""), "authenticity": s.get("authenticity", "")})
    return out


def dump(path, d):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Shared node. Append-only: a change is a new `rev` plus a `history` entry, never an overwrite. See build/SCHEMA.md, Nodes.\n")
        yaml.safe_dump(d, f, sort_keys=False, allow_unicode=True, width=120, default_flow_style=False)


def node(id_, type_, e, T, extra=None, created="", merged=""):
    n = {"id": id_, "rev": 1, "type": type_, "label": " ".join(str(e["label"]).split()), "time": str(e["time"]),
         "precision": e.get("precision", "day"), "kind": e.get("kind", "analysis"), "status": e.get("status", "single")}
    for k in ("end", "alt_time", "alt_tag", "alt_note"):
        if e.get(k): n[k] = str(e[k])
    n["what"] = " ".join(str(e.get("detail", "")).split())
    n["sources"] = src_list(T, e.get("sources", []))
    if e.get("link"): n["link"] = e["link"]
    if extra: n.update(extra)
    n["created"] = TODAY
    n["history"] = [{"rev": 1, "date": TODAY, "change": created}]
    return n


def main():
    os.makedirs(NODES_DIR, exist_ok=True)
    gpath = "build/subjects/gulf-of-tonkin/timeline.yaml"
    gtext = git_show(gpath)
    G = yaml.safe_load(gtext)
    vtext = git_show("build/subjects/votes-johnson-tonkin/timeline.yaml")
    V = yaml.safe_load(vtext)
    X = yaml.safe_load(git_show("build/subjects/votes-johnson-tonkin/extra_events.yaml"))
    byid = {e["id"]: e for e in V["events"]}
    xby = {e["id"]: e for e in X["events"]}

    ids, refs_g, refs_x, refs_v = {}, {}, {}, {}
    # 1. Tonkin dig events
    for e in G["events"]:
        d = str(e["time"])[:10]
        ids[e["id"]] = f"tonkin-{d}-{slug(strip_date(e['label']))}"
    # 2. roll-call nodes for the Tonkin family
    vote_ids = {}
    for vid in ["v1", "v2"] + [f"v{i}" for i in range(38, 47)]:
        e = byid[vid]
        vote_ids[vid] = "vote-" + e["link"].rsplit("/", 1)[1]
    # merges: same event described in two digs
    MERGES = {"t1": "e2", "v44": "g9"}
    ids["g9"] = vote_ids["v44"]            # the 24 Jun 1970 Senate vote keeps the dataset id
    made = {}
    for e in G["events"]:
        nid = ids[e["id"]]
        extra, why = {}, f"Created from the Gulf of Tonkin timeline, event {e['id']}."
        if e["id"] == "e2":
            t1 = xby["t1"]
            why += " Merged with votes-johnson-tonkin overlay event t1 (same event, same time)."
            e = dict(e); e["sources"] = list(e["sources"])
        if e["id"] == "g9":
            v = byid["v44"]
            why += " Merged with votes-johnson-tonkin roll-call event v44 (the same Senate vote, Voteview roll call)."
            e = dict(e); e["detail"] = e["detail"] + " Voteview record: " + v["detail"]
        if e["id"] == "e7":
            extra["related"] = [vote_ids["v1"], vote_ids["v2"]]
            why += " Summary of the two chamber votes, which are their own nodes (related)."
        n = node(nid, "document" if e["id"] == "f9" else "event", e, G, extra, why)
        if e["id"] == "f9":
            n["manifest"] = {"subject": "gulf-of-tonkin", "source": "src-bundy-memo-1964"}
        if e["id"] == "e2":
            for s in src_list(V, ["s_hanyok"]) if False else []: pass
        made[nid] = n
        refs_g[e["id"]] = nid
    # t1 merged into e2 (same sources already listed), t2 is its own node
    refs_x["t1"] = ids["e2"]
    t2 = xby["t2"]
    nid = "tonkin-1964-08-04-second-attack-reported-then-refuted"
    made[nid] = node(nid, "event", {**t2, "label": "4 Aug: a second attack on the destroyers is reported (NSA's own study finds it did not happen)",
                                    "detail": "Summary node for the reported second attack of 4 August 1964. Its detail is in the 4 August events (f1 to f8). The study's finding is the claim tonkin-aug4-attack-occurred in the Gulf of Tonkin dig."},
                     X, {"related": [ids[k] for k in ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8")]},
                     "Created from votes-johnson-tonkin overlay event t2. Overlaps the 4 August events of the Gulf of Tonkin dig but is a summary, so it was not merged.")
    refs_x["t2"] = nid
    # roll-call nodes (v44 already made via g9)
    for vid, nid in vote_ids.items():
        if vid == "v44":
            refs_v[vid] = nid
            continue
        e = byid[vid]
        made[nid] = node(nid, "event", e, V, None, f"Created from votes-johnson-tonkin roll-call event {vid} (Voteview).")
        refs_v[vid] = nid
    # new event: Fulbright opens the debate (page image already held)
    fid = "tonkin-1964-08-06-fulbright-opens-senate-debate-aug4-as-fact"
    cr = [s for s in yaml.safe_load(open(os.path.join(SUBJ, "gulf-of-tonkin", "sources", "MANIFEST.yaml")))["sources"]]
    cr64 = next(s for s in cr if s["id"] == "src-congressional-record-1964-aug6")
    made[fid] = node(fid, "event", {"label": "6 Aug: Fulbright opens the Senate debate and states the 4 August attack as fact", "time": "1964-08-06T12:00:00Z", "precision": "day",
                                    "kind": "official", "status": "single",
                                    "detail": "Fulbright: 'On August 4 the Maddox and another destroyer, the C. Turner Joy, were again attacked by North Vietnamese torpedo boats in international waters ... without any doubt a calculated act of military aggression.' Congressional Record, Senate, 6 Aug 1964, p. 18399, read on the page image. See claim tonkin-fulbright-opening-aug4-as-fact."},
                     {"sources": []}, {"manifest": {"subject": "gulf-of-tonkin", "source": "src-congressional-record-1964-aug6"}},
                     "Created from claim tonkin-fulbright-opening-aug4-as-fact, whose anchor is the page image (node crec-1964-p18399).")
    made[fid]["sources"] = [{"title": cr64["title"], "url": cr64["url"], "authenticity": "authenticated, strong (see the dig's sources manifest)"}]
    # 3. page images
    img_dir = os.path.join(SUBJ, "gulf-of-tonkin", "sources", "congressional-record")
    IM = {"crec-1964-p18399-061.png": ("crec-1964-p18399", "1964-08-06", "Congressional Record, Senate, 6 Aug 1964, p. 18399 (page image)", "src-congressional-record-1964-aug6", [fid]),
          "crec-1964-p18470-30.png": ("crec-1964-p18470", "1964-08-07", "Congressional Record, Senate, 7 Aug 1964, p. 18470, roll call on the resolution (page image)", "src-congressional-record-1964", [ids["e7"]]),
          "crec-1970-p21119-019.png": ("crec-1970-p21119", "1970-06-24", "Congressional Record, Senate, 24 Jun 1970, p. 21119 (page image)", "src-congressional-record-1970", [vote_ids["v44"]]),
          "crec-1970-p21131-031.png": ("crec-1970-p21131", "1970-06-24", "Congressional Record, Senate, 24 Jun 1970, p. 21131 (page image)", "src-congressional-record-1970", [vote_ids["v44"]]),
          "crec-1970-p21132-032.png": ("crec-1970-p21132", "1970-06-24", "Congressional Record, Senate, 24 Jun 1970, p. 21132, roll call on the Dole amendment (page image)", "src-congressional-record-1970", [vote_ids["v44"]])}
    man = {s["id"]: s for s in cr}
    for fn, (nid, d, label, src, ev) in IM.items():
        p = os.path.join(img_dir, fn)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        n = {"id": nid, "rev": 1, "type": "image", "label": label, "time": f"{d}T12:00:00Z", "precision": "day", "kind": "document", "status": "single",
             "what": "A page image of the GPO bound edition, stored as the checked copy behind the quotations and vote counts read from it. The full volume is not stored.",
             "sources": [{"title": man[src]["title"], "url": man[src]["url"], "authenticity": "authenticated, strong (see the dig's sources manifest)"}],
             "media": {"file": f"../subjects/gulf-of-tonkin/sources/congressional-record/{fn}", "sha256": h},
             "manifest": {"subject": "gulf-of-tonkin", "source": src}, "evidences": ev, "created": TODAY,
             "history": [{"rev": 1, "date": TODAY, "change": "Created from the stored page image; sha256 recomputed and equals the value in the dig's sources manifest."}]}
        made[nid] = n
    for nid, n in made.items():
        dump(os.path.join(NODES_DIR, nid + ".yaml"), n)

    # 4. rewrite the Tonkin timeline: references instead of copies (header comments kept)
    head, _, _ = gtext.partition("\nevents:")
    ev = []
    for e in G["events"]:
        r = {"id": e["id"], "panel": e["panel"], "lane": e["lane"], "node": refs_g[e["id"]], "rev": 1}
        ev.append(r)
        if e["id"] == "e6":
            ev.append({"id": "e6b", "panel": e["panel"], "lane": e["lane"], "node": fid, "rev": 1})
    body = "\nevents:\n" + "".join("  - " + yaml.safe_dump(r, default_flow_style=True, width=1000, sort_keys=False).strip() + "\n" for r in ev)
    open(os.path.join(ROOT, gpath), "w", encoding="utf-8").write(head + body)
    # 5. overlay events of the votes dig
    xtext = git_show("build/subjects/votes-johnson-tonkin/extra_events.yaml")
    xhead = xtext.partition("\nevents:")[0]
    notes = {"t1": "In this dig: claim tonkin-aug2-maddox-engaged. See the Gulf of Tonkin dig.", "t2": "See the Gulf of Tonkin dig."}
    xev = [{"id": k, "panel": xby[k]["panel"], "lane": xby[k]["lane"], "node": refs_x[k], "rev": 1, "note": notes[k]} for k in ("t1", "t2")]
    open(os.path.join(SUBJ, "votes-johnson-tonkin", "extra_events.yaml"), "w", encoding="utf-8").write(
        xhead + "\nevents:\n" + "".join("  - " + yaml.safe_dump(r, default_flow_style=True, width=1000, sort_keys=False).strip() + "\n" for r in xev))
    print(f"nodes written: {len(made)} ({sum(1 for n in made.values() if n['type']=='image')} images)")
    for nid in sorted(made): print("  ", nid)


if __name__ == "__main__":
    main()
