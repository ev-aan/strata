#!/usr/bin/env python3
"""Stratah conformance check.

Runs the mechanical rules from CONTRIBUTING.md over every subject in
build/subjects/. Deploys are blocked when it finds an ERROR.

    python3 build/conformance.py              # check the working tree
    python3 build/conformance.py --base REF   # also check append-only logs and
                                              # never-reused IDs against git REF

ERRORS block the deploy. WARNINGS are printed but do not block; each one names
an open question the owner has not yet ruled on.

Only rules that are mechanically decidable live here. Judgments (is this
falsifiable? is this anchor good enough?) stay with people.
"""
import argparse
import glob
import os
import subprocess
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBJECTS = os.path.join(ROOT, "build", "subjects")

STATES = {"established", "proposed", "contested", "refuted", "searched_gap"}
CLASSES = {"material", "primary_text", "interpretive", "synthetic"}
CLASS_ALIASES = {"primary-text": "primary_text"}  # older corpus spelling
REFUTATION_CLASSES = {"narrative_drift", "misattribution", "motivated_error",
                      "institutional_propaganda", "fabrication"}
CONFIDENCE = {"high", "moderate", "low", "provisional"}
# YAML reads a bare `no` as False; both mean "not checked".
ANCHOR_CHECKED = {"no", "secondary", "primary"}
REQUIRED = ["id", "state", "statement", "evidence_class", "evidential_weight",
            "adoption_weight", "anchor_checked", "would_change_if"]

# Subjects written before the weighted claim format existed. Their gaps are
# reported as WARNINGS until they are brought up to the current format.
# Remove a subject from this list once it conforms; never add new subjects.
LEGACY = {"proto-indo-european"}


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, where, msg):
        self.errors.append(f"{where}: {msg}")

    def warn(self, where, msg):
        self.warnings.append(f"{where}: {msg}")


def load(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def norm_checked(v):
    if v is False or v is None:
        return "no" if v is False else None
    if v is True:
        return "true"
    return str(v)


def check_claim(r, subject, c, legacy):
    cid = c.get("id", "<no id>")
    where = f"{subject}:{cid}"
    soft = r.warn if legacy else r.err

    for k in REQUIRED:
        if k not in c:
            soft(where, f"missing `{k}` (rules 1, 3, 7)")

    state = c.get("state")
    if state not in STATES:
        r.err(where, f"unknown state `{state}`")

    ec = c.get("evidence_class")
    if ec in CLASS_ALIASES:
        r.warn(where, f"evidence_class `{ec}` is the old spelling of `{CLASS_ALIASES[ec]}`")
        ec = CLASS_ALIASES[ec]
    if ec is not None and ec not in CLASSES:
        r.err(where, f"unknown evidence_class `{ec}`")

    conf = c.get("confidence")
    if conf is not None and conf not in CONFIDENCE:
        r.err(where, f"unknown confidence `{conf}`")

    checked = norm_checked(c.get("anchor_checked"))
    if checked is not None and checked not in ANCHOR_CHECKED:
        r.err(where, f"anchor_checked `{checked}` must be one of no | secondary | primary")

    for w in ("evidential_weight", "adoption_weight"):
        v = c.get(w)
        if v is not None and not (isinstance(v, int) and 1 <= v <= 5):
            r.err(where, f"`{w}` must be a whole number 1-5, got `{v}`")
    for banned in ("weight", "combined_weight", "total_weight", "score"):
        if banned in c:
            r.err(where, f"`{banned}` merges the two weights (rule 1)")

    # Rule 9
    if state == "refuted":
        if not c.get("refutes_target"):
            r.err(where, "Rule 9: refuted claim must name `refutes_target`")
        if ec not in ("material", "primary_text"):
            r.err(where, f"Rule 9: refutation must rest on material or primary_text, not `{ec}`")
    # Rule 12
    rc = c.get("refutation_class")
    if rc is not None:
        if state != "refuted":
            r.err(where, "Rule 12: refutation_class is only allowed on refuted claims")
        if rc not in REFUTATION_CLASSES:
            r.err(where, f"unknown refutation_class `{rc}`")

    if state == "searched_gap" and not c.get("next_step"):
        if c.get("gap_type") == "structural":
            if not c.get("gap_reason"):
                r.err(where, "structural gap must give its `gap_reason`")
        else:
            r.err(where, "searched_gap must name its `next_step`, "
                         "or be marked `gap_type: structural` with a `gap_reason`")
    if c.get("gap_type") is not None and c.get("gap_type") != "structural":
        r.err(where, f"unknown gap_type `{c.get('gap_type')}`")
    if state == "proposed" and conf == "high":
        r.err(where, "proposed is capped at provisional confidence, not high")

    if "wikipedia.org" in yaml.safe_dump(c.get("anchor", "")) + yaml.safe_dump(c.get("anchors", "")):
        r.err(where, "Wikipedia may be linked for orientation but is never an anchor")

    # Owner decision 2026-10-02: established requires a primary check, and
    # claims filed before that are re-anchored rather than downgraded. Warn
    # (not block) while that re-anchoring is in progress.
    if state == "established" and checked != "primary":
        r.warn(where, f"established but anchor_checked is `{checked}`: "
                      "re-anchor to the primary source (do not downgrade)")


def check_subject(r, sdir):
    subject = os.path.basename(sdir)
    legacy = subject in LEGACY
    ids = {}

    cpath = os.path.join(sdir, "claims.yaml")
    if os.path.exists(cpath):
        d = load(cpath) or {}
        claims = d.get("claims") or []
        if claims and "divergence_note" not in d:
            (r.warn if legacy else r.err)(subject, "no `divergence_note` (the gap is the product)")
        for c in claims:
            if not isinstance(c, dict):
                r.err(subject, "claim entry is not a mapping")
                continue
            cid = c.get("id")
            if cid in ids:
                r.err(subject, f"duplicate claim id `{cid}`")
            ids[cid] = c
            check_claim(r, subject, c, legacy)

        hc = d.get("headline_claim")
        if hc is not None:
            target = ids.get(hc)
            if target is None:
                r.err(subject, f"headline_claim `{hc}` is not a claim in this subject")
            elif d.get("headline_status") == "published":
                ok = (target.get("state") in ("established", "refuted")
                      and target.get("confidence") == "high"
                      and norm_checked(target.get("anchor_checked")) == "primary")
                if not ok:
                    r.err(subject, f"published headline rests on `{hc}`, which is not "
                                   "established/refuted at high confidence with a primary check")

    tpath = os.path.join(sdir, "threads.yaml")
    if os.path.exists(tpath):
        d = load(tpath) or {}
        for t in d.get("threads") or []:
            if t.get("confers_weight") is not False:
                r.err(f"{subject}:{t.get('id')}", "threads must set `confers_weight: false`")

    lpath = os.path.join(sdir, "log.yaml")
    if os.path.exists(lpath):
        d = load(lpath) or {}
        seen = set()
        for e in d.get("log") or []:
            lid = e.get("id")
            if lid in seen:
                r.err(subject, f"duplicate log id `{lid}`")
            seen.add(lid)


def git_show(ref, path):
    try:
        return subprocess.run(["git", "-C", ROOT, "show", f"{ref}:{path}"],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None


def check_history(r, base):
    """Rule 6 (append, never erase) and never-reused IDs, against git REF."""
    for lpath in glob.glob(os.path.join(SUBJECTS, "*", "log.yaml")):
        rel = os.path.relpath(lpath, ROOT)
        old = git_show(base, rel)
        if old is None:
            continue
        old_entries = {e.get("id"): e for e in (yaml.safe_load(old) or {}).get("log") or []}
        new_entries = {e.get("id"): e for e in (load(lpath) or {}).get("log") or []}
        for lid, e in old_entries.items():
            if lid not in new_entries:
                r.err(rel, f"log entry `{lid}` was removed (rule 6: append, never erase)")
            elif new_entries[lid] != e:
                r.err(rel, f"log entry `{lid}` was edited (rule 6: corrections are new entries)")
    for cpath in glob.glob(os.path.join(SUBJECTS, "*", "claims.yaml")):
        rel = os.path.relpath(cpath, ROOT)
        old = git_show(base, rel)
        if old is None:
            continue
        old_ids = {c.get("id") for c in (yaml.safe_load(old) or {}).get("claims") or []}
        new_ids = {c.get("id") for c in (load(cpath) or {}).get("claims") or []}
        for cid in sorted(old_ids - new_ids, key=str):
            r.err(rel, f"claim `{cid}` was deleted; retire it with a state change, never remove it")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", help="git ref to compare against for history rules")
    args = ap.parse_args()

    r = Report()
    subjects = sorted(p for p in glob.glob(os.path.join(SUBJECTS, "*")) if os.path.isdir(p))
    for sdir in subjects:
        try:
            check_subject(r, sdir)
        except yaml.YAMLError as e:
            r.err(os.path.basename(sdir), f"YAML does not parse: {e}")
    if args.base:
        check_history(r, args.base)

    for w in r.warnings:
        print(f"WARNING  {w}")
    for e in r.errors:
        print(f"ERROR    {e}")
    print(f"\n{len(subjects)} subjects checked: {len(r.errors)} errors, {len(r.warnings)} warnings")
    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
