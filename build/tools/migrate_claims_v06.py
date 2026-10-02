#!/usr/bin/env python3
"""One-off schema v0.6 migration of the claims of the four published excavations (run once). Text edits only, so comments in claims.yaml survive.
Adds to every claim: statement_kind (assigned by rule, to be reviewed). Adds by hand to the headline and contested claims: assumptions, alternatives,
confidence_reasons, disputed_by. Converts `anchor.nodes` lists to {node, verb} mappings."""
import os, re, sys, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUBS = ("gulf-of-tonkin", "mcafee-and-surfside", "eikon-basilike", "casket-letters")

def kind_of(c):
    st = c["state"]
    s = " ".join(str(c["statement"]).split())
    if st == "searched_gap":
        return "search_result"
    if st == "established" and (re.search(r'"|“', s) or re.search(r"\b(told|said|wrote|charged|announced|records?|printed|voted|passed|states?|stated|says)\b", s)):
        return "reported"
    return "judgment"

EXTRA = {
 "tonkin-aug4-attack-occurred": """    assumptions:
      - text: "The declassified intercept reports, read through Hanyok's study, are complete enough that no unreleased 4 August material shows an attack."
        if_wrong: "New intercepts, ship logs or North Vietnamese records showing boats present and firing on 4 August would reopen the claim."
      - text: "Hanyok's re-analysis of the intercepts is sound. We read it and the reports but did not repeat his analysis."
        if_wrong: "A reanalysis showing that Reports 7, 12 or 13 do describe an attack on the ships would weaken the refutation."
    alternatives:
      - text: "An attack took place but left no trace in the signals intelligence."
        why_not_preferred: "Hanyok, with 122 relevant SIGINT products, concludes 'no attack happened that night' (read), and no source read shows one."
      - text: "The key after-action report did concern 4 August."
        why_not_preferred: "Its original decrypted Vietnamese text and translation cannot be located (claim tonkin-original-text-missing), so it cannot be tested either way."
    confidence_reasons:
      start: high
      start_because: "The anchor was read directly (primary)."
      steps:
        - {domain: risk_of_bias, effect: none, reason: "Hanyok writes from NSA's own records against his own institution's earlier account, and the intercept reports themselves were read. The weight rests largely on his re-analysis, which we did not repeat."}
        - {domain: unreported_negative_results, effect: none, reason: "The original text of the key after-action report cannot be located. Considered and not applied because the other reports read do not describe an attack on the ships. Watch this one."}
        - {domain: independent_corroboration, effect: none, reason: "Giap's account (via Prados, secondary) agrees; counted as corroboration only, not as a basis."}
      reviewed: false
""",
 "surfside-deliberate-timed-to-mcafee": """    assumptions:
      - text: "NIST's account of the failure, read in its public summary pages and not in the full technical report, is accurate and complete enough to rule out a separate deliberate cause."
        if_wrong: "Evidence of sabotage or an external cause, or a link between McAfee or his data and the building, would change the claim. The summary read does not say whether sabotage was specifically tested and excluded."
    alternatives:
      - text: "The collapse was deliberate and its timing was a coincidence."
        why_not_preferred: "NIST finds the failure began in early June 2021 at two connections, with causes in the original design and construction, and no source read shows a deliberate act."
    confidence_reasons:
      start: high
      start_because: "The anchor was read directly (primary)."
      steps:
        - {domain: indirectness, effect: none, reason: "Only NIST's public pages were read, not the technical report. Considered and not applied because the claim is a conjunction, and the dates alone (failure began before the death) refute 'timed to follow McAfee's death'."}
      reviewed: false
""",
 "eikon-milton-pamela-charge": """    assumptions:
      - text: "The EEBO-TCP transcription of Eikonoklastes (A50898) reproduces the printed passages faithfully."
        if_wrong: "A different reading of the printed wording; the quotation would need re-checking against the page images."
    alternatives:
      - text: "The charge first appeared in the 1650 second edition and not in 1649."
        why_not_preferred: "Not excluded: the edition read is the 1650 second edition and the first edition was not read. This is the condition in would_change_if."
    confidence_reasons:
      start: high
      start_because: "The anchor was read directly (primary)."
      steps:
        - {domain: indirectness, effect: none, reason: "The claim says Milton made the charge in Eikonoklastes, which the text read shows. It does not claim the charge is true or that it appeared in 1649."}
      reviewed: false
""",
 "casket-originals-lost": """    assumptions:
      - text: "That no original has been traced since the 1580s means they are lost and not merely unrecognised."
        if_wrong: "An original surfacing and being authenticated would change the claim."
    alternatives:
      - text: "An original survives, unrecognised, in a private or archival collection."
        why_not_preferred: "No source read reports one. The claim rests on absence, so it is held at provisional confidence."
    confidence_reasons:
      start: moderate
      start_because: "The anchor was checked against a secondary source (Henderson 1889, read in OCR)."
      steps:
        - {domain: unreported_negative_results, effect: down1, reason: "The claim rests on the absence of any traced original, which cannot prove absence."}
        - {domain: indirectness, effect: down1, reason: "The account is from 1889. No modern holdings or catalogues were checked."}
      reviewed: false
""",
 "casket-authenticity-contested": """    disputed_by:
      - {who: "T. F. Henderson", kind: person, position: "argues the letters are genuine", source_read: true, via: "Henderson 1889 (read in OCR); he is an advocate for genuineness, so his judgements are not independent evidence"}
      - {who: "National Museums Scotland", kind: institution, position: "says it is 'widely thought' the letters were doctored", source_read: false, via: "quoted in this claim's adoption note; not read here"}
""",
 "eikon-charles-wrote-book": """    disputed_by:
      - {who: "John Gauden", kind: person, position: "claimed after the Restoration that he wrote it (claim eikon-gauden-claimed-authorship)", source_read: false, via: "the Q-002 page; Gauden's letters were not read here"}
""",
 "tonkin-senior-knowledge": """    disputed_by:
      - {who: "historians, not named in the sources read", kind: unnamed, position: "divided on what senior officials knew", source_read: false, via: "this claim's adoption note"}
""",
}
CR_ONLY = {}

def convert_nodes(text):
    def sub(m):
        ids = [x.strip() for x in m.group(2).split(",")]
        verb = "disputes" if False else "supports"
        return m.group(1) + "nodes:\n" + "".join(f"{m.group(1)}  - {{node: {i}, verb: __VERB__}}\n" for i in ids).rstrip("\n")
    return re.sub(r"^( +)nodes: \[([^\]]+)\]$", sub, text, flags=re.M)

def main():
    for s in SUBS:
        p = os.path.join(ROOT, "build", "subjects", s, "claims.yaml")
        t = open(p, encoding="utf-8").read()
        C = yaml.safe_load(t)
        byid = {c["id"]: c for c in C["claims"]}
        out, lines, cur = [], t.split("\n"), None
        for l in lines:
            m = re.match(r"^  - id: (\S+)", l)
            if m:
                cur = m.group(1)
            out.append(l)
            if cur in byid and re.match(r"^    confidence: ", l):
                c = byid[cur]
                out.append(f"    statement_kind: {kind_of(c)}   # assigned by rule 2026-10-02, to be reviewed")
                if cur in EXTRA:
                    out.extend(EXTRA[cur].rstrip("\n").split("\n"))
                    EXTRA.pop(cur)
        t2 = "\n".join(out)
        t2 = convert_nodes(t2)
        # verb: refutation evidence disputes the statement, everything else supports it
        def fix(blockm):
            blk = blockm.group(0)
            return blk.replace("__VERB__", "disputes" if "state: refuted" in blk else "supports")
        t2 = re.sub(r"(?ms)^  - id: .*?(?=^  - id: |\Z)", fix, t2)
        open(p, "w", encoding="utf-8").write(t2)
    print("unused EXTRA:", list(EXTRA))

if __name__ == "__main__":
    main()
