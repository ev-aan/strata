#!/usr/bin/env python3
"""Render a Strata timeline.yaml to a self-contained HTML page with inline SVG.

Usage: python3 build/tools/render_timeline.py build/subjects/<subject>/timeline.yaml
Writes timeline.html next to the YAML. YAML is the source of truth; never edit the HTML by hand.
Marker shape = kind of source (data, official, witness, media). Marker style = status
(reported, single, disputed, inferred). Colour is never the only signal.
"""
import sys, html, datetime as dt
from pathlib import Path
import yaml

W, LABEL_W, PAD_R = 1120, 215, 24
LANE_H, TOP, AXIS_H = 64, 14, 44

def parse(t):
    return dt.datetime.fromisoformat(str(t).replace("Z", "+00:00"))

def esc(s):
    return html.escape(str(s), quote=True)

def marker(kind, cx, cy, r, cls):
    if kind == "data":
        return f'<circle class="{cls}" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/>'
    if kind == "official":
        return f'<rect class="{cls}" x="{cx-r:.1f}" y="{cy-r:.1f}" width="{2*r}" height="{2*r}" rx="2"/>'
    if kind == "witness":
        return f'<polygon class="{cls}" points="{cx:.1f},{cy-r-2:.1f} {cx+r+2:.1f},{cy:.1f} {cx:.1f},{cy+r+2:.1f} {cx-r-2:.1f},{cy:.1f}"/>'
    return f'<polygon class="{cls}" points="{cx:.1f},{cy-r-1:.1f} {cx+r+2:.1f},{cy+r:.1f} {cx-r-2:.1f},{cy+r:.1f}"/>'

def render_panel(panel, events, lanes, numbers):
    start, end = parse(panel["start"]), parse(panel["end"])
    span = (end - start).total_seconds()
    pw = W - LABEL_W - PAD_R
    X = lambda t: LABEL_W + pw * ((parse(t) - start).total_seconds() / span)
    lane_ids = panel["lanes"]
    H = TOP + LANE_H * len(lane_ids) + AXIS_H
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(panel["title"])}" class="tl">']
    # grid and axis
    step = dt.timedelta(minutes=panel.get("tick_minutes", 0)) if panel.get("tick_minutes") else dt.timedelta(hours=panel.get("tick_hours", 6))
    t = start
    ticks = []
    while t <= end:
        ticks.append(t); t += step
    for t in ticks:
        x = LABEL_W + pw * ((t - start).total_seconds() / span)
        o.append(f'<line class="grid" x1="{x:.1f}" y1="{TOP-8}" x2="{x:.1f}" y2="{TOP+LANE_H*len(lane_ids)}"/>')
        lab = t.strftime("%H:%M") if panel.get("tick_minutes") else t.strftime("%d %b %H:%M")
        o.append(f'<text class="tick" x="{x:.1f}" y="{TOP+LANE_H*len(lane_ids)+16}" text-anchor="middle">{lab}</text>')
        if panel.get("tick_minutes"):
            d = (t + dt.timedelta(hours=4)).strftime("%H:%M")
            o.append(f'<text class="tick2" x="{x:.1f}" y="{TOP+LANE_H*len(lane_ids)+31}" text-anchor="middle">{d}</text>')
    ytxt = TOP + LANE_H * len(lane_ids)
    o.append(f'<text class="axl" x="10" y="{ytxt+16}">Time, UTC</text>')
    if panel.get("tick_minutes"):
        o.append(f'<text class="axl" x="10" y="{ytxt+31}">Same, Dubai time (UTC+4)</text>')
    for i, lid in enumerate(lane_ids):
        y = TOP + LANE_H * i
        o.append(f'<rect class="lane{i%2}" x="0" y="{y}" width="{W}" height="{LANE_H}"/>')
        o.append(f'<text class="lane-label" x="10" y="{y+LANE_H/2+4}">{esc(lanes[lid]["label"])}</text>')
    # events per lane with vertical dodge
    for i, lid in enumerate(lane_ids):
        evs = sorted([e for e in events if e["panel"] == panel["id"] and e["lane"] == lid], key=lambda e: parse(e["time"]))
        levels = []  # last x end per level
        for e in evs:
            x = X(e["time"]); xe = X(e["end"]) if e.get("end") else x
            lv = 0
            while lv < len(levels) and levels[lv] > x - 26:
                lv += 1
            if lv == len(levels): levels.append(0)
            levels[lv] = max(xe, x) + 4
            nlev = 3
            cy = TOP + LANE_H * i + 16 + lv * 16 if nlev else TOP + LANE_H * i + LANE_H / 2
            cy = min(cy, TOP + LANE_H * i + LANE_H - 12)
            cls = f'm {e["status"]}'
            n = numbers[e["id"]]
            if e.get("end"):
                o.append(f'<rect class="span {e["status"]}" x="{x:.1f}" y="{cy-3:.1f}" width="{max(xe-x,3):.1f}" height="6" rx="3"/>')
            if e.get("alt_time"):
                ax = X(e["alt_time"])
                o.append(f'<line class="alt" x1="{ax:.1f}" y1="{cy:.1f}" x2="{x:.1f}" y2="{cy:.1f}"/>')
                o.append(f'<circle class="ghost" cx="{ax:.1f}" cy="{cy:.1f}" r="8"><title>{esc(e["alt_note"])}</title></circle>')
                o.append(f'<text class="ghost-t" x="{ax:.1f}" y="{cy+22:.1f}" text-anchor="middle">CNN time</text>')
            tip = f'{n}. {e["label"]} ({e["status"]}, {e["kind"]}). {e.get("detail","")}'
            o.append(f'<g class="ev"><title>{esc(tip)}</title>{marker(e["kind"], x, cy, 8, cls)}'
                     f'<text class="num" x="{x+13:.1f}" y="{cy+4:.1f}">{n}</text>'
                     + (f'<text class="bang" x="{x:.1f}" y="{cy+4:.1f}" text-anchor="middle">!</text>' if e["status"] == "disputed" else '') + '</g>')
    o.append('</svg>')
    return "\n".join(o)

CSS = """
:root{--bg:#fbfaf7;--fg:#1d1c1a;--mute:#5d5a54;--card:#ffffff;--line:#d9d5cc;--lane0:#f3f1ec;--lane1:#faf9f6;
--rep:#1f5fa8;--single:#5b7fa6;--disp:#b25400;--inf:#6b6b6b;--ghost:#8a2b2b}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#15161a;--fg:#ecebe6;--mute:#a9a79f;--card:#1d1f25;--line:#3a3d46;--lane0:#1b1d23;--lane1:#17181d;
--rep:#6fb0ff;--single:#8fb0d6;--disp:#ffa24a;--inf:#a3a3a3;--ghost:#ff8a8a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:1180px;margin:0 auto;padding:20px 16px 56px}h1{font-size:1.5rem;margin:.2em 0}h2{font-size:1.15rem;margin:1.6em 0 .5em}
.note{color:var(--mute);max-width:80ch}.note.small{font-size:12.5px;margin:.1em 0 .4em}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:10px 0}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--card)}svg.tl{width:100%;min-width:900px;height:auto;display:block}
.lane0{fill:var(--lane0)}.lane1{fill:var(--lane1)}.grid{stroke:var(--line);stroke-width:1}.lane-label{font-size:12.5px;fill:var(--fg)}
.tick{font-size:11px;fill:var(--mute)}.tick2{font-size:10.5px;fill:var(--mute);opacity:.85}.axl{font-size:10.5px;fill:var(--mute)}
.m,.span{stroke-width:2}.m.reported{fill:var(--rep);stroke:var(--rep)}.m.single{fill:var(--single);fill-opacity:.55;stroke:var(--single);stroke-dasharray:3 2}
.m.disputed{fill:var(--disp);stroke:var(--fg)}.m.inferred{fill:none;stroke:var(--inf);stroke-dasharray:3 2}
.span.reported{fill:var(--rep);opacity:.35}.span.single{fill:var(--single);opacity:.3}.span.disputed{fill:var(--disp);opacity:.35}.span.inferred{fill:var(--inf);opacity:.25}
.num{font-size:11px;font-weight:700;fill:var(--fg)}.bang{font-size:11px;font-weight:800;fill:#111;pointer-events:none}
.ghost{fill:none;stroke:var(--ghost);stroke-width:2;stroke-dasharray:3 2}.ghost-t{font-size:10px;fill:var(--ghost)}.alt{stroke:var(--ghost);stroke-width:1.5;stroke-dasharray:2 3}
.legend{display:flex;flex-wrap:wrap;gap:6px 22px;align-items:center;font-size:13px}.legend span{display:inline-flex;align-items:center;gap:6px}
table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}th{color:var(--mute);font-weight:600}
td.n{font-weight:700;white-space:nowrap}.tag{font-size:11.5px;padding:1px 7px;border:1px solid var(--line);border-radius:99px;white-space:nowrap}
.tag.disputed{border-color:var(--disp);color:var(--disp)}.people li{margin:.35em 0}a{color:var(--rep)}
"""

def legend():
    def sw(inner):
        return '<svg width="22" height="20" viewBox="0 0 22 20" aria-hidden="true">' + inner + '</svg>'
    bang = '<text x="11" y="14" text-anchor="middle" class="bang">!</text>'
    ghost = '<circle class="ghost" cx="11" cy="10" r="7"/>'
    items = [
        ("<b>Shape = kind of source:</b>", None),
        (sw(marker("data", 11, 10, 7, "m reported")), "machine-recorded data"),
        (sw(marker("official", 11, 10, 7, "m reported")), "official statement"),
        (sw(marker("witness", 11, 10, 7, "m reported")), "a person's account"),
        (sw(marker("media", 11, 10, 7, "m reported")), "a news outlet's report"),
        ("<b>Style = status:</b>", None),
        (sw(marker("data", 11, 10, 7, "m reported")), "2+ sources agree"),
        (sw(marker("data", 11, 10, 7, "m single")), "one source"),
        (sw(marker("data", 11, 10, 7, "m disputed") + bang), "sources differ"),
        (sw(marker("data", 11, 10, 7, "m inferred")), "our inference / time not reported"),
        (sw(ghost), "the same event at another source's time"),
    ]
    parts = []
    for a, b in items:
        parts.append(a if b is None else "<span>" + a + " " + html.escape(b) + "</span>")
    return '<div class="legend card" aria-label="Legend">' + " ".join(parts) + "</div>"

def main(path):
    path = Path(path); d = yaml.safe_load(path.read_text())
    tl, panels, lanes, ev, srcs = d["timeline"], d["panels"], d["lanes"], d["events"], d["sources"]
    order = []
    for p in panels:
        order += [e["id"] for e in sorted([e for e in ev if e["panel"] == p["id"]], key=lambda e: parse(e["time"]))]
    numbers = {eid: i + 1 for i, eid in enumerate(order)}
    byid = {e["id"]: e for e in ev}
    body = [f'<h1>{esc(tl["title"])}</h1>', f'<p class="note">As of {esc(tl["as_of"])}. {esc(tl["note"])}</p>', legend()]
    for p in panels:
        body.append(f'<h2>{esc(p["title"])}</h2><p class="note small">Scroll sideways on a phone.</p><div class="scroll">{render_panel(p, ev, lanes, numbers)}</div>')
    body.append('<h2>Events (numbers match the diagram)</h2><div class="card"><table><thead><tr><th>#</th><th>When (UTC)</th><th>What</th><th>Status</th><th>Sources</th></tr></thead><tbody>')
    for eid in order:
        e = byid[eid]; t = parse(e["time"])
        when = t.strftime("%d %b") + ("" if e["precision"] == "day" else " " + t.strftime("%H:%M") + (" to " + parse(e["end"]).strftime("%H:%M") if e.get("end") else ""))
        when += {"approx": " (approx.)", "day": " (date only)"}.get(e["precision"], "")
        s = ", ".join(f'<a href="{esc(srcs[k]["url"])}" rel="noopener">{esc(k)}</a>' for k in e["sources"])
        body.append(f'<tr><td class="n">{numbers[eid]}</td><td>{esc(when)}</td><td><b>{esc(e["label"])}</b><br>{esc(e.get("detail",""))}'
                    + (f'<br><i>CNN-time ghost marker: {esc(e["alt_note"])}</i>' if e.get("alt_note") else '') + f'</td>'
                    f'<td><span class="tag {e["status"]}">{esc(e["status"])}</span> <span class="tag">{esc(e["kind"])}</span></td><td>{s}</td></tr>')
    body.append('</tbody></table></div>')
    body.append('<h2>People and bodies involved</h2><div class="card"><ul class="people">' + "".join(f'<li><b>{esc(x["who"])}</b>: {esc(x["detail"])}</li>' for x in d["people"]) + '</ul></div>')
    body.append('<h2>Sources</h2><div class="card"><ul>' + "".join(f'<li><code>{esc(k)}</code> <a href="{esc(v["url"])}" rel="noopener">{esc(v["title"])}</a></li>' for k, v in srcs.items()) + '</ul></div>')
    body.append('<p class="note">Generated from timeline.yaml by build/tools/render_timeline.py. This page records what is reported and where reports differ. It is not a finding about what happened.</p>')
    out = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(tl["title"])}</title><style>{CSS}</style></head><body><main>{"".join(body)}</main></body></html>'
    dest = path.with_name("timeline.html"); dest.write_text(out); print("wrote", dest, len(out), "bytes;", len(ev), "events")

if __name__ == "__main__":
    main(sys.argv[1])
