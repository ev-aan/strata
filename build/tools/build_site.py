#!/usr/bin/env python3
"""Assemble the public site into site/ from the repository. YAML is the source of truth; pages are generated.

Usage: python3 build/tools/build_site.py [outdir=site]

Includes: the existing homepage, method page and bounty pages (copied as they are), plus generated pages for each dig listed
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
    nav = (f'<nav><a class="b" href="{up}">{E(CFG["name"])}</a><a href="{up}digs/">Digs</a><a href="{up}method/">Method</a>'
           f'<a href="{up}corrections/">Corrections</a><a href="{up}about/">About</a></nav>')
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
    bits = f'<p><span class="pill s-{E(st)}">{E("refuted: the claim below is false" if st == "refuted" else st.replace("_", " "))}</span> <span class="small">confidence {E(c.get("confidence", "n/a"))}</span></p>'
    bits += f'<p>{E(" ".join(str(c.get("statement", "")).split()))}</p>'
    bits += (f'<div class="meter"><span>Evidence</span><span class="dots">{dots(c.get("evidential_weight"))}</span>'
             f'<span>Public belief</span><span class="dots">{dots(c.get("adoption_weight"))}</span><span>Source checked</span><span>{E(chk)}</span></div>')
    more = ""
    if desc: more += f'<p><b>Anchor.</b> {E(" ".join(str(desc).split()))}</p>'
    if c.get("would_change_if"): more += f'<p><b>Would change if.</b> {E(" ".join(str(c["would_change_if"]).split()))}</p>'
    if nxt: more += f'<p><b>Next step.</b> {E(" ".join(str(nxt).split()))}</p>'
    if more: bits += f'<details><summary>Evidence and limits</summary>{more}</details>'
    return f'<div class="claim" id="{E(c.get("id"))}">{bits}</div>'

order = {"refuted": 0, "established": 1, "contested": 2, "proposed": 3, "searched_gap": 4}
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
# existing pages and files, copied unchanged
for f in ("index.html", "CNAME"):
    if os.path.exists(os.path.join(ROOT, f)): shutil.copy(os.path.join(ROOT, f), OUT)
for d in ("method", "bounties"):
    if os.path.isdir(os.path.join(ROOT, d)): shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
open(os.path.join(OUT, ".nojekyll"), "w").close()

digs, corrections, urls = [], [], ["/", "/digs/", "/method/", "/corrections/", "/about/"]
for sub in CFG["publish"]:
    base = os.path.join(ROOT, "build", "subjects", sub)
    cl = yaml.safe_load(open(os.path.join(base, "claims.yaml")))
    slug = cl.get("url_slug") or sub
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
    banner = (f'<div class="banner"><b>Open dig.</b> This question is still being worked. The headline finding is stated at the confidence shown below; '
              f'not every source has been read in full, and each claim says which. Claims so far: {E(tally)}.</div>' if status != "published" else "")
    body = (f'<p class="eyebrow">Dig · {E(cl.get("title"))}</p><h1>{E(head)}</h1>{banner}'
            f'<p class="summary">{E(" ".join(str(cl.get("search_summary", "")).split()))}</p>')
    if hc: body += f'<h2>The headline finding</h2>{claim_html(hc)}'
    body += f'<p>{E(" ".join(str(cl.get("description", "")).split()))}</p>'
    if cl.get("divergence_note"): body += f'<h2>Where evidence and belief differ</h2><p>{E(" ".join(str(cl["divergence_note"]).split()))}</p>'
    if has_tl: body += '<h2>Timeline</h2><p>Every point on the timeline links to its source. <a href="timeline/">Open the timeline</a>.</p>'
    chp = os.path.join(base, "challenges.yaml")
    if os.path.exists(chp):
        chs = yaml.safe_load(open(chp)).get("challenges", [])
        lab = {"answered": "answered: finding stands", "partly_answered": "partly answered", "open": "open: not yet testable", "finding_changed": "finding changed"}
        body += ('<h2>Challenges addressed</h2><p>Objections raised against this dig, in the form people raise them, with the test we ran and where it stands. '
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
         "mainEntityOfPage": f"https://{CFG['domain']}/digs/{slug}/", "about": cl.get("title"),
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

items = "".join(f'<li><a href="{E(s)}/"><b>{E(h)}</b></a><br><span class="small">{E(" ".join(str(sm).split()))}</span>'
                f'{"" if st == "published" else " <span class=pill>open dig</span>"}</li>' for s, h, sm, st in digs)
write("digs/index.html", page("Digs", f'<p class="eyebrow">Digs</p><h1>What we have dug into</h1><p>Each dig files its claims with evidence, confidence and limits.</p><ul class="l">{items}</ul>', "Digs published on Stratah.", "/digs/", depth=1))
crow = "".join(f'<li><span class="mono">{E(d)}</span> · <a href="../digs/{E(sl)}/">{E(h)}</a><br>{E(t)}</li>' for d, sub, sl, h, t in sorted(corrections, reverse=True)) or "<li>No corrections logged yet.</li>"
write("corrections/index.html", page("Corrections", f'<p class="eyebrow">Corrections</p><h1>What we got wrong, and fixed</h1><p>Every correction made to a published dig is logged and stays visible. The logs are append-only: an entry is never deleted or rewritten, only added to.</p><ul class="l">{crow}</ul>', "Corrections to Stratah digs.", "/corrections/", depth=1))
write("about/index.html", page("About", f'<p class="eyebrow">About</p><h1>{E(CFG["name"])}: {E(CFG["tagline"])}</h1><p>{E(" ".join(CFG["about"].split()))}</p><p>See the <a href="../method/">method</a> for the rules, and <a href="../corrections/">corrections</a> for what we have fixed.</p>', " ".join(CFG["about"].split())[:200], "/about/", depth=1))
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>https://{CFG['domain']}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: https://{CFG['domain']}/sitemap.xml\n")
write("llms.txt", f"# {CFG['name']}\n\n> {' '.join(CFG['about'].split())}\n\n## Digs\n\n" + "".join(f"- [{h}](https://{CFG['domain']}/digs/{s}/): {' '.join(str(sm).split())} ({'published' if st == 'published' else 'open dig'}; data: https://{CFG['domain']}/digs/{s}/claims.yaml)\n" for s, h, sm, st in digs) + f"\n## How to cite\n\nCite the dig page and name its status. Each claim lists its confidence and whether its source was read directly. Corrections: https://{CFG['domain']}/corrections/\n")
print(f"site built in {OUT}: {len(digs)} dig(s), {len(corrections)} correction note(s)")
