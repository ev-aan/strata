#!/usr/bin/env python3
"""Render summary.yaml + presidencies.yaml (from build/tools/build_votes.py) into a readable HTML/SVG overview.
Usage: python3 build/tools/render_votes_summary.py <subject dir> [title]
Rows: House and Senate roll calls per month (passage votes darker); bands: presidencies; dots: the closest passage votes
(rule in summary.yaml), each a link to the official record. Neutral colours: no party colours."""
import sys, os, yaml, html, datetime
d = sys.argv[1]; title = sys.argv[2] if len(sys.argv) > 2 else "Recorded votes"
S = yaml.safe_load(open(os.path.join(d, "summary.yaml"))); P = yaml.safe_load(open(os.path.join(d, "presidencies.yaml")))["presidencies"]
V = None
vp = os.path.join(d, "verification.yaml")
if os.path.exists(vp): V = yaml.safe_load(open(vp))
months = sorted(S["months"]); m0 = datetime.date.fromisoformat(months[0] + "-01"); m1 = datetime.date.fromisoformat(months[-1] + "-01")
nm = (m1.year - m0.year) * 12 + m1.month - m0.month + 1
L, R, W = 120, 30, 1400; PW = W - L - R; mw = PW / nm
def x_of(date):
    dt = date if isinstance(date, datetime.date) else datetime.date.fromisoformat(str(date))
    return L + ((dt.year - m0.year) * 12 + dt.month - m0.month + (dt.day - 1) / 31) * mw
rows = [("H", "House"), ("S", "Senate")]; ROWH = 150; TOP = 56
H = TOP + ROWH * 2 + 120
mx = max(sum(v for k, v in c.items() if k.startswith(ch)) for c in S["months"].values() for ch, _ in rows)
out = []
for i, p in enumerate(P):
    xa, xb = x_of(p["from"]), min(x_of(p["to"]), W - R)
    out.append(f'<rect x="{xa:.1f}" y="{TOP-26}" width="{xb-xa:.1f}" height="{H-TOP-30}" fill="var(--b{i%2})"/>')
    out.append(f'<text x="{xa+4:.1f}" y="{TOP-10}" class="band">{html.escape(p["name"])}</text>')
for ci, (ch, name) in enumerate(rows):
    y0 = TOP + ci * ROWH + ROWH - 30
    out.append(f'<text x="8" y="{y0-ROWH/2+12:.0f}" class="lab">{name}</text><text x="8" y="{y0-ROWH/2+28:.0f}" class="sub">votes per month</text>')
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{y0}" y2="{y0}" class="ax"/>')
    for m in months:
        c = S["months"][m]; tot = sum(v for k, v in c.items() if k.startswith(ch)); ps = c.get(f"{ch}_passage", 0)
        if not tot: continue
        x = x_of(m + "-01"); h = (ROWH - 56) * tot / mx; hp = (ROWH - 56) * ps / mx
        out.append(f'<rect x="{x+0.5:.1f}" y="{y0-h:.1f}" width="{max(mw-1,1):.1f}" height="{h:.1f}" class="o"><title>{m}: {tot} {name} roll calls, {ps} passage votes</title></rect>')
        if ps: out.append(f'<rect x="{x+0.5:.1f}" y="{y0-hp:.1f}" width="{max(mw-1,1):.1f}" height="{hp:.1f}" class="p"/>')
# year ticks
for yr in range(m0.year, m1.year + 1):
    x = x_of(f"{yr}-01-01")
    if x < L: continue
    out.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{TOP}" y2="{TOP+ROWH*2+30}" class="tick"/><text x="{x+3:.1f}" y="{TOP+ROWH*2+44}" class="sub">{yr}</text>')
# closest passage dots
yb = TOP + ROWH * 2 + 70
for ci, (ch, name) in enumerate(rows):
    yy = yb + ci * 22
    out.append(f'<text x="8" y="{yy+4}" class="sub">closest {name} passage</text>')
    for r in S["closest_passage"]:
        if r["chamber"] != ch: continue
        t = f'{r["date"]}  {r["bill"]}  {r["description"] or r["question"]}  {r["result"]}  {r["yea"]}-{r["nay"]}'
        out.append(f'<a href="{html.escape(r["url"])}" target="_blank" rel="noopener"><circle cx="{x_of(r["date"]):.1f}" cy="{yy}" r="6" class="d"><title>{html.escape(t)}</title></circle></a>')
svg = f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{html.escape(title)}">' + "".join(out) + "</svg>"
tr = "".join(f'<tr><td>{r["date"]}</td><td>{"House" if r["chamber"]=="H" else "Senate"}</td><td>{html.escape(r["bill"])}</td><td>{html.escape(r["description"] or r["question"])}</td>'
             f'<td>{html.escape(r["result"])}</td><td>{r["yea"]}-{r["nay"]}</td><td><a href="{html.escape(r["url"])}" target="_blank" rel="noopener">official record</a></td></tr>' for r in sorted(S["closest_passage"], key=lambda r: r["date"]))
ver = ""
if V: ver = f'<p><b>Verification:</b> {V["checked"]} roll calls checked against the official record; results {V["totals"]}; {len(V["exceptions"])} listed exceptions (see verification.yaml). The official record wins where they differ.</p>'
page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1c1a;--mute:#5d5a54;--line:#d9d5cc;--b0:#f1efe9;--b1:#faf9f6;--o:#9db4d1;--p:#1f5fa8;--d:#b25400}}
@media (prefers-color-scheme:dark){{:root:not([data-theme=light]){{--bg:#15161a;--fg:#ecebe6;--mute:#a9a79f;--line:#3a3d46;--b0:#1b1d23;--b1:#17181d;--o:#4b6381;--p:#6fb0ff;--d:#ffa24a}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,sans-serif;padding:16px;max-width:1440px;margin-inline:auto}}
h1{{font-size:1.5rem}}.band{{font-size:13px;fill:var(--fg);font-weight:600}}.lab{{font-size:14px;fill:var(--fg);font-weight:600}}.sub{{font-size:11px;fill:var(--mute)}}
.ax{{stroke:var(--line)}}.tick{{stroke:var(--line);stroke-dasharray:2 3}}.o{{fill:var(--o)}}.p{{fill:var(--p)}}.d{{fill:var(--d);stroke:var(--bg);stroke-width:1.5}}.d:hover{{r:9}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}}th,td{{text-align:left;padding:6px 8px;border-top:1px solid var(--line);vertical-align:top}}a{{color:var(--p)}}.n{{color:var(--mute);max-width:900px}}
.wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:8px}}</style></head><body>
<h1>{html.escape(title)}</h1>
<p class="n">{S["rolls"]} recorded votes in the House and Senate. Bars are votes per month; the darker part is passage votes of bills and joint resolutions. Grey bands are presidential terms, shown for context only; no claim is made that a President caused any vote. Orange dots are the closest passage votes (rule: {html.escape(S["closest_rule"])}). Each dot links to the official record. Source index: Voteview (secondary); official XML is the anchor.</p>
{ver}<div class="wrap">{svg}</div>
<h2>Closest passage votes (flagged by the rule above)</h2><div class="wrap"><table><tr><th>Date</th><th>Chamber</th><th>Bill</th><th>Description</th><th>Result</th><th>Yea-Nay</th><th>Source</th></tr>{tr}</table></div>
<p class="n">Generated from summary.yaml and presidencies.yaml by build/tools/render_votes_summary.py. The full vote list is in rollcalls-111.yaml to rollcalls-119.yaml.</p></body></html>'''
open(os.path.join(d, "overview.html"), "w").write(page); print("wrote overview.html", len(page), "bytes")
