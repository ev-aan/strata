#!/usr/bin/env python3
"""After reviewing a node change, update the `rev` that timelines pin for it (the 'read it again and update the pin' step).
Usage: python3 build/tools/repin_timelines.py   (rewrites `node: X, rev: N` in flow-style timeline files; generated timelines are rebuilt by their generator)"""
import os, re, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
from nodes import load_nodes, ROOT
nodes = load_nodes()
for f in glob.glob(os.path.join(ROOT, "build", "subjects", "*", "*.yaml")):
    t = open(f, encoding="utf-8").read()
    n = re.sub(r"node: ([^,}\s]+), rev: \d+", lambda m: f"node: {m.group(1)}, rev: {nodes[m.group(1)]['rev']}" if m.group(1) in nodes else m.group(0), t)
    if n != t:
        open(f, "w", encoding="utf-8").write(n); print("repinned", os.path.relpath(f, ROOT))
