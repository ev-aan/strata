#!/usr/bin/env python3
"""Make the web thumbnail of an image node, the way image search keeps a small copy and links to the original.
Usage: python3 build/tools/make_thumb.py <node id> [--original-url URL] [--rights public_domain|thumbnail_only|licensed|unknown]
Reads the node's media.file, writes build/nodes/media/<id>.thumb.jpg (max 640 px wide), records its sha256, the original's
url and the rights status in the node, and adds a history entry under a new rev. Append-only: the original is never changed.
Rights: `public_domain` (for example a US Government work) may be shown whole; `thumbnail_only` means keep only the thumbnail and
the link; anything else is `unknown` until checked. This is a rule of the project, not legal advice."""
import os, sys, hashlib, yaml
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ND = os.path.join(ROOT, "build", "nodes")

def main():
    a = sys.argv[1:]
    nid = a[0]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    fp = os.path.join(ND, nid + ".yaml")
    n = yaml.safe_load(open(fp, encoding="utf-8"))
    m = n["media"]
    src = os.path.normpath(os.path.join(ND, m["file"]))
    os.makedirs(os.path.join(ND, "media"), exist_ok=True)
    out = os.path.join(ND, "media", nid + ".thumb.jpg")
    im = Image.open(src).convert("RGB")
    im.thumbnail((640, 2000))
    im.save(out, "JPEG", quality=80, optimize=True)
    m["thumb"] = f"media/{nid}.thumb.jpg"
    m["thumb_sha256"] = hashlib.sha256(open(out, "rb").read()).hexdigest()
    m["original_url"] = opt("--original-url", m.get("original_url") or (n["sources"][0]["url"] if n.get("sources") else ""))
    m["rights"] = opt("--rights", m.get("rights", "unknown"))
    n["rev"] += 1
    n["history"].append({"rev": n["rev"], "date": "2026-10-02", "change": f"Added a {im.size[0]}x{im.size[1]} thumbnail, the original's url and the rights status ({m['rights']})."})
    with open(fp, "w", encoding="utf-8") as f:
        f.write("# Shared node. Append-only: a change is a new `rev` plus a `history` entry, never an overwrite. See build/SCHEMA.md, Nodes.\n")
        yaml.safe_dump(n, f, sort_keys=False, allow_unicode=True, width=120, default_flow_style=False)
    print(nid, im.size, os.path.getsize(out), "bytes", m["rights"])

if __name__ == "__main__":
    main()
