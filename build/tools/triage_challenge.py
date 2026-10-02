#!/usr/bin/env python3
"""Completeness check for a public challenge (docs/CHALLENGES.md). It NEVER admits or declines: it only says whether the form is complete,
whether the sources are new to the page, and whether it repeats another open challenge. The issue text is treated as data, never executed.
Usage: python3 build/tools/triage_challenge.py <issue-body.md> [others.json]
others.json (optional): [{"number": 12, "claim": "...", "urls": ["..."]}] for other open challenges.
Prints one JSON object: {"status": "ready"|"needs-info", "failures": [...], "notes": [...]}"""
import os, re, sys, json, glob, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def sections(body):
    out, cur = {}, None
    for line in body.splitlines():
        m = re.match(r"^###\s+(.*\S)\s*$", line)
        if m:
            cur = m.group(1).strip().lower(); out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}

def get(sec, *names):
    for k, v in sec.items():
        if any(k.startswith(n) for n in names):
            return "" if v in ("_No response_",) else v
    return ""

def main():
    body = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
    others = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
    me = str(os.environ.get("ISSUE_NUMBER", ""))
    derived = []
    for o in others:                                    # entries may carry a raw issue body (from `gh issue list`)
        if "body" in o:
            if str(o.get("number")) == me:
                continue
            s2 = sections(o["body"])
            derived.append({"number": o["number"], "claim": re.sub(r"[^a-z0-9-]", "", get(s2, "claim id").lower()),
                            "urls": sorted(set(re.findall(r"https?://[^\s)>\]]+", get(s2, "your evidence"))))})
        else:
            derived.append(o)
    others = derived
    sec = sections(body)
    fails, notes = [], []
    sub = re.sub(r"[^a-z0-9-]", "", get(sec, "excavation").lower())
    claim = re.sub(r"[^a-z0-9-]", "", get(sec, "claim id").lower())
    what, ev, why, kind = get(sec, "the statement you dispute"), get(sec, "your evidence"), get(sec, "how it changes"), get(sec, "what kind")
    base = os.path.join(ROOT, "build", "subjects", sub) if sub else ""
    cited_text = ""
    if not sub or not os.path.isdir(base):
        fails.append("S1: the excavation is not one we publish (check the excavation field).")
    else:
        cp = os.path.join(base, "claims.yaml")
        if os.path.exists(cp):
            raw = open(cp, encoding="utf-8").read(); cited_text += raw
            ids = {c["id"] for c in (yaml.safe_load(raw) or {}).get("claims", [])}
            if claim != "assessment" and claim not in ids:
                fails.append(f"S1: `{claim or '(blank)'}` is not a claim of this excavation. Give one claim id, or `assessment`.")
        mp = os.path.join(base, "sources", "MANIFEST.yaml")
        if os.path.exists(mp): cited_text += open(mp, encoding="utf-8").read()
        for f in glob.glob(os.path.join(ROOT, "build", "nodes", "*.yaml")):
            cited_text += open(f, encoding="utf-8").read()
    if len(re.sub(r"\s+", " ", what)) < 40:
        fails.append("S1: quote the exact statement you dispute and say what is wrong (at least a sentence).")
    urls = sorted(set(re.findall(r"https?://[^\s)>\]]+", ev)))
    locator = re.search(r"\b(p\.|pp\.|page|pages|para|paragraph|section|sec\.|chapter|ch\.|folio|line|vol\.|no\.)\s*\d", ev, re.I)
    if len(ev) < 80 or not (urls or locator):
        fails.append("S2/S3: give each source with a full citation, a link or how to obtain it, and the exact page or passage.")
    elif not locator:
        notes.append("S2: no page or locator was found in the evidence; a reviewer will ask for one.")
    if len(re.sub(r"\s+", " ", why)) < 60:
        fails.append("S4: say what the claim should say instead, which part it affects, and why your evidence supports that.")
    if not re.search(r"- \[x\] I read", body, re.I) or len(re.findall(r"- \[x\]", body, re.I)) < 3:
        fails.append("Confirmation boxes are not all ticked.")
    if urls:
        already = [u for u in urls if u.rstrip("/").lower() in cited_text.lower()]
        if len(already) == len(urls):
            notes.append("S2: every link you gave is already cited on this page. This counts only if you show a different reading of it; say so.")
        elif already:
            notes.append(f"{len(already)} of your {len(urls)} links are already cited on this page.")
    for o in others:
        if o.get("claim") == claim and set(o.get("urls", [])) & set(urls):
            notes.append(f"Possible duplicate of #{o['number']} (same claim, same source). Duplicates without new evidence are closed (C3).")
    if re.search(r"\b(everyone knows|obvious(ly)?|they lied|cover.?up|wake up)\b", what + " " + why, re.I) and not urls:
        notes.append("S5: opinion without a source. Evidence is needed, not assertion.")
    print(json.dumps({"status": "needs-info" if fails else "ready", "failures": fails, "notes": notes, "claim": claim, "excavation": sub}, indent=1))

if __name__ == "__main__":
    main()
