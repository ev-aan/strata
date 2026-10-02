#!/usr/bin/env python3
"""
Thread validator (prototype). Enforces the four thread rules mechanically against the
corpus, so the firewall between synthesis and evidence is checked, not merely asserted.

This is a standalone prototype for the new primitive; it must eventually be folded into
the main eight-rule validator (and share its claim-loading). Field names follow the
corpus YAML in this directory and may need reconciliation with the live schema.
"""
import sys, glob, os
try:
    import yaml
except ImportError:
    sys.exit("pyyaml required: pip install pyyaml --break-system-packages")

CORPUS_DIR = os.path.dirname(os.path.abspath(__file__))
ATTEST = {"preserved", "reconstructed", "inferred", "interpretive"}
WEAKEST_ORDER = ["preserved", "reconstructed", "inferred", "interpretive"]  # strong -> weak

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def main():
    claim_ids = set()
    thread_ids = set()
    anchor_refs = []  # (claim_id, ref_string)

    # 1) collect claim ids and anchor refs from every subject file
    for path in sorted(glob.glob(os.path.join(CORPUS_DIR, "*.yaml"))):
        doc = load_yaml(path)
        if not doc or "subject" not in doc:
            continue
        subj = doc["subject"]["id"]
        for c in doc.get("claims", []):
            cid = f"{subj}:{c['id']}"
            claim_ids.add(cid)
            for a in c.get("anchors", []):
                anchor_refs.append((cid, str(a.get("ref", ""))))

    # 2) load threads
    tdoc = load_yaml(os.path.join(CORPUS_DIR, "threads.yaml"))
    threads = tdoc.get("threads", []) if tdoc else []
    for t in threads:
        thread_ids.add(t["id"])

    errors, warnings, info = [], [], []

    for t in threads:
        tid, ttype = t["id"], t.get("type")
        members = t.get("members", [])

        # RULE T1 — no orphan members
        unresolved = [m["claim"] for m in members if m["claim"] not in claim_ids]
        for u in unresolved:
            (warnings if u.startswith("gilgamesh:") else errors).append(
                f"[T1] {tid}: member '{u}' does not resolve to a known claim id"
                + (" (expected — Gilgamesh seed-corpus ids pending reconciliation)"
                   if u.startswith("gilgamesh:") else "")
            )

        # RULE T3 — morphology threads: every member tagged; surface weakest node
        if ttype == "morphology":
            for m in members:
                if m.get("attestation") not in ATTEST:
                    errors.append(f"[T3] {tid}: member '{m['claim']}' missing/invalid attestation")
            present = [m["attestation"] for m in members if m.get("attestation") in ATTEST]
            if present:
                weakest = max(present, key=lambda a: WEAKEST_ORDER.index(a))
                tag = "" if weakest == "preserved" else "  <-- thread no stronger than this"
                info.append(f"[T3] {tid}: weakest-attested node = '{weakest}'{tag}")

        # RULE T4 — reception-overlay threads carry no weight, members interpretive/contested
        if ttype == "reception-overlay":
            if t.get("confers_weight", True) is not False:
                errors.append(f"[T4] {tid}: reception-overlay must set confers_weight: false")
            else:
                info.append(f"[T4] {tid}: overlay correctly declares confers_weight: false (zero evidential weight)")

    # RULE T2 — firewall: no thread id may appear in any claim's anchors
    for cid, ref in anchor_refs:
        for tid in thread_ids:
            if tid in ref:
                errors.append(f"[T2] claim '{cid}' cites thread '{tid}' as an anchor — synthesis is not evidence")
    info.append(f"[T2] firewall checked across {len(anchor_refs)} anchors; threads cited as evidence: "
                f"{sum(1 for cid,ref in anchor_refs for tid in thread_ids if tid in ref)}")

    print(f"corpus: {len(claim_ids)} claims across "
          f"{len(set(c.split(':')[0] for c in claim_ids))} subjects; {len(threads)} threads\n")
    for line in info:    print("  ok   ", line)
    print()
    for line in warnings: print("  WARN ", line)
    for line in errors:   print("  FAIL ", line)
    print()
    if errors:
        print(f"RESULT: {len(errors)} hard failures, {len(warnings)} warnings")
        sys.exit(1)
    print(f"RESULT: pass ({len(warnings)} warnings)")

if __name__ == "__main__":
    main()
