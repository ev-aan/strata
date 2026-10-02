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


def check_anchor_format(r, subject, c, sdir):
    """N25: every claim has ONE `anchor` mapping {type, description, [sources], [nodes], [accessible]}. No `anchors:` list, no `ref:`."""
    where = f"{subject}:{c.get('id')}"
    if "anchors" in c:
        r.err(where, "uses `anchors:`; the format is one `anchor:` mapping (SCHEMA N25)")
    a = c.get("anchor")
    if not isinstance(a, dict):
        r.err(where, "`anchor` must be a mapping with `type` and `description` (SCHEMA N25)")
        return
    for k in ("type", "description"):
        if not str(a.get(k) or "").strip():
            r.err(where, f"anchor is missing `{k}` (SCHEMA N25)")
    if "ref" in a:
        r.err(where, "anchor uses `ref:`; use `sources: [manifest ids]` (SCHEMA N25)")
    srcs = a.get("sources")
    if srcs is not None:
        if not isinstance(srcs, list):
            r.err(where, "anchor `sources` must be a list of manifest ids")
        else:
            mpath = os.path.join(sdir, "sources", "MANIFEST.yaml")
            ids = {s.get("id") for s in ((load(mpath) or {}).get("sources") or [])} if os.path.exists(mpath) else set()
            for s in srcs:
                if s not in ids:
                    r.err(where, f"anchor source `{s}` is not in sources/MANIFEST.yaml (SCHEMA N25)")


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

    # schema v0.6 (SCHEMA.md N18-N22)
    sk = c.get("statement_kind")
    if sk is not None and sk not in ("reported", "judgment", "assumption", "search_result"):
        r.err(where, f"unknown statement_kind `{sk}`")
    for k_, need in (("assumptions", ("text", "if_wrong")), ("alternatives", ("text", "why_not_preferred"))):
        for x in c.get(k_) or []:
            for f_ in need:
                if not (isinstance(x, dict) and x.get(f_)):
                    r.err(where, f"each entry of `{k_}` needs `{f_}`")
    if c.get("likelihood") is not None and c["likelihood"] not in ("almost no chance", "very unlikely", "unlikely", "roughly even chance", "likely", "very likely", "almost certain"):
        r.err(where, f"unknown likelihood term `{c['likelihood']}`")
    cr = c.get("confidence_reasons")
    if cr:
        lv = {"provisional": 0, "low": 1, "moderate": 2, "high": 3}
        eff = {"down1": -1, "down2": -2, "up1": 1, "none": 0}
        domains = {"risk_of_bias", "inconsistency", "indirectness", "imprecision", "unreported_negative_results", "independent_corroboration", "primary_anchor_read", "convergent_material_evidence"}
        if cr.get("start") not in lv:
            r.err(where, "confidence_reasons.start must be high | moderate | low | provisional")
        net = 0
        for st_ in cr.get("steps") or []:
            if st_.get("domain") not in domains:
                r.err(where, f"unknown confidence domain `{st_.get('domain')}`")
            if st_.get("effect") not in eff:
                r.err(where, f"unknown confidence effect `{st_.get('effect')}` (down1 | down2 | up1 | none)")
            else:
                net += eff[st_["effect"]]
            if not st_.get("reason"):
                r.err(where, "every confidence step needs a written reason")
        if cr.get("start") in lv:
            got = max(0, min(3, lv[cr["start"]] + net))
            if conf in lv and lv[conf] > got:
                r.err(where, f"confidence `{conf}` is higher than its recorded reasons give ({[k for k, v in lv.items() if v == got][0]})")
            elif conf in lv and lv[conf] < got:
                r.warn(where, f"confidence `{conf}` is lower than its recorded reasons give; say why in a step")
    for d_ in c.get("disputed_by") or []:
        for f_ in ("who", "kind", "position", "source_read"):
            if d_.get(f_) in (None, ""):
                r.err(where, f"disputed_by entry needs `{f_}`")
        if d_.get("kind") not in ("person", "institution", "group", "work", "unnamed"):
            r.err(where, f"disputed_by kind `{d_.get('kind')}` unknown")
    if state == "contested" and not c.get("disputed_by"):
        r.warn(where, "contested claim names no disputant (`disputed_by`)")

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


PUB_STATUS = {"published", "unpublished", "corrected", "expression_of_concern",
              "withdrawn", "retracted"}
PUB_FLAGGED = {"expression_of_concern", "withdrawn", "retracted"}


def load_sources(sdir):
    for name in (os.path.join("sources", "MANIFEST.yaml"), "sources.yaml"):
        p = os.path.join(sdir, name)
        if os.path.exists(p):
            return {s.get("id"): s for s in (load(p) or {}).get("sources") or []
                    if isinstance(s, dict)}
    return {}


def claim_refs(c):
    a = c.get("anchor") if isinstance(c.get("anchor"), dict) else {}
    refs = list(a.get("sources") or []) + list(a.get("ref") or [])
    for a in c.get("anchors") or []:
        if isinstance(a, dict):
            refs += a.get("ref") or []
    return refs


def check_publication(r, subject, sdir, claims, d):
    """Rules PS1-PS4 (build/SCHEMA.md): a retracted or flagged publication can never
    be cited as if it were sound, and its status must be shown at the top of the dig."""
    sources = load_sources(sdir)
    flagged = {}
    for sid, s in sources.items():
        pub = s.get("publication")
        if pub is None:
            continue
        st = pub.get("status") if isinstance(pub, dict) else None
        if st not in PUB_STATUS:
            r.err(f"{subject}:{sid}", f"PS1: publication status `{st}` must be one of "
                                      + " | ".join(sorted(PUB_STATUS)))
            continue
        if st in PUB_FLAGGED:
            if not pub.get("date") or not pub.get("notice"):
                r.err(f"{subject}:{sid}", f"PS2: a `{st}` publication needs its `date` and `notice`")
            flagged[sid] = st
    shown = {n.get("source") for n in d.get("source_notices") or [] if isinstance(n, dict)}
    for c in claims:
        if not isinstance(c, dict):
            continue
        ack = set(c.get("flagged_sources") or [])
        for ref in claim_refs(c):
            st = flagged.get(ref)
            if st and ref not in ack:
                msg = (f"PS3: cites `{ref}`, which is {st.replace('_', ' ')}; list it in "
                       "`flagged_sources` so the status is shown with the claim")
                (r.err if st in ("retracted", "withdrawn") else r.warn)(f"{subject}:{c.get('id')}", msg)
    for sid, st in flagged.items():
        if st in ("retracted", "withdrawn") and sid not in shown:
            r.err(subject, f"PS4: `{sid}` is {st} but has no entry in `source_notices` "
                           "at the top of claims.yaml")


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
            check_anchor_format(r, subject, c, sdir)

        check_publication(r, subject, sdir, claims, d)

        vd = d.get("assessment")
        if vd:
            for k_ in ("question", "answer", "headline", "text", "basis", "would_settle"):
                if not vd.get(k_):
                    r.err(subject, f"assessment missing `{k_}`")
            if vd.get("answer") not in ("yes", "no", "leans_yes", "leans_no", "unsettled", "partly"):
                r.err(subject, f"assessment answer `{vd.get('answer')}` unknown")
            _txt = " ".join(str(vd.get(k_, "")) for k_ in ("headline", "text")) + " " + " ".join(str(v_) for v_ in (vd.get("lean") or {}).values())
            if "%" in _txt or "percent" in _txt.lower():
                r.err(subject, "an assessment must not state a percentage: no source supplies one (SCHEMA N23)")
            kp_ = vd.get("key_points") or []
            if len(kp_) != 3:
                r.warn(subject, "the assessment should give exactly three `key_points` (the executive summary)")
            for k_ in kp_:
                if len(str(k_)) > 170:
                    r.warn(subject, "a key point is over 170 characters")
            if len(str(vd.get("headline", ""))) > 200:
                r.warn(subject, "assessment headline is over 200 characters")
            _by = {c_.get("id"): c_ for c_ in claims}
            for b_ in vd.get("basis") or []:
                if b_ not in _by:
                    r.err(subject, f"assessment basis `{b_}` is not a claim in this subject")
            if vd.get("answer") in ("leans_yes", "leans_no") and not any(_by.get(b_, {}).get("confidence") in ("moderate", "high") for b_ in vd.get("basis") or []):
                r.err(subject, "a 'leans' assessment needs at least one basis claim at moderate or high confidence; otherwise say unsettled and give a `lean` note")
            if vd.get("lean"):
                for k_ in ("toward", "short", "strength", "because", "caveats"):
                    if not vd["lean"].get(k_):
                        r.err(subject, f"assessment lean missing `{k_}`")
        hc = d.get("headline_claim")
        if hc is not None:
            target = ids.get(hc)
            if target is None:
                r.err(subject, f"headline_claim `{hc}` is not a claim in this subject")
            elif d.get("headline_status") in ("review", "published"):
                ok = (target.get("state") in ("established", "refuted")
                      and target.get("confidence") == "high"
                      and norm_checked(target.get("anchor_checked")) == "primary")
                if not ok:
                    r.err(subject, f"{d.get('headline_status')} headline rests on `{hc}`, which is not "
                                   "established/refuted at high confidence with a primary check")

        h = d.get("headline")
        if h and not 70 <= len(h) <= 95:
            r.warn(subject, f"headline is {len(h)} characters; aim for 70-95 (rule 7)")
        if claims and not h and d.get("dig_status") not in ("parked", "pilot_draft", "data", "open_corpus"):
            r.warn(subject, "has claims but no headline and no dig_status; a complete dig needs a specific headline")

    chpath = os.path.join(sdir, "challenges.yaml")
    if os.path.exists(chpath):
        seen = set()
        for ch in (load(chpath) or {}).get("challenges") or []:
            cid = ch.get("id")
            if cid in seen:
                r.err(subject, f"duplicate challenge id `{cid}`")
            seen.add(cid)
            for k in ("challenge", "raised_by", "test", "result", "answer"):
                if not ch.get(k):
                    r.err(f"{subject}:{cid}", f"challenge missing `{k}`")
            if ch.get("result") not in ("answered", "partly_answered", "open", "finding_changed", "declined"):
                r.err(f"{subject}:{cid}", f"challenge result `{ch.get('result')}` is not allowed")
            ik = ch.get("intake")
            if ik is not None:
                for k_ in ("issue", "decided", "criteria"):
                    if not ik.get(k_):
                        r.err(f"{subject}:{cid}", f"challenge intake needs `{k_}`")
                crit = ik.get("criteria") or {}
                for s_ in ("S1", "S2", "S3", "S4", "S5"):
                    if crit.get(s_) not in ("pass", "fail"):
                        r.err(f"{subject}:{cid}", f"intake criterion {s_} must be pass or fail")
                if ch.get("result") != "declined" and any(v == "fail" for v in crit.values()):
                    r.err(f"{subject}:{cid}", "a challenge that failed an admission criterion cannot have an admitted result")
            for ref in ch.get("touches") or []:
                if ref not in ids:
                    r.err(f"{subject}:{cid}", f"challenge touches unknown claim `{ref}`")

    def resolve(ref):
        """Return the claim for `subject:claim-id` (or a bare id) in this subject, or None.
        Members of other subjects are reported separately (cross-subject check not built yet)."""
        ref = str(ref)
        if ":" in ref:
            subj, cid = ref.split(":", 1)
            if subj != subject:
                return "other-subject"
            return ids.get(cid)
        return ids.get(ref)

    weighted_ids = set()   # thread and transmission ids, for the T2/X3 firewall

    tpath = os.path.join(sdir, "threads.yaml")
    thread_ids = set()
    if os.path.exists(tpath):
        d = load(tpath) or {}
        for t in d.get("threads") or []:
            tid = t.get("id")
            where = f"{subject}:{tid}"
            thread_ids.add(tid)
            if t.get("confers_weight") is not False:
                r.err(where, "threads must set `confers_weight: false`")
            for m in t.get("members") or []:
                ref = m.get("claim") if isinstance(m, dict) else m
                if ":" not in str(ref):
                    r.warn(where, f"member `{ref}`: write it as subject:claim-id (T1)")
                target = resolve(ref)
                if target == "other-subject":
                    r.warn(where, f"member `{ref}` is in another subject; cross-subject check not built yet")
                    continue
                if target is None:
                    r.err(where, f"member `{ref}` does not resolve to a claim (T1)")
                    continue
                if t.get("type") == "reception-overlay" and target.get("state") not in ("contested",) \
                        and target.get("evidence_class") != "interpretive":
                    r.err(where, f"reception-overlay member `{ref}` is `{target.get('state')}`; "
                                 "only contested or interpretive claims may be members (T4). "
                                 "Trace a settled myth in transmission.yaml instead")
        weighted_ids |= thread_ids

    # Transmission records (format proposed 2026-10-02, see build/SCHEMA.md): rules X1-X4.
    xpath = os.path.join(sdir, "transmission.yaml")
    chain_ids = set()
    if os.path.exists(xpath):
        d = load(xpath) or {}
        manifest = {}
        mpath = os.path.join(sdir, "sources", "MANIFEST.yaml")
        if os.path.exists(mpath):
            manifest = {s.get("id") for s in (load(mpath) or {}).get("sources") or []}
        for ch in d.get("chains") or []:
            cid = ch.get("id")
            where = f"{subject}:{cid}"
            chain_ids.add(cid)
            if ch.get("confers_weight") is not False:
                r.err(where, "transmission chains must set `confers_weight: false` (X1)")
            target = resolve(ch.get("about"))
            if target is None or target == "other-subject":
                r.err(where, f"`about: {ch.get('about')}` does not resolve to a claim in this subject (X4)")
            seen_events = set()
            for e in ch.get("events") or []:
                eid = e.get("id")
                if eid in seen_events:
                    r.err(where, f"duplicate event id `{eid}`")
                seen_events.add(eid)
                if not e.get("source"):
                    r.err(where, f"event `{eid}` names no source (X2)")
                elif manifest and e.get("source") not in manifest:
                    r.err(where, f"event `{eid}` source `{e.get('source')}` is not in sources/MANIFEST.yaml (X2)")
                if e.get("read") not in ("yes", "no", True, False):
                    r.err(where, f"event `{eid}` must say `read: yes` or `read: no` (X2)")
        weighted_ids |= chain_ids
        for tid in thread_ids:
            if tid in chain_ids:
                r.err(subject, f"id `{tid}` is used for both a thread and a transmission chain")

    # T2 / X3: synthesis and spread are never evidence. No claim may cite a thread or chain.
    for c in ids.values():
        anchor_text = yaml.safe_dump(c.get("anchor", "")) + yaml.safe_dump(c.get("anchors", ""))
        for wid in weighted_ids:
            if wid and wid in anchor_text:
                r.err(f"{subject}:{c.get('id')}", f"cites `{wid}` as an anchor; threads and "
                                                  "transmission chains confer no weight (T2/X3)")

    # Absence anchors are capped at provisional confidence (CONTRIBUTING.md section 2).
    for c in ids.values():
        if c.get("absence_anchor") and c.get("confidence") not in ("provisional", "low"):
            r.err(f"{subject}:{c.get('id')}", "absence anchor: confidence is capped at provisional")

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
                # Owner-approved redaction (SCHEMA N26): allowed only if a NEW entry names it in `redacts` and says why.
                redacted = any(lid in (x.get("redacts") or []) and x.get("id") not in old_entries for x in new_entries.values())
                if not redacted:
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


def check_publish_gate(r):
    sp = os.path.join(os.path.dirname(SUBJECTS), "site.yaml")
    if not os.path.exists(sp):
        return
    for s in (load(sp) or {}).get("publish") or []:
        rp = os.path.join(SUBJECTS, s, "review.yaml")
        if not os.path.exists(rp):
            r.err(f"publish-gate:{s}", "published subject has no review.yaml (docs/PUBLISH_GATE.md)")
            continue
        rv = load(rp) or {}
        st = rv.get("status")
        if st not in ("passed", "passed_with_open_items", "grandfathered"):
            r.err(f"publish-gate:{s}", f"review status `{st}` does not allow publishing")
        # Revision rounds (docs/PUBLISH_GATE.md): a blocking request must have an author response and a reviewer resolution before a pass.
        for rd in rv.get("rounds") or []:
            for q in rd.get("requests") or []:
                if q.get("severity") == "blocking" and st in ("passed", "passed_with_open_items") and (not q.get("author_response") or q.get("resolved") is not True):
                    r.err(f"publish-gate:{s}", f"round {rd.get('round')} request `{q.get('id')}` is blocking but has no author response or reviewer resolution")


def check_taxonomy(r, subjects):
    tp = os.path.join(os.path.dirname(SUBJECTS), "taxonomy.yaml")
    if not os.path.exists(tp):
        r.warn("taxonomy", "build/taxonomy.yaml is missing")
        return
    tx = load(tp) or {}
    areas, types, asg = tx.get("areas") or {}, tx.get("question_types") or {}, tx.get("assignments") or {}
    for sdir in subjects:
        s = os.path.basename(sdir)
        a = asg.get(s)
        if not a:
            r.warn("taxonomy", f"{s} has no entry in build/taxonomy.yaml (area and question types)")
            continue
        for k in [a.get("area")] + list(a.get("areas") or []):
            if k not in areas:
                r.err(f"taxonomy:{s}", f"unknown area `{k}`")
        for k in a.get("types") or []:
            if k not in types:
                r.err(f"taxonomy:{s}", f"unknown question type `{k}`")
        if not a.get("types"):
            r.warn(f"taxonomy:{s}", "no question type given")
    for s in asg:
        if not os.path.isdir(os.path.join(SUBJECTS, s)):
            r.warn("taxonomy", f"assignment for `{s}` has no subject folder")


def check_definitions(r):
    dd = os.path.join(os.path.dirname(SUBJECTS), "definitions")
    for f in sorted(glob.glob(os.path.join(dd, "*.yaml"))):
        did = os.path.basename(f)[:-5]
        d = load(f) or {}
        w = f"definition:{did}"
        if d.get("id") != did:
            r.err(w, "`id` must equal the file name")
        for k in ("label", "authority", "quoted", "from_bce", "to_bce", "via"):
            if d.get(k) in (None, ""):
                r.err(w, f"missing `{k}`")
        if isinstance(d.get("from_bce"), int) and isinstance(d.get("to_bce"), int) and d["from_bce"] < d["to_bce"]:
            r.err(w, "from_bce must not be later than to_bce (BCE years count down)")
        if d.get("authority_read_directly") is not True and not d.get("via"):
            r.err(w, "an authority not read directly must say how it was reached (`via`)")


def check_nodes(r):
    """Shared nodes (build/nodes/*.yaml): see SCHEMA.md, Nodes."""
    import hashlib, re
    ndir = os.path.join(os.path.dirname(SUBJECTS), "nodes")
    nodes = {}
    for f in sorted(glob.glob(os.path.join(ndir, "*.yaml"))):
        fid = os.path.basename(f)[:-5]
        try:
            n = load(f) or {}
        except yaml.YAMLError as e:
            r.err(f"node:{fid}", f"YAML does not parse: {e}")
            continue
        nodes[fid] = n
        w = f"node:{fid}"
        if n.get("id") != fid:
            r.err(w, "`id` must equal the file name")
        for k in ("rev", "type", "label", "time", "kind", "status", "what", "history"):
            if n.get(k) in (None, ""):
                r.err(w, f"missing `{k}`")
        if n.get("type") not in ("event", "document", "image", "recording", "dataset", "object"):
            r.err(w, f"unknown type `{n.get('type')}`")
        if n.get("status") not in ("single", "reported", "disputed", "inferred"):
            r.err(w, f"unknown status `{n.get('status')}`")
        if not re.match(r"^-?\d{4}-\d\d-\d\d", str(n.get("time", ""))):
            r.err(w, f"time `{n.get('time')}` is not ISO")
        if n.get("date_basis") not in ("stated", "derived", "publication_proxy", "inferred", "dataset_field"):
            r.warn(w, f"date_basis `{n.get('date_basis')}` missing or unknown (stated | derived | publication_proxy | inferred | dataset_field)")
        _srcs = n.get("sources") or []
        for s in _srcs:
            if not s.get("origin"):
                r.warn(w, f"source `{str(s.get('title'))[:40]}` has no `origin` (schema v0.5): independence cannot be counted")
            if s.get("source_type") not in (None, "primary_document", "official_record", "official_history", "dataset", "scholarly", "secondary_report", "news", "social_media", "testimony", "ai_generated", "unknown"):
                r.err(w, f"unknown source_type `{s.get('source_type')}`")
            if s.get("source_type") == "ai_generated" and len(_srcs) == 1:
                r.err(w, "an ai_generated source cannot be the only source of a node")
            if s.get("access") not in (None, "read", "cited_only"):
                r.err(w, "source `access` must be read or cited_only")
        if _srcs and all(s.get("origin") for s in _srcs):
            import sys as _s
            _s.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
            from nodes import assess
            a_ = assess(n)
            if n.get("status") == "reported" and a_["independent"] < 2:
                r.warn(w, f"status `reported` (2+ sources agree) but the sources trace to {a_['independent']} independent origin: they repeat one record")
            if n.get("status") == "single" and a_["independent"] >= 2:
                r.warn(w, f"status `single` but {a_['independent']} independent origins are declared")
        if not n.get("sources") and not n.get("source_gap"):
            r.err(w, "a node needs at least one source, or a stated `source_gap`")
        for s in n.get("sources") or []:
            if not s.get("title"):
                r.err(w, "a source has no title")
        h = n.get("history") or []
        if h and h[-1].get("rev") != n.get("rev"):
            r.err(w, "the last `history` entry must describe the current `rev` (append-only)")
        if n.get("derived_from") and not n.get("variant_reason"):
            r.err(w, "a variant (`derived_from`) must give `variant_reason`")
        m = (n.get("media") or {})
        if m.get("file"):
            fp = os.path.normpath(os.path.join(ndir, m["file"]))
            if not os.path.exists(fp):
                r.err(w, f"media file missing: {m['file']}")
            elif m.get("sha256") and hashlib.sha256(open(fp, "rb").read()).hexdigest() != m["sha256"]:
                r.err(w, "media sha256 does not match the file")
        wn = n.get("window")
        if wn:
            import sys as _s2
            _s2.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
            from nodes import iso_key
            e_, l_ = iso_key(wn.get("earliest")), (None if wn.get("latest") == "open" else iso_key(wn.get("latest")))
            if e_ is None or (wn.get("latest") != "open" and l_ is None):
                r.err(w, "window earliest/latest must be ISO dates (latest may be `open`)")
            else:
                if l_ is not None and e_ > l_:
                    r.err(w, "window earliest is after latest")
                tk = iso_key(n.get("time"))
                if tk and (tk < e_ or (l_ is not None and tk > l_)):
                    r.err(w, "node `time` lies outside its own window")
                cv = wn.get("certainly_covers")
                if cv:
                    f_, t_ = iso_key(cv.get("from")), iso_key(cv.get("to"))
                    if f_ is None or t_ is None or f_ > t_ or f_ < e_ or (l_ is not None and t_ > l_):
                        r.err(w, "certainly_covers must be a valid span inside the window")
            for k_ in ("begin_note", "end_note"):
                if not wn.get(k_):
                    r.err(w, f"window needs `{k_}`: the reason for that boundary")
            if wn.get("defined_by"):
                dd = {}
                for did in wn["defined_by"]:
                    dp = os.path.join(os.path.dirname(SUBJECTS), "definitions", did + ".yaml")
                    if not os.path.exists(dp):
                        r.err(w, f"window defined_by unknown definition `{did}`")
                    else:
                        dd[did] = load(dp)
                if dd and len(dd) == len(wn["defined_by"]):
                    e2 = max(d["from_bce"] for d in dd.values()); l2 = min(d["to_bce"] for d in dd.values())
                    c1 = min(d["from_bce"] for d in dd.values()); c2 = max(d["to_bce"] for d in dd.values())
                    if iso_key(wn.get("earliest"))[0] != -e2 or iso_key(wn.get("latest"))[0] != -l2:
                        r.err(w, f"window does not match its definitions (expected {e2} to {l2} BCE)")
                    cv = wn.get("certainly_covers") or {}
                    if c1 >= c2 and (iso_key(cv.get("from")) or (0,))[0] != -c1:
                        r.err(w, f"certainly_covers does not match the definitions' intersection ({c1} to {c2} BCE)")
        pl = n.get("place")
        if pl:
            if not pl.get("name"):
                r.err(w, "place needs a `name`")
            if pl.get("lat") is not None or pl.get("lon") is not None:
                if not (isinstance(pl.get("lat"), (int, float)) and -90 <= pl["lat"] <= 90 and isinstance(pl.get("lon"), (int, float)) and -180 <= pl["lon"] <= 180):
                    r.err(w, "place lat/lon out of range")
                if pl.get("precision") not in ("exact", "site", "city", "region"):
                    r.err(w, "place with coordinates needs `precision` (exact | site | city | region)")
                if not pl.get("source"):
                    r.err(w, "place with coordinates needs the `source` of the coordinates")
        mf = n.get("manifest")
        if mf:
            mp = os.path.join(SUBJECTS, mf["subject"], "sources", "MANIFEST.yaml")
            ids = {s.get("id") for s in (load(mp) or {}).get("sources", [])} if os.path.exists(mp) else set()
            if mf["source"] not in ids:
                r.err(w, f"manifest entry `{mf['source']}` not found in {mf['subject']}")
    for fid, n in nodes.items():
        for ref in n.get("about") or []:
            if ref not in nodes:
                r.err(f"node:{fid}", f"`about` refers to unknown node `{ref}`")
            elif nodes[ref].get("type") != "object":
                r.warn(f"node:{fid}", f"`about` node `{ref}` is not of type object")
        for ref in n.get("evidences") or []:
            if ref not in nodes:
                r.err(f"node:{fid}", f"`evidences` refers to unknown node `{ref}`")
        for rel in n.get("related") or []:
            w = f"node:{fid}"
            if isinstance(rel, str):
                r.warn(w, f"related link to `{rel}` has no grade and reason (schema v0.5)")
                rel = {"node": rel}
            else:
                if rel.get("grade") not in ("established", "possible"):
                    r.err(w, f"related link to `{rel.get('node')}`: grade must be established or possible")
                if not rel.get("why"):
                    r.err(w, f"related link to `{rel.get('node')}` needs a `why`")
                if rel.get("kind") not in ("same_event", "part_of", "summarises", "overlaps", "responds_to"):
                    r.err(w, f"related link to `{rel.get('node')}`: unknown kind `{rel.get('kind')}`")
            if rel.get("node") not in nodes:
                r.err(w, f"`related` refers to unknown node `{rel.get('node')}`")
        if n.get("derived_from") and n["derived_from"] not in nodes:
            r.err(f"node:{fid}", f"derived_from unknown node `{n['derived_from']}`")
    for fid, n in nodes.items():
        m = n.get("media") or {}
        if m.get("thumb"):
            tp_ = os.path.normpath(os.path.join(ndir, m["thumb"]))
            if not os.path.exists(tp_):
                r.err(f"node:{fid}", f"thumbnail missing: {m['thumb']}")
            elif m.get("thumb_sha256") and hashlib.sha256(open(tp_, "rb").read()).hexdigest() != m["thumb_sha256"]:
                r.err(f"node:{fid}", "thumbnail sha256 does not match the file")
        if m.get("file") and m.get("rights") not in ("public_domain", "thumbnail_only", "licensed", "unknown"):
            r.warn(f"node:{fid}", "media has no `rights` status (public_domain | thumbnail_only | licensed | unknown)")
    for sdir in sorted(glob.glob(os.path.join(SUBJECTS, "*"))):
        cp_ = os.path.join(sdir, "claims.yaml")
        if os.path.exists(cp_):
            for c in (load(cp_) or {}).get("claims", []):
                for ref in ((c.get("anchor") or {}).get("nodes") or []) if isinstance(c.get("anchor"), dict) else []:
                    if isinstance(ref, dict):
                        if ref.get("verb") not in ("supports", "disputes", "refutes", "qualifies", "confirms", "corrects", "extends"):
                            r.err(f"{os.path.basename(sdir)}:{c.get('id')}", f"anchor node `{ref.get('node')}` has unknown verb `{ref.get('verb')}`")
                        ref = ref.get("node")
                    if ref not in nodes:
                        r.err(f"{os.path.basename(sdir)}:{c.get('id')}", f"anchor refers to unknown node `{ref}`")
    for sdir in sorted(glob.glob(os.path.join(SUBJECTS, "*"))):
        tp = os.path.join(sdir, "timeline.yaml")
        if not os.path.exists(tp):
            continue
        sub = os.path.basename(sdir)
        for e in (load(tp) or {}).get("events", []):
            nid = e.get("node")
            if not nid:
                continue
            if nid not in nodes:
                r.err(sub, f"timeline event {e.get('id')} refers to unknown node `{nid}`")
            elif e.get("rev") is not None and e["rev"] < nodes[nid].get("rev", 1):
                r.warn(sub, f"timeline event {e.get('id')} was written against rev {e['rev']} of node `{nid}`; it is now rev {nodes[nid]['rev']}: re-read and update the pin")
    return nodes


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
    check_taxonomy(r, subjects)
    check_publish_gate(r)
    check_definitions(r)
    nodes = check_nodes(r)
    if args.base:
        check_history(r, args.base)

    for w in r.warnings:
        print(f"WARNING  {w}")
    for e in r.errors:
        print(f"ERROR    {e}")
    print(f"\n{len(subjects)} subjects and {len(nodes)} shared nodes checked: {len(r.errors)} errors, {len(r.warnings)} warnings")
    sys.exit(1 if r.errors else 0)


if __name__ == "__main__":
    main()
