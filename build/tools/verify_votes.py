#!/usr/bin/env python3
"""Check every indexed roll call against the official House Clerk / Senate.gov XML (yea and nay totals, date).
Usage: python3 build/tools/verify_votes.py <subject dir> <cache.json>
Writes <subject dir>/verification.yaml: counts, and every exception (mismatch or unreachable). Resumable via the cache file."""
import sys, os, re, json, glob, time, datetime, urllib.request, yaml, collections
from concurrent.futures import ThreadPoolExecutor
d, cache_f = sys.argv[1], sys.argv[2]
cache = json.load(open(cache_f)) if os.path.exists(cache_f) else {}
rows = []
for f in sorted(glob.glob(os.path.join(d, "rollcalls-*.yaml"))):
    y = yaml.safe_load(open(f)); c = y["congress"]
    rows += [(c, x) for x in y["rollcalls"]]
def url(c, x):
    if x["ch"] == "H": return f"https://clerk.house.gov/evs/{str(x['d'])[:4]}/roll{x['n']:03d}.xml"
    return f"https://www.senate.gov/legislative/LIS/roll_call_votes/vote{c}{x['s']}/vote_{c}_{x['s']}_{x['n']:05d}.xml"
def get(u):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=40).read().decode("utf8", "ignore")
        except Exception as e:
            time.sleep(2 * (i + 1)); err = str(e)[:50]
    return "ERR " + err
def check(a):
    c, x = a; u = url(c, x)
    if u in cache: return
    t = get(u)
    if t.startswith("ERR"): cache[u] = ["unreachable", t]; return
    try:
        if x["ch"] == "H":
            if "<recorded-vote>" not in t: cache[u] = ["unreachable", "no recorded votes"]; return
            cnt = collections.Counter(re.findall(r"<vote>([^<]*)</vote>", t))
            y = cnt["Yea"] + cnt["Aye"]; n = cnt["Nay"] + cnt["No"]
            dt = re.search(r"<action-date>([^<]+)</action-date>", t).group(1)
            dd = str(datetime.datetime.strptime(dt, "%d-%b-%Y").date())
        else:
            y = int(re.search(r"<yeas>(\d+)</yeas>", t).group(1)); n = int(re.search(r"<nays>(\d+)</nays>", t).group(1)); dd = None
    except Exception as e:
        cache[u] = ["unreachable", "parse " + str(e)[:40]]; return
    q = x["q"].startswith("Election of the Speaker")
    ok = q or ((y, n) == (x["y"], x["x"]) and (dd is None or dd == str(x["d"])))
    cache[u] = ["match" if ok else "mismatch", [y, n, dd]]
todo = [a for a in rows if url(*a) not in cache]
print("to check", len(todo), "of", len(rows), flush=True)
done = 0
with ThreadPoolExecutor(5) as ex:
    for i, _ in enumerate(ex.map(check, todo)):
        if i % 500 == 0: json.dump(cache, open(cache_f, "w")); print(i, flush=True)
json.dump(cache, open(cache_f, "w"))
cnt = collections.Counter(v[0] for v in cache.values())
exc = []
for c, x in rows:
    v = cache.get(url(c, x))
    if v and v[0] != "match": exc.append({"chamber": x["ch"], "congress": c, "date": str(x["d"]), "n": x["n"], "index_yea_nay": [x["y"], x["x"]], "result": v[0], "official_or_error": v[1], "url": url(c, x)})
yaml.safe_dump({"checked": len(cache), "totals": dict(cnt), "note": "match = yea, nay (and House date) equal the official XML. Speaker elections are skipped (they count names, not yea/nay). Differences are listed with both counts; their causes are not analysed here. The official record wins.", "exceptions": exc},
               open(os.path.join(d, "verification.yaml"), "w"), sort_keys=False, width=140)
print(dict(cnt), "exceptions", len(exc))
