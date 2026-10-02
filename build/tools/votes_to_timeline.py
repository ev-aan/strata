#!/usr/bin/env python3
"""Turn a rollcalls-*.yaml set (build_votes.py) into a timeline.yaml for render_timeline.py.
Usage: python3 build/tools/votes_to_timeline.py <subject dir> <title> <start YYYY-MM-DD> <end YYYY-MM-DD> [extra_events.yaml]
Every vote is one dot linking to its roll-call page (official XML from 1990, Voteview page before)."""
import sys, os, glob, yaml, re, datetime
d, title, start, end = sys.argv[1:5]
extra = yaml.safe_load(open(sys.argv[5])) if len(sys.argv) > 5 else {"panels": [], "lanes": {}, "sources": {}, "events": []}
S = yaml.safe_load(open(os.path.join(d, "summary.yaml")))
ev = []; k = 0
for f in sorted(glob.glob(os.path.join(d, "rollcalls-*.yaml"))):
    y = yaml.safe_load(open(f)); c = y["congress"]
    for x in y["rollcalls"]:
        k += 1
        if int(str(x["d"])[:4]) >= 1990:
            url = (f"https://clerk.house.gov/evs/{str(x['d'])[:4]}/roll{x['n']:03d}.xml" if x["ch"] == "H" else
                   f"https://www.senate.gov/legislative/LIS/roll_call_votes/vote{c}{x['s']}/vote_{c}_{x['s']}_{x['n']:05d}.xml")
        else:
            url = "https://voteview.com/rollcall/R%s%03d%04d" % (x["ch"], c, x["n"])
        txt = re.sub(r"\s+", " ", x["t"]).strip().capitalize() or x["q"]
        ev.append({"id": f"v{k}", "panel": "years", "lane": "house" if x["ch"] == "H" else "senate", "time": f"{x['d']}T12:00:00Z", "precision": "day",
                   "kind": "official", "status": "single", "sources": ["s_vv"], "link": url,
                   "label": f"{x['d']}: {'House' if x['ch']=='H' else 'Senate'} {x['b'] or ''} {txt[:60]}".replace("  ", " "),
                   "detail": f"{txt} Result: {x['res'] or 'n/a'}; yea {x['y']}, nay {x['x']}. Roll call {x['n']}."})
        # a roll call that is already a shared node (build/nodes/vote-<Voteview id>.yaml) is referenced, not copied
        vid = url.rsplit("/", 1)[1] if "voteview.com" in url else None
        if vid and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nodes", f"vote-{vid}.yaml")):
            ev[-1]["_node"] = f"vote-{vid}"
            ev[-1]["_rev"] = yaml.safe_load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "nodes", f"vote-{vid}.yaml")))["rev"]
# extra panels may carry copy_votes_between: [from, to]; the vote dots in that window are repeated in the panel
for pn in extra["panels"]:
    win = pn.pop("copy_votes_between", None)
    if win:
        for e in [e for e in ev if win[0] <= e["time"][:10] <= win[1]]:
            c = dict(e); c["id"] += "r"; c["panel"] = pn["id"]; ev.append(c)
ev = [({"id": e["id"], "panel": e["panel"], "lane": e["lane"], "node": e["_node"], "rev": e["_rev"]} if "_node" in e else e) for e in ev]
panels = [{"id": "years", "bands": extra.get("bands", []), "title": f"Panel A: {start[:4]} to {end[:4]} (one tick per year)", "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z", "tick_years": 1,
           "lanes": ["tonkin", "house", "senate"]}] + extra["panels"]
lanes = {"tonkin": {"label": "Gulf of Tonkin dig events"}, "house": {"label": "House votes"}, "senate": {"label": "Senate votes"}, **extra["lanes"]}
sources = {"s_vv": {"title": "Voteview roll-call data (secondary index; official record is the anchor from 1990, the Congressional Record before)", "url": "https://voteview.com", "authenticity": "dataset; counts spot-checked for 2009-2026 against official XML, not for these years"}, **extra["sources"]}
tl = {"timeline": {"id": os.path.basename(d.rstrip("/")), "title": title, "as_of": str(datetime.date.today()),
      "note": "Selection rule (log it): roll calls whose description, question or bill contains vietnam, viet nam, southeast asia, tonkin, indochina or gulf of. This is a crude keyword filter: it includes some off-topic votes and will miss Vietnam-related votes that lack those words. Times are not recorded for these votes, so each dot is drawn at noon UTC on its date (date precision only). Every dot links to its roll-call page."},
      "panels": panels, "lanes": lanes, "people": [], "sources": sources, "events": ev + extra["events"]}
yaml.safe_dump(tl, open(os.path.join(d, "timeline.yaml"), "w"), sort_keys=False, width=160, allow_unicode=True)
print(len(ev), "vote events")
