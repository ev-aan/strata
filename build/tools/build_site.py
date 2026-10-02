#!/usr/bin/env python3
"""Assemble the public site into site/ from the repository. YAML is the source of truth; pages are generated.

Usage: python3 build/tools/build_site.py [outdir=site]

Includes: the existing homepage, method page and open-question pages (copied as they are), plus generated pages for each dig listed
under `publish` in build/site.yaml: /digs/ (index), /digs/<slug>/ (article), its timeline, its claims.yaml and sources manifest,
/corrections/ (every logged correction of a published dig) and /about/. Digs not listed are not published."""
import os, sys, shutil, html, re, json, datetime, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, sys.argv[1] if len(sys.argv) > 1 else "site")
CFG = yaml.safe_load(open(os.path.join(ROOT, "build", "site.yaml")))
E = lambda s: html.escape(str(s if s is not None else ""))
TODAY = datetime.date.today().isoformat()

CSS = """:root{--sand:#F5F2EC;--sand2:#EAE5DC;--ink:#1A1814;--mid:#4A4640;--mute:#6f6962;--amber:#8B6914;--amber-l:#F5EDD5;--teal:#0F6E56;--teal-l:#E1F5EE;--coral:#993C1D;--coral-l:#FAECE7;--line:rgba(26,24,20,.14);--card:#fff}
@media (prefers-color-scheme:dark){:root{--sand:#16150f;--sand2:#201e17;--ink:#ece8de;--mid:#c3beb2;--mute:#a09a8d;--amber:#d9b45a;--amber-l:#2c2512;--teal:#5ccaa5;--teal-l:#10261f;--coral:#ee9372;--coral-l:#30190f;--line:rgba(236,232,222,.16);--card:#1d1b14}}
*{box-sizing:border-box}body{margin:0;background:var(--sand);color:var(--ink);font:17px/1.65 'Fraunces',Georgia,serif}
.w{max-width:780px;margin:0 auto;padding:0 20px 64px}nav{display:flex;gap:22px;flex-wrap:wrap;align-items:baseline;padding:22px 0;border-bottom:1px solid var(--line);margin-bottom:34px;font:12px 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase}
nav a{color:var(--mute);text-decoration:none}nav a.b{color:var(--ink);font:500 17px Georgia,serif;letter-spacing:.1em}a{color:var(--teal)}
h1{font-weight:400;font-size:clamp(28px,5vw,42px);line-height:1.15;letter-spacing:-.01em;margin:.2em 0 .5em}h2{font-weight:500;font-size:22px;margin:2em 0 .5em;border-bottom:1px solid var(--line);padding-bottom:6px}
.eyebrow,.mono{font:12px 'IBM Plex Mono',ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--mute)}
.banner{background:var(--amber-l);border:1px solid var(--line);border-radius:8px;padding:10px 14px;font-size:15px;margin:14px 0}.summary{font-size:20px;color:var(--mid);font-weight:300}
.claim{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:12px 0}.claim p{margin:.3em 0}
.pill{display:inline-block;font:11.5px 'IBM Plex Mono',ui-monospace,monospace;border:1px solid currentColor;border-radius:99px;padding:1px 9px}
.s-established{color:var(--teal)}.s-refuted{color:var(--coral)}.s-contested,.s-proposed{color:var(--amber)}.s-searched_gap{color:var(--mute)}
.meter{display:grid;grid-template-columns:130px 1fr;gap:2px 10px;font:12px 'IBM Plex Mono',ui-monospace,monospace;color:var(--mute);margin:8px 0}.dots{letter-spacing:3px;color:var(--ink)}
details summary{cursor:pointer;color:var(--mute);font-size:14px}details p{font-size:15px;color:var(--mid)}small,.small{font-size:14px;color:var(--mute)}
ul.l{list-style:none;padding:0}ul.l li{padding:12px 0;border-top:1px solid var(--line)}footer{margin-top:50px;padding-top:16px;border-top:1px solid var(--line);font-size:14px;color:var(--mute)}"""

def page(title, body, desc="", canonical="", extra_head="", depth=0):
    up = "../" * depth
    nav = (f'<nav><a class="b" href="{up}">{E(CFG["name"])}</a><a href="{up}digs/">Active Excavations</a><a href="{up}method/">Method</a>'
           f'<a href="{up}atlas/">Atlas</a><a href="{up}ideas/">Ideas</a><a href="{up}corrections/">Corrections</a><a href="{up}about/">About</a></nav>')
    meta = f'<meta name="description" content="{E(desc)}">' if desc else ""
    og = (f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">'
          f'<meta property="og:type" content="article"><meta property="og:site_name" content="{E(CFG["name"])}">'
          + (f'<meta property="og:url" content="https://{CFG["domain"]}{canonical}">' if canonical else ""))
    can = f'<link rel="canonical" href="https://{CFG["domain"]}{canonical}">' if canonical else ""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{E(title)}{"" if title.startswith(CFG["name"]) or len(title) > 70 else " | " + E(CFG["name"])}</title>{meta}{can}{og}{extra_head}<link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@300;400;500&family=IBM+Plex+Mono&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body><div class="w">{nav}{body}'
            f'<footer>Built {TODAY} from YAML in the repository. <a href="{E(CFG["source_url"])}">Source</a> · '
            f'<a href="{E(CFG["issues_url"])}">Challenge a finding</a></footer></div></body></html>')

def write(rel, text):
    p = os.path.join(OUT, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(text)

def dots(n): n = int(n or 0); return "●" * n + "○" * (5 - n)

def claim_html(c):
    st = c.get("state", "")
    an = c.get("anchor") or {}
    desc = an.get("description") if isinstance(an, dict) else ""
    chk = c.get("anchor_checked")
    chk = "no" if chk is False else chk
    nxt = c.get("next_step")
    bits = f'<p><span class="pill s-{E(st)}">{E("refuted: the claim below is false" if st == "refuted" else st.replace("_", " "))}</span> <span class="small">confidence {E(c.get("confidence", "n/a"))}{(" · " + {"reported": "what a source says", "judgment": "our conclusion", "assumption": "an assumption", "search_result": "result of a search"}.get(c.get("statement_kind"), "")) if c.get("statement_kind") else ""}</span></p>'
    bits += f'<p>{E(" ".join(str(c.get("statement", "")).split()))}</p>'
    bits += (f'<div class="meter"><span>Evidence</span><span class="dots">{dots(c.get("evidential_weight"))}</span>'
             f'<span>Public belief</span><span class="dots">{dots(c.get("adoption_weight"))}</span><span>Source checked</span><span>{E(chk)}</span></div>')
    more = ""
    if desc: more += f'<p><b>Anchor.</b> {E(" ".join(str(desc).split()))}</p>'
    if c.get("would_change_if"): more += f'<p><b>Would change if.</b> {E(" ".join(str(c["would_change_if"]).split()))}</p>'
    if nxt: more += f'<p><b>Next step.</b> {E(" ".join(str(nxt).split()))}</p>'
    nl = an.get("nodes") if isinstance(an, dict) else None
    if nl: more += '<p><b>Evidence nodes</b> <span class="small">(what each does to the statement above)</span></p><ul class="l" style="overflow:auto">' + "".join(node_html(x["node"], x.get("verb", "")) if isinstance(x, dict) else node_html(x) for x in nl) + '</ul>'
    if c.get("assumptions"): more += '<p><b>Assumptions this rests on.</b></p><ul class="l">' + "".join(f'<li>{E(a["text"])}<br><span class="small">If wrong: {E(a["if_wrong"])}</span></li>' for a in c["assumptions"]) + '</ul>'
    if c.get("alternatives"): more += '<p><b>Alternatives considered.</b></p><ul class="l">' + "".join(f'<li>{E(a["text"])}<br><span class="small">Why not preferred: {E(a["why_not_preferred"])}</span></li>' for a in c["alternatives"]) + '</ul>'
    cr = c.get("confidence_reasons")
    if cr:
        more += f'<p><b>Why this confidence.</b> Starts at <b>{E(cr["start"])}</b> ({E(str(cr.get("start_because", "")).rstrip("."))}).</p><ul class="l">' + "".join(
            f'<li><span class="pill">{E(s["domain"].replace("_", " "))}: {E({"none": "no change", "down1": "down one", "down2": "down two", "up1": "up one"}[s["effect"]])}</span> {E(s["reason"])}</li>' for s in cr["steps"]) + '</ul>' + ('<p class="small">These reasons were drafted by the project and have not yet been reviewed.</p>' if not cr.get("reviewed") else "")
    if c.get("disputed_by"): more += '<p><b>Disputed by.</b></p><ul class="l">' + "".join(f'<li>{E(d["who"])}: {E(d["position"])}<br><span class="small">{E(d["via"])}{"" if d.get("source_read") else " (source not read here)"}</span></li>' for d in c["disputed_by"]) + '</ul>'
    if more: bits += f'<details><summary>Evidence and limits</summary>{more}</details>'
    return f'<div class="claim" id="{E(c.get("id"))}">{bits}</div>'

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nodes as _nodes
NODES = _nodes.load_nodes()
CUR = {"slug": ""}
ASSESS = {}
TAX = yaml.safe_load(open(os.path.join(ROOT, "build", "taxonomy.yaml")))
AREAS, QTYPES = TAX["areas"], TAX["question_types"]
META = {}   # slug -> {sub, area, areas, types, popular}


def node_html(nid, verb=""):
    n = NODES.get(nid)
    if not n: return ""
    m = n.get("media") or {}
    srcs = " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["title"])}</a>' if s.get("url") else E(s["title"]) for s in (n.get("sources") or [])[:2])
    img = ""
    if m.get("thumb"):
        fn = os.path.basename(m["thumb"])
        os.makedirs(os.path.join(OUT, "digs", CUR["slug"], "media"), exist_ok=True)
        shutil.copy(os.path.join(_nodes.NODES_DIR, m["thumb"]), os.path.join(OUT, "digs", CUR["slug"], "media", fn))
        orig = m.get("original_url") or ""
        tag = f'<img src="media/{E(fn)}" alt="{E(n["label"])}" loading="lazy" style="max-width:220px;border:1px solid var(--line);border-radius:6px;float:right;margin:0 0 6px 12px">'
        img = f'<a href="{E(orig)}" target="_blank" rel="noopener">{tag}</a>' if orig else tag
    return (f'<li>{img}{("<span class=pill>" + E(verb) + "</span> ") if verb else ""}<b>{E(n["label"])}</b> <span class="small">· {E(str(n["time"])[:10])} · {E(n["type"])} · node {E(nid)} rev {E(n["rev"])}</span>'
            f'<br><span class="small">{srcs}</span></li>')

ANS = {"yes": "Yes", "no": "No", "leans_yes": "Leans yes", "leans_no": "Leans no", "unsettled": "Unsettled", "partly": "Partly"}

def short_line(v, claims=None):
    """The short answer, for example 'Unsettled, leans slightly toward yes' or 'No (high confidence)'."""
    rc = (claims or {}).get(v.get("rated_claim") or (v.get("basis") or [None])[0])
    line = ANS.get(v["answer"], v["answer"])
    if v.get("lean"):
        line += f', leans {v["lean"]["strength"]}ly toward {v["lean"].get("short") or v["lean"]["toward"]}'
    elif v["answer"] in ("yes", "no") and rc and rc.get("confidence"):
        line += f' ({rc["confidence"]} confidence)'
    return line


def assessment_html(v, slug, prefix="", show_question=True, claims=None):
    """Executive summary first: the answer, three key points, the ratings of the central claim and what would settle it. The reasoning folds underneath.
    No percentages: see SCHEMA N23."""
    if not v: return ""
    cls = {"yes": "s-established", "no": "s-refuted", "unsettled": "s-contested", "partly": "s-contested"}.get(v["answer"], "s-contested")
    links = " ".join(f'<a href="{prefix}digs/{E(slug)}/#{E(c)}">{E(c)}</a>' for c in v.get("basis", []))
    kp = "".join(f"<li>{E(x)}</li>" for x in v.get("key_points", []))
    rc = (claims or {}).get(v.get("rated_claim") or (v.get("basis") or [None])[0])
    rate = ""
    if rc:
        rate = (f'<p class="small" style="margin:6px 0 10px"><b>Central claim:</b> {E(" ".join(str(rc["statement"]).split())[:140])}'
                f'<br>Evidence <span class="dots">{dots(rc.get("evidential_weight"))}</span> &nbsp; Public belief <span class="dots">{dots(rc.get("adoption_weight"))}</span>'
                f' &nbsp; Source checked: {E(rc.get("anchor_checked") if rc.get("anchor_checked") is not False else "no")}</p>')
    lean = ""
    if v.get("lean"):
        lean = f'<p><b>Which way the evidence leans:</b> {E(v["lean"]["strength"])}ly toward <b>{E(v["lean"]["toward"])}</b>. This is not a finding.</p>'
    more = (f'<p>{E(" ".join(str(v["text"]).split()))}</p>'
            + (f'<p>{E(v["lean"]["because"])}</p><p class="small"><b>Why the lean is not a finding.</b> {E(v["lean"]["caveats"])}</p>' if v.get("lean") else "")
            + f'<p class="small">Based on: {links}</p>'
            + '<p class="small">We give no probability figure. Confidence words describe how sure we are of the basis, and no source supplies a number that would not be invented.</p>')
    line = short_line(v, claims)
    strip = (f'<p class="eyebrow" style="margin:18px 0 0">The short answer</p>'
             f'<p style="font-size:clamp(28px,6vw,40px);line-height:1.15;margin:2px 0 16px;font-weight:400;color:var(--ink)">{E(line)}</p>')
    return (strip + f'<section class="claim" style="border:1px solid var(--line);border-left:7px solid var(--amber);padding:18px 20px" id="where-it-stands"><h2 style="font-size:30px;border:0;margin:0 0 2px;padding:0">Where it stands</h2>'
            f'<p class="eyebrow" style="margin:0 0 12px">Current assessment · as of {TODAY}</p>{("<p><b>" + E(v["question"]) + "</b></p>") if show_question else ""}'
            f'<p style="font-size:21px;line-height:1.4;margin:6px 0 10px"><b>{E(v["headline"])}</b></p>'
            f'<ul style="margin:0 0 8px;padding-left:20px">{kp}</ul>{lean}{rate}'
            f'<p class="small"><b>What would settle it.</b> {E(v["would_settle"])}</p>'
            f'<details><summary>The full reasoning</summary>{more}</details></section>')

order = {"refuted": 0, "established": 1, "contested": 2, "proposed": 3, "searched_gap": 4}
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
# existing pages and files, copied unchanged
for f in ("index.html", "CNAME"):
    if os.path.exists(os.path.join(ROOT, f)): shutil.copy(os.path.join(ROOT, f), OUT)
for d in ("method", "questions"):
    if os.path.isdir(os.path.join(ROOT, d)): shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
open(os.path.join(OUT, ".nojekyll"), "w").close()
# the open-question pages used to live under /bounties/: leave redirects so old links keep working
for _q in sorted(os.listdir(os.path.join(ROOT, "questions"))) if os.path.isdir(os.path.join(ROOT, "questions")) else []:
    if os.path.isdir(os.path.join(ROOT, "questions", _q)):
        os.makedirs(os.path.join(OUT, "bounties", _q), exist_ok=True)
        open(os.path.join(OUT, "bounties", _q, "index.html"), "w", encoding="utf-8").write(
            f'<!doctype html><meta charset="utf-8"><title>Moved</title><meta http-equiv="refresh" content="0; url=../../questions/{_q}/">'
            f'<link rel="canonical" href="https://{CFG["domain"]}/questions/{_q}/"><p>This page moved to <a href="../../questions/{_q}/">/questions/{_q}/</a>.</p>')
os.makedirs(os.path.join(OUT, "bounties"), exist_ok=True)
open(os.path.join(OUT, "bounties", "index.html"), "w", encoding="utf-8").write(
    f'<!doctype html><meta charset="utf-8"><title>Moved</title><meta http-equiv="refresh" content="0; url=../#questions"><link rel="canonical" href="https://{CFG["domain"]}/#questions"><p>These pages are now <a href="../#questions">open questions</a>.</p>')

digs, corrections, urls = [], [], ["/", "/digs/", "/atlas/", "/ideas/", "/method/", "/corrections/", "/about/"]
for sub in CFG["publish"]:
    base = os.path.join(ROOT, "build", "subjects", sub)
    cl = yaml.safe_load(open(os.path.join(base, "claims.yaml")))
    slug = cl.get("url_slug") or sub
    CUR["slug"] = slug
    head = cl.get("headline") or cl.get("title")
    status = cl.get("headline_status", "draft")
    byid = {c["id"]: c for c in cl["claims"]}
    hc = byid.get(cl.get("headline_claim"))
    srcs = []
    mp = os.path.join(base, "sources", "MANIFEST.yaml")
    if os.path.exists(mp): srcs = yaml.safe_load(open(mp)).get("sources", [])
    has_tl = os.path.exists(os.path.join(base, "timeline.html"))
    n = {}
    for c in cl["claims"]: n[c.get("state")] = n.get(c.get("state"), 0) + 1
    tally = ", ".join(f"{v} {k.replace('_', ' ')}" for k, v in sorted(n.items(), key=lambda kv: order.get(kv[0], 9)))
    banner = (f'<div class="banner"><b>Open excavation.</b> This question is still being worked. The headline finding is stated at the confidence shown below; '
              f'not every source has been read in full, and each claim says which. Claims so far: {E(tally)}.</div>' if status != "published" else "")
    _a = TAX["assignments"].get(sub, {})
    META[slug] = {"question": (cl.get("assessment") or {}).get("question"), "short": short_line(cl["assessment"], {c["id"]: c for c in cl["claims"]}) if cl.get("assessment") else "", "sub": sub, "area": _a.get("area"), "areas": _a.get("areas", []), "types": _a.get("types", []), "popular": bool(_a.get("popular_claims"))}
    _tags = ""
    if _a.get("area"):
        _tags = (f'<p class="small">Area: <a href="../../areas/{E(_a["area"])}/">{E(AREAS[_a["area"]]["name"])}</a>'
                 + "".join(f' · <a href="../../areas/{E(x)}/">{E(AREAS[x]["name"])}</a>' for x in _a.get("areas", []))
                 + " · Question: " + ", ".join(E(QTYPES[x]["name"]) for x in _a.get("types", []))
                 + (" · Starts from a widely shared claim" if _a.get("popular_claims") else "") + "</p>")
    _as = cl.get("assessment")
    body = (f'<p class="eyebrow">Excavation · {E(cl.get("title"))}</p><h1>{E(_as["question"] if _as else head)}</h1>{_tags}'
            + assessment_html(_as, slug, show_question=False, claims={c["id"]: c for c in cl["claims"]}) + banner
            + ("" if _as else f'<p class="summary">{E(" ".join(str(cl.get("search_summary", "")).split()))}</p>'))
    ASSESS[sub] = (cl.get("assessment"), slug, {c["id"]: c for c in cl["claims"]})
    if hc: body += f'<h2>The headline finding</h2>{claim_html(hc)}'
    body += f'<p>{E(" ".join(str(cl.get("description", "")).split()))}</p>'
    if cl.get("divergence_note"): body += f'<h2>Where evidence and belief differ</h2><p>{E(" ".join(str(cl["divergence_note"]).split()))}</p>'
    if has_tl: body += '<h2>Timeline</h2><p>Every point on the timeline links to its source. <a href="timeline/">Open the timeline</a>.</p>'
    chp = os.path.join(base, "challenges.yaml")
    if os.path.exists(chp):
        chs = yaml.safe_load(open(chp)).get("challenges", [])
        lab = {"answered": "answered: finding stands", "partly_answered": "partly answered", "open": "open: not yet testable", "finding_changed": "finding changed"}
        body += ('<h2>Challenges addressed</h2><p>Objections raised against this excavation, in the form people raise them, with the test we ran and where it stands. '
                 'Open ones are shown as plainly as answered ones. Have one we missed? <a href="' + E(CFG["issues_url"]) + '">Send it</a>.</p>')
        for ch in chs:
            ref = " ".join(f'<a href="#{E(x)}">{E(x)}</a>' for x in ch.get("touches") or [])
            body += (f'<div class="claim"><p><b>{E(ch["challenge"])}</b></p><p><span class="pill s-{"established" if ch["result"] == "answered" else "contested"}">{E(lab[ch["result"]])}</span> '
                     f'<span class="small">raised by: {E(ch["raised_by"])}</span></p><p>{E(" ".join(str(ch["answer"]).split()))}</p>'
                     f'<details><summary>Test and claims</summary><p>{E(ch["test"])}</p>{("<p>" + ref + "</p>") if ref else ""}</details></div>')
    body += '<h2>All claims</h2>' + "".join(claim_html(c) for c in sorted(cl["claims"], key=lambda c: order.get(c.get("state"), 9)))
    if srcs:
        body += '<h2>Sources</h2><ul class="l">'
        for s in srcs:
            a = s.get("authenticity") or {}
            st = a.get("status", "") if isinstance(a, dict) else a
            u = s.get("url", "")
            body += f'<li>{("<a href=" + chr(34) + E(u) + chr(34) + ">") if u else ""}{E(s.get("title"))}{"</a>" if u else ""} <span class="small">· authenticity: {E(st)}</span></li>'
        body += '</ul>'
    body += f'<h2>The data</h2><p>These pages are generated from plain YAML: <a href="claims.yaml">claims.yaml</a>' + (' · <a href="MANIFEST.yaml">sources manifest</a>' if srcs else "") + '. If you can show a finding is wrong, <a href="' + E(CFG["issues_url"]) + '">challenge it</a>.</p>'
    summ = " ".join(str(cl.get("search_summary", "")).split())
    ld = '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": head, "description": summ,
         "inLanguage": "en", "dateModified": TODAY, "isAccessibleForFree": True, "url": f"https://{CFG['domain']}/digs/{slug}/",
         "mainEntityOfPage": f"https://{CFG['domain']}/digs/{slug}/", "about": cl.get("title"), "keywords": [AREAS[x]["name"] for x in ([META[slug]["area"]] + META[slug]["areas"]) if x] + [QTYPES[x]["name"] for x in META[slug]["types"]],
         "publisher": {"@type": "Organization", "name": CFG["name"], "url": f"https://{CFG['domain']}/"}}).replace("</", "<\\/") + '</script>'
    write(f"digs/{slug}/index.html", page(head, body, " ".join(str(cl.get("search_summary", "")).split()), f"/digs/{slug}/", ld, depth=2))
    shutil.copy(os.path.join(base, "claims.yaml"), os.path.join(OUT, "digs", slug, "claims.yaml"))
    if srcs: shutil.copy(mp, os.path.join(OUT, "digs", slug, "MANIFEST.yaml"))
    if has_tl:
        os.makedirs(os.path.join(OUT, "digs", slug, "timeline"), exist_ok=True)
        shutil.copy(os.path.join(base, "timeline.html"), os.path.join(OUT, "digs", slug, "timeline", "index.html"))
        shutil.copy(os.path.join(base, "timeline.yaml"), os.path.join(OUT, "digs", slug, "timeline", "timeline.yaml"))
    digs.append((slug, head, cl.get("search_summary", ""), status))
    urls.append(f"/digs/{slug}/")
    if has_tl: urls.append(f"/digs/{slug}/timeline/")
    lp = os.path.join(base, "log.yaml")
    if os.path.exists(lp):
        for e in yaml.safe_load(open(lp)).get("log", []):
            txt = " ".join(str(e.get("entry", "")).split())
            for m in re.finditer(r"CORRECTION[^.]*\.(?:[^.]*\.){0,2}", txt):
                corrections.append((str(e.get("date", "")), sub, slug, head, m.group(0).strip()))

def _li(s, h, sm, st):
    m = META.get(s, {})
    areas_all = [x for x in ([m.get("area")] + m.get("areas", [])) if x]
    tag = (f'<br><span class="small">{E(AREAS[m["area"]]["name"])} · ' + ", ".join(E(QTYPES[x]["name"]) for x in m.get("types", [])) + (" · starts from a widely shared claim" if m.get("popular") else "") + "</span>") if m.get("area") else ""
    return (f'<li data-areas="{" ".join(areas_all)}" data-types="{" ".join(m.get("types", []))}" data-popular="{1 if m.get("popular") else 0}"><a href="{E(s)}/"><b>{E(m.get("question") or h)}</b></a>{("<br>" + E(m["short"])) if m.get("short") else ""}{tag}{"" if m.get("short") else "<br><span class=small>" + E(" ".join(str(sm).split())) + "</span>"}'
            f'{"" if st == "published" else " <span class=pill>open excavation</span>"}</li>')
items = "".join(_li(*d) for d in digs)
used_areas = [k for k in AREAS if any(k in ([META[s]["area"]] + META[s]["areas"]) for s, *_ in digs)]
used_types = [k for k in QTYPES if any(k in META[s]["types"] for s, *_ in digs)]
chips = ('<p class="small" id="filters">Browse: <b>Area</b> ' + " ".join(f'<button class="pill" data-k="a:{k}" style="cursor:pointer;background:none;color:inherit">{E(AREAS[k]["name"])}</button>' for k in used_areas)
         + ' <b>Question</b> ' + " ".join(f'<button class="pill" data-k="t:{k}" style="cursor:pointer;background:none;color:inherit">{E(QTYPES[k]["name"])}</button>' for k in used_types)
         + ' <button class="pill" data-k="p:1" style="cursor:pointer;background:none;color:inherit">Starts from a widely shared claim</button> <button class="pill" data-k="x" style="cursor:pointer;background:none;color:inherit">Show all</button></p>')
filt_js = ("<script>(function(){var on=new Set(),lis=[].slice.call(document.querySelectorAll('ul.l li[data-areas]'));function run(){lis.forEach(function(li){var ok=true;on.forEach(function(k){var v=k.slice(2);"
           "if(k[0]==='a'&&li.dataset.areas.split(' ').indexOf(v)<0)ok=false;if(k[0]==='t'&&li.dataset.types.split(' ').indexOf(v)<0)ok=false;if(k[0]==='p'&&li.dataset.popular!=='1')ok=false});li.style.display=ok?'':'none'})}"
           "[].slice.call(document.querySelectorAll('#filters button')).forEach(function(b){b.onclick=function(){var k=b.dataset.k;if(k==='x'){on.clear();[].forEach.call(document.querySelectorAll('#filters button'),function(x){x.style.fontWeight=''})}else if(on.has(k)){on.delete(k);b.style.fontWeight=''}else{on.add(k);b.style.fontWeight='700'}run()}})})();</script>")
write("digs/index.html", page("Active excavations", f'<p class="eyebrow">Active excavations</p><h1>What we are excavating</h1><p>Each excavation files its claims with evidence, confidence and limits.</p>{chips}<ul class="l">{items}</ul>{filt_js}', "Active excavations on Stratah: each files its claims with evidence, confidence and limits.", "/digs/", depth=1))
for _k in used_areas:
    _rows = "".join(_li(*d) for d in digs if _k in ([META[d[0]]["area"]] + META[d[0]]["areas"]))
    _rows = _rows.replace('href="', 'href="../../digs/')
    write(f"areas/{_k}/index.html", page(f'{AREAS[_k]["name"]}', f'<p class="eyebrow">Area</p><h1>{E(AREAS[_k]["name"])}</h1><p>{E(AREAS[_k]["about"])}</p><ul class="l">{_rows}</ul><p><a href="../../digs/">All active excavations</a></p>', f'{AREAS[_k]["name"]} excavations on Stratah: {AREAS[_k]["about"]}', f"/areas/{_k}/", depth=2))
    urls.append(f"/areas/{_k}/")
crow = "".join(f'<li><span class="mono">{E(d)}</span> · <a href="../digs/{E(sl)}/">{E(h)}</a><br>{E(t)}</li>' for d, sub, sl, h, t in sorted(corrections, reverse=True)) or "<li>No corrections logged yet.</li>"
write("corrections/index.html", page("Corrections", f'<p class="eyebrow">Corrections</p><h1>What we got wrong, and fixed</h1><p>Every correction made to a published excavation is logged and stays visible. The logs are append-only: an entry is never deleted or rewritten, only added to.</p><ul class="l">{crow}</ul>', "Corrections to Stratah digs.", "/corrections/", depth=1))
write("about/index.html", page("About", f'<p class="eyebrow">About</p><h1>{E(CFG["name"])}: {E(CFG["tagline"])}</h1><p>{E(" ".join(CFG["about"].split()))}</p><p>See the <a href="../method/">method</a> for the rules, and <a href="../corrections/">corrections</a> for what we have fixed.</p>', " ".join(CFG["about"].split())[:200], "/about/", depth=1))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_atlas
write("atlas/index.html", build_atlas.build_atlas_html(CFG["publish"])[0])
_ideas = yaml.safe_load(open(os.path.join(ROOT, "build", "ideas.yaml")))
_lab = {"parked": "parked", "exploring": "exploring", "done": "done"}
_li = "".join(f'<li id="{E(i["id"])}"><b>{E(i["title"])}</b> <span class="pill">{E(_lab.get(i["status"], i["status"]))}</span><br>{E(" ".join(str(i["summary"]).split()))}</li>' for i in _ideas["ideas"])
write("ideas/index.html", page("Ideas for exploration", f'<p class="eyebrow">Ideas</p><h1>Ideas for exploration</h1><p>{E(" ".join(str(_ideas["intro"]).split()))}</p><ul class="l">{_li}</ul><p><a href="{E(CFG["issues_url"])}">Suggest an idea or a dig</a>.</p>', "Ideas and possible next digs for Stratah, with their status.", "/ideas/", depth=1))
_QMAP = {"casket-letters": "casket-letters", "eikon-basilike": "eikon-basilike"}
for _sub, _qd in _QMAP.items():
    _qp = os.path.join(OUT, "questions", _qd, "index.html")
    if os.path.exists(_qp) and _sub in ASSESS and ASSESS[_sub][0]:
        _q = open(_qp, encoding="utf-8").read()
        _q = re.sub(r"<!--ASSESSICT-->", lambda m: assessment_html(ASSESS[_sub][0], ASSESS[_sub][1], prefix="../../", claims=ASSESS[_sub][2]), _q, count=1)
        open(_qp, "w", encoding="utf-8").write(_q)
_hp = os.path.join(OUT, "index.html")
if os.path.exists(_hp):
    _h = open(_hp, encoding="utf-8").read()
    _cards = "".join(f'<a class="dig-card" href="digs/{E(s)}/" style="display:block"><div class="dig-icon">&#9672;</div><div class="dig-name">{E(META[s].get("question") or h)}</div>'
                     f'<div class="dig-meta"><span style="color:var(--ink)">{E(META[s].get("short", ""))}</span>{"" if META[s].get("short") else "<br>" + E(" ".join(str(sm).split()))} {"" if st == "published" else "(Open excavation)"}</div></a>' for s, h, sm, st in digs)
    _h = re.sub(r"<!--EXCAVATIONS:start.*?-->.*?<!--EXCAVATIONS:end-->", lambda m: f'<div class="dig-grid" style="grid-template-columns:1fr">{_cards}</div>', _h, flags=re.S)
    open(_hp, "w", encoding="utf-8").write(_h)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://{CFG['domain']}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: https://{CFG['domain']}/sitemap.xml\n")
write("llms.txt", f"# {CFG['name']}\n\n> {' '.join(CFG['about'].split())}\n\n## Active excavations\n\n" + "".join(f"- [{h}](https://{CFG['domain']}/digs/{s}/) [{AREAS[META[s]['area']]['name'] if META[s]['area'] else ''}]: {' '.join(str(sm).split())} ({'published' if st == 'published' else 'open excavation'}; data: https://{CFG['domain']}/digs/{s}/claims.yaml)\n" for s, h, sm, st in digs) + f"\n## How to cite\n\nCite the dig page and name its status. Each claim lists its confidence and whether its source was read directly. Corrections: https://{CFG['domain']}/corrections/\n")
print(f"site built in {OUT}: {len(digs)} excavation(s), {len(corrections)} correction note(s)")
