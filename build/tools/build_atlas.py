#!/usr/bin/env python3
"""Build the Stratah atlas: one zoomable, filterable map of every dated event in the digs' timeline.yaml files.

Usage as a script: python3 build/tools/build_atlas.py <out.html> [--all]
  default: only the digs listed under `publish` in build/site.yaml (what the public site may show)
  --all:   every subject that has a timeline.yaml (a private preview; includes work in progress)
Used by build_site.py (function build_atlas_html) for site/atlas/.

Time runs left (past) to right (future). Each dig is a row; vertical position inside a row only avoids overlap.
`axis` per event: 'real' (default; when it happened or was recorded) or 'narrative' (when a story says it happened).
The two axes are switched, never mixed. YAML is the source; this page is generated."""
import os, sys, glob, json, html, datetime, re, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nodes import resolve_timeline

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SUBJ = os.path.join(ROOT, "build", "subjects")

def _days(y, m, d):
    # days since 1970-01-01 in the proleptic Gregorian calendar (astronomical years, so 1 BCE is year 0)
    y -= m <= 2
    era = y // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468

def ms(iso):
    s = str(iso).replace("Z", "")
    if s.startswith("-") or len(s.split("-")[0]) > 4:
        m = re.match(r"^(-?\d+)-(\d\d)-(\d\d)", s)
        yy = int(m.group(1))
        yy = yy + 1 if yy < 0 else yy       # negative years are BCE as written: -2345 is 2345 BCE (astronomical -2344)
        return _days(yy, int(m.group(2)), int(m.group(3))) * 86400000
    d = datetime.datetime.fromisoformat(s) if "T" in s else datetime.datetime.fromisoformat(s + "T00:00:00")
    return int((d - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)

def load(subjects):
    data = []
    for sub in subjects:
        tp = os.path.join(SUBJ, sub, "timeline.yaml")
        if not os.path.exists(tp): continue
        T = yaml.safe_load(open(tp))
        T = resolve_timeline(T)
        tl = T.get("timeline", {}); srcs = T.get("sources", {}); lanes = T.get("lanes", {})
        cp = os.path.join(SUBJ, sub, "claims.yaml")
        title = tl.get("title") or sub
        slug = None
        if os.path.exists(cp):
            C = yaml.safe_load(open(cp)); slug = C.get("url_slug"); title_dig = C.get("title") or sub
        else: title_dig = sub
        evs, seen = [], set()
        for e in T.get("events", []):
            key = (e.get("label"), e.get("time"))
            if key in seen: continue          # the same event repeated in a zoomed panel
            seen.add(key)
            ss = [{"title": (srcs.get(i) or {}).get("title", i), "url": (srcs.get(i) or {}).get("url", ""), "auth": (srcs.get(i) or {}).get("authenticity", "")} for i in e.get("sources", [])]
            evs.append({"id": f"{sub}:{e.get('id')}", "t": ms(e["time"]), "e": ms(e["end"]) if e.get("end") else None, "p": e.get("precision", "day"),
                        "k": e.get("kind", "analysis"), "st": e.get("status", "single"), "l": " ".join(str(e.get("label", "")).split()),
                        "d": " ".join(str(e.get("detail", "")).split()), "lane": (lanes.get(e.get("lane")) or {}).get("label", e.get("lane", "")),
                        "link": e.get("link") or (ss[0]["url"] if ss else ""), "src": ss, "axis": e.get("axis", "real"),
                        "alt": ({"t": ms(e["alt_time"]), "note": e.get("alt_note", "")} if e.get("alt_time") else None), "node": e.get("node", ""), "db": e.get("date_basis", ""), "win": ({"a": ms(e["window"]["earliest"]), "b": (None if e["window"].get("latest") == "open" else ms(str(e["window"]["latest"]) + ("T23:59:59" if "T" not in str(e["window"]["latest"]) and len(str(e["window"]["latest"])) > 7 else ""))), "cv": ([ms(e["window"]["certainly_covers"]["from"]), ms(e["window"]["certainly_covers"]["to"])] if e["window"].get("certainly_covers") else None), "bn": e["window"].get("begin_note", ""), "en": e["window"].get("end_note", "")} if e.get("window") else None), "co": e.get("corro"), "pl": e.get("place"), "ab": e.get("about", []), "sh": [s for s in e.get("shared_by", []) if s != sub]})
        if evs: data.append({"id": sub, "title": title_dig, "tl_title": tl.get("title", ""), "slug": slug, "events": sorted(evs, key=lambda x: x["t"])})
    return data

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Atlas: events across the excavations</title>
<meta name="description" content="Every dated event in the Stratah excavations on one zoomable timeline, left to right from past to future, filterable, each dot linking to its source.">
<style>
:root{--bg:#F5F2EC;--panel:#fff;--ink:#1A1814;--mid:#4A4640;--mute:#6f6962;--line:rgba(26,24,20,.16);--c0:#1f5fa8;--c1:#a8541a;--c2:#2a7a5a;--c3:#8a3b72;--c4:#6a6a2a;--c5:#a02c3c;--c6:#2c6f8f;--c7:#7a5a1a}
@media (prefers-color-scheme:dark){:root{--bg:#16150f;--panel:#1d1b14;--ink:#ece8de;--mid:#c3beb2;--mute:#a09a8d;--line:rgba(236,232,222,.2);--c0:#6fb0ff;--c1:#ffa24a;--c2:#5ccaa5;--c3:#e08cc8;--c4:#cfcf6a;--c5:#ff8a98;--c6:#7cc7ea;--c7:#e0bd6a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Georgia,sans-serif;display:flex;flex-direction:column;height:100vh}
header{padding:10px 16px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}h1{font:500 18px Georgia,serif;margin:0;letter-spacing:.04em}
.tog,.chip,button{font:12px ui-monospace,monospace;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:99px;padding:3px 11px;cursor:pointer}.chip.off{opacity:.35}.tog.on{background:var(--ink);color:var(--bg)}button:disabled,.tog:disabled{opacity:.4;cursor:not-allowed}
#filters{padding:6px 16px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:6px;align-items:center;font:12px ui-monospace,monospace;color:var(--mute)}
input[type=search]{font:13px system-ui;padding:3px 10px;border:1px solid var(--line);border-radius:99px;background:var(--panel);color:var(--ink);width:170px}
main{flex:1;display:flex;min-height:0}#stage{flex:1;min-width:0;position:relative;overflow-x:hidden;overflow-y:auto;touch-action:pan-y}#svg{width:100%;height:100%;display:block;cursor:grab}#svg:active{cursor:grabbing}
#panel{width:340px;max-width:44vw;border-left:1px solid var(--line);background:var(--panel);padding:14px;overflow:auto;font-size:14px}#panel h2{font:500 16px Georgia,serif;margin:.2em 0 .4em}.mono{font:11.5px ui-monospace,monospace;color:var(--mute)}
a{color:var(--c0)}.note{color:var(--mute);font-size:13px}.clist{padding-left:18px}.clist li{margin:6px 0}.rowlabel{font:600 12px system-ui;cursor:pointer}
@media (max-width:760px){header .mono{display:none}#filters{display:none}#filters.open{display:flex;max-height:34vh;overflow:auto}main{flex-direction:column}#panel{width:100%;max-width:none;height:30vh;border-left:0;border-top:1px solid var(--line)}}
</style></head><body>
<header><h1>ATLAS</h1><span class="mono">time runs left (past) to right (future); scroll to see every excavation. Pinch, drag, double-tap or the + &minus; buttons on a row zoom that row; tap a numbered bubble to open the group. Switch to one shared axis to compare excavations</span>
<span><button class="tog on" id="axReal">Real-world time</button> <button class="tog" id="axNarr" disabled title="No narrative timelines yet">Narrative time</button></span>
<span><button class="tog on" id="viewTl">Timeline</button> <button class="tog" id="viewMap" title="Show events that have a place on a map">Map</button></span>
<span id="scaleWrap"><button class="tog on" id="scaleBtn" title="Switch between each excavation on its own time scale and all excavations on one shared axis">Each excavation on its own scale</button> <button id="ftog" onclick="document.getElementById('filters').classList.toggle('open')">Filters</button> <button id="fit">Fit all</button> <button id="zin">+</button> <button id="zout">&minus;</button></span></header>
<div id="filters"></div>
<main><div id="stage"><svg id="svg" role="img" aria-label="Timeline of events across the excavations"></svg><div id="mapbox" style="display:none;height:100%;position:relative"><div id="map" style="position:absolute;inset:0 0 44px 0"></div><div id="maptime" style="position:absolute;left:0;right:0;bottom:0;height:44px;padding:8px 14px;font:12px ui-monospace,monospace;background:var(--panel);border-top:1px solid var(--line)"><label>Show events up to <b id="asofLbl"></b> <input type="range" id="asof" style="width:60%;vertical-align:middle"></label> <span id="mapNote" class="note"></span></div></div></div>
<aside id="panel"><h2>Pick a dot</h2><p class="note">Each row is one excavation. Click a dot for what happened, how we know, and the source. Shapes show the kind of source; a dashed, pale dot means one source or a date only.</p>
<p class="note"><b>Zoom:</b> pinch or drag a row, double-tap it, use the + and &minus; buttons on the row (&#10226; resets it), or tap a numbered bubble to open that group of events.</p>
<p class="note">Rows share one time axis, so far-apart events in different excavations are visible side by side. Narrative time (when a story says something happened) is kept apart from real-world time and switches in once narrative events exist.</p></aside></main>
<script>
const DATA=__DATA__;
const KIND={data:'circle',document:'hex',official:'square',witness:'diamond',analysis:'down',media:'up'};
const SHAPE_LABEL={circle:'machine-recorded data',hex:'a primary document',square:'an official statement',diamond:'a person’s account',down:'a scholar’s account',up:'a news report'};
const NS='http://www.w3.org/2000/svg';const svg=document.getElementById('svg'),stage=document.getElementById('stage');
const state={scale:'own',axis:'real',off:new Set(),kinds:new Set(),statuses:new Set(),q:''};let W=800,H=500;
const allEv=DATA.flatMap(d=>d.events.map(e=>Object.assign({dig:d.id},e)));
let t0=Math.min(...allEv.map(e=>e.t)),t1=Math.max(...allEv.map(e=>e.e||e.t));const pad=(t1-t0)*0.04+86400000*30;t0-=pad;t1+=pad;
let view={a:t0,b:t1};const rowView={};let rowsGeo=[];const LW=()=>stage.clientWidth<600?100:150;const YEAR=365.2425*86400000;
function el(n,a,p){const x=document.createElementNS(NS,n);for(const k in a)x.setAttribute(k,a[k]);if(p)p.appendChild(x);return x}
function fmt(e){const d=new Date(e.t);const y=d.getUTCFullYear(),m=d.getUTCMonth(),dd=d.getUTCDate();const M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 const Y=v=>v<=0?(1-v)+' BCE':String(v);let s=e.p==='year'?Y(y):e.p==='month'?M[m]+' '+Y(y):dd+' '+M[m]+' '+Y(y);if(e.p==='exact'||e.p==='approx'){const hh=String(d.getUTCHours()).padStart(2,'0'),mm=String(d.getUTCMinutes()).padStart(2,'0');if(hh+mm!=='1200'&&hh+mm!=='0000')s+=' '+hh+':'+mm+' UTC'}
 if(e.e){const f=new Date(e.e);s+=' to '+(e.p==='year'?'':f.getUTCDate()+' '+M[f.getUTCMonth()]+' ')+Y(f.getUTCFullYear())}return s+(e.p==='approx'?' (approx.)':e.p==='range'?' (range)':'')}
const COL=i=>'var(--c'+(i%8)+')';
function marker(k,x,y,r,col,hollow,dash,g,ev){let s;const sw=1.6;const at={fill:hollow?'none':col,'fill-opacity':hollow?1:.85,stroke:col,'stroke-width':sw};if(dash)at['stroke-dasharray']='3 2';
 if(k==='circle')s=el('circle',Object.assign({cx:x,cy:y,r:r},at),g);else if(k==='square')s=el('rect',Object.assign({x:x-r,y:y-r,width:2*r,height:2*r,rx:2},at),g);
 else if(k==='diamond')s=el('polygon',Object.assign({points:`${x},${y-r*1.3} ${x+r*1.3},${y} ${x},${y+r*1.3} ${x-r*1.3},${y}`},at),g);
 else if(k==='down')s=el('polygon',Object.assign({points:`${x-r*1.2},${y-r} ${x+r*1.2},${y-r} ${x},${y+r*1.2}`},at),g);else if(k==='up')s=el('polygon',Object.assign({points:`${x-r*1.2},${y+r} ${x+r*1.2},${y+r} ${x},${y-r*1.2}`},at),g);
 else{const p=[];for(let i=0;i<6;i++){const a=Math.PI/3*i;p.push((x+r*1.2*Math.cos(a))+','+(y+r*1.2*Math.sin(a)))}s=el('polygon',Object.assign({points:p.join(' ')},at),g)}
 s.style.cursor='pointer';s.addEventListener('click',ev=>{ev.stopPropagation();show(g.__e)});return s}
function ticks(a,b,w){const H1=3600000,D1=86400000,out=[],need=84,span=b-a,Mn=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 const S=[['h',1],['h',3],['h',6],['h',12],['d',1],['d',2],['d',7],['d',14],['m',1],['m',3],['m',6],['y',1],['y',2],['y',5],['y',10],['y',25],['y',50],['y',100],['y',250],['y',500],['y',1000]];
 const dur=([u,n])=>u==='h'?n*H1:u==='d'?n*D1:u==='m'?n*30.44*D1:n*YEAR;
 let pick=S[S.length-1];for(const s of S){if(dur(s)/span*w>=need){pick=s;break}}const [u,n]=pick;
 if(u==='h'||u==='d'){const d=dur(pick);for(let tm=Math.floor(a/d)*d;tm<=b;tm+=d){if(tm<a)continue;const c=new Date(tm);
   out.push([tm,u==='h'?c.getUTCDate()+' '+Mn[c.getUTCMonth()]+' '+String(c.getUTCHours()).padStart(2,'0')+':00':c.getUTCDate()+' '+Mn[c.getUTCMonth()]+' '+c.getUTCFullYear()])}}
 else if(u==='m'){const A=new Date(a);let mi=A.getUTCFullYear()*12+Math.floor(A.getUTCMonth()/n)*n;for(;;mi+=n){const yy=Math.floor(mi/12),mm=mi-yy*12;const c=new Date(0);c.setUTCFullYear(yy,mm,1);c.setUTCHours(0,0,0,0);const tm=c.getTime();if(tm>b)break;if(tm>=a)out.push([tm,Mn[mm]+' '+(yy<=0?(1-yy)+' BCE':yy)])}}
 else{const A=new Date(a),B=new Date(b);const set=new Set();const k0=Math.floor(A.getUTCFullYear()/n)-1,k1=Math.ceil(B.getUTCFullYear()/n)+1;
  for(let k=Math.max(k0,1);k<=k1;k++)set.add(k*n);for(let k=1;k<=Math.ceil(-A.getUTCFullYear()/n)+2;k++)set.add(1-k*n);
  for(const yy of [...set].sort((p,q)=>p-q)){const c=new Date(0);c.setUTCFullYear(yy,0,1);c.setUTCHours(0,0,0,0);const tm=c.getTime();if(tm>b||tm<a)continue;out.push([tm,yy<=0?(1-yy)+' BCE':String(yy)])}}
 return out}
function passes(e){if(state.off.has(e.dig))return false;if(e.axis!==state.axis)return false;if(state.kinds.size&&!state.kinds.has(e.k))return false;if(state.statuses.size&&!state.statuses.has(e.st))return false;
 if(state.q){const s=(e.l+' '+e.d+' '+e.lane).toLowerCase();if(!s.includes(state.q))return false}return true}
state.view='tl';
function colOf(i){return getComputedStyle(document.documentElement).getPropertyValue('--c'+(i%8)).trim()||'#1f5fa8'}
let LM=null,mapObj=null,mapLayer=null;
function loadLeaflet(cb){if(window.L){cb();return}const c=document.createElement('link');c.rel='stylesheet';c.href='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css';document.head.appendChild(c);const s=document.createElement('script');s.src='https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js';s.onload=cb;s.onerror=()=>{document.getElementById('mapNote').textContent='The map library could not be loaded (needs an internet connection).'};document.head.appendChild(s)}
const placed=allEv.filter(e=>e.pl&&e.pl.lat!=null);
function setView(v){state.view=v;document.getElementById('viewTl').classList.toggle('on',v==='tl');document.getElementById('viewMap').classList.toggle('on',v==='map');
 document.getElementById('svg').style.display=v==='tl'?'block':'none';document.getElementById('mapbox').style.display=v==='map'?'block':'none';document.getElementById('scaleWrap').style.display=v==='tl'?'':'none';
 if(v==='map'){loadLeaflet(()=>{if(!mapObj){mapObj=L.map('map',{worldCopyJump:true}).setView([30,10],2);L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(mapObj);mapLayer=L.layerGroup().addTo(mapObj);
   const ts=placed.map(e=>e.t);const sl=document.getElementById('asof');sl.min=Math.min(...ts);sl.max=Math.max(...ts)+86400000;sl.step=1;sl.value=sl.max;sl.oninput=()=>drawMap(false)}drawMap(true)})}else draw()}
function drawMap(fit){if(!mapObj)return;mapLayer.clearLayers();const asof=+document.getElementById('asof').value;document.getElementById('asofLbl').textContent=fmt({t:asof,p:'day'});
 const evs=placed.filter(e=>passes(e)&&e.t<=asof);const pts=[];const groups={};
 for(const e of evs){const di=DATA.findIndex(d=>d.id===e.dig),col=colOf(di);const ll=[e.pl.lat,e.pl.lon];pts.push(ll);
  if(e.pl.uncertainty_km)L.circle(ll,{radius:e.pl.uncertainty_km*1000,color:col,weight:1,fillOpacity:.08}).addTo(mapLayer);
  const m=L.circleMarker(ll,{radius:8,color:col,weight:2,fillColor:col,fillOpacity:e.pl.precision==='exact'||e.pl.precision==='site'?.8:.35}).addTo(mapLayer);
  m.bindTooltip(fmt(e)+': '+e.l+' ('+e.pl.name+', '+e.pl.precision+')');m.on('click',()=>{show(e)});
  for(const o of e.ab||[]){(groups[o]=groups[o]||[]).push(e)}}
 for(const o in groups){const g=groups[o].sort((a,b)=>a.t-b.t);if(g.length>1)L.polyline(g.map(e=>[e.pl.lat,e.pl.lon]),{color:'#888',weight:2,dashArray:'5 6'}).addTo(mapLayer).bindTooltip('custody route: '+o)}
 document.getElementById('mapNote').textContent=evs.length+' of '+placed.length+' placed events. Faint circles and pale dots mean the place is approximate.';
 mapObj.invalidateSize();if(fit&&pts.length){setTimeout(()=>{mapObj.invalidateSize();mapObj.fitBounds(pts,{maxZoom:9,padding:[40,40]})},80)}}
function draw(){if(state.view==='map'){drawMap(false);return}W=stage.clientWidth;H=stage.clientHeight;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML='';rowsGeo=[];
 const L=LW(),R=14,T=34,pw=W-L-R;const X=t=>L+(t-view.a)/(view.b-view.a)*pw;
 const defs=el('g',{},svg);const digs=DATA.filter(d=>!state.off.has(d.id));
 // axis ticks
 const own=state.scale==='own';const tk=own?[]:ticks(view.a,view.b,pw);for(const [t,lab] of tk){const x=X(t);el('line',{x1:x,x2:x,y1:T-6,y2:H-4,stroke:'var(--line)','stroke-width':1},defs);const tx=el('text',{x:x+3,y:T-12,fill:'var(--mute)','font-size':11,'font-family':'ui-monospace,monospace'},defs);tx.textContent=lab}
 let y=T;const rowInfo=[];
 digs.forEach((d,ri)=>{const evs=d.events.filter(e=>passes(Object.assign({dig:d.id},e))).map(e=>Object.assign({dig:d.id},e));
  let rv=view;if(own){if(rowView[d.id])rv=rowView[d.id];else{const base=evs.length?evs:d.events.filter(e=>e.axis===state.axis);if(base.length){const a=Math.min(...base.map(e=>e.t)),b=Math.max(...base.map(e=>e.e||e.t));const pad=(b-a)*0.06+86400000*20;rv={a:a-pad,b:b+pad}}}}
  const Xr=tt=>L+(tt-rv.a)/(rv.b-rv.a)*pw,AX=own?18:0;
  const showLab=pw/((rv.b-rv.a)/YEAR)>40;
  const vis=evs.filter(e=>{const x=Xr(e.t),xe=e.e?Xr(e.e):x;return xe>=L-20&&x<=W+20});
  const levels=[];const place=[];const items=[];
  if(showLab){for(const e of vis){const x=Xr(e.t);let lv=0;while(lv<levels.length&&levels[lv]>x-14)lv++;if(lv===levels.length)levels.push(-1e9);levels[lv]=Math.max(x,e.e?Xr(e.e):x)+8+Math.min(e.l.length,46)*5.8+6;items.push({e,x,lv})}}
  else{let cur=null;for(const e of vis){const x=Xr(e.t);if(cur&&x-cur.lx<18){cur.es.push(e);cur.lx=x}else{cur={es:[e],x,lx:x};items.push(cur)}}levels.push(0)}
  const rh=Math.max(80,22+AX+levels.length*17);el('rect',{x:0,y:y,width:W,height:rh,fill:ri%2?'transparent':'rgba(128,128,128,.07)'},defs);
  const lab=el('text',{x:8,y:y+16,class:'rowlabel',fill:COL(DATA.indexOf(d))},defs);const words=d.title.split(' ');let line='',ln=0;for(const w of words){if((line+' '+w).length>(L<120?13:20)){const ts=el('tspan',{x:8,dy:ln?14:0},lab);ts.textContent=line;line=w;ln++;if(ln>2)break}else line=(line?line+' ':'')+w}if(ln<=2){const ts=el('tspan',{x:8,dy:ln?14:0},lab);ts.textContent=line}
  if(own){for(const [tm,lb] of ticks(rv.a,rv.b,pw)){const x=Xr(tm);el('line',{x1:x,x2:x,y1:y+2,y2:y+rh,stroke:'var(--line)','stroke-width':1},defs);const tx=el('text',{x:x+3,y:y+13,fill:'var(--mute)','font-size':10.5,'font-family':'ui-monospace,monospace'},defs);tx.textContent=lb}}
  lab.addEventListener('click',()=>{if(own){state.scale='shared';syncScale();zoomTo(d)}else zoomTo(d)});const cnt=el('text',{x:8,y:y+rh-6,fill:'var(--mute)','font-size':10.5,'font-family':'ui-monospace,monospace'},defs);cnt.textContent=evs.length<d.events.length?evs.length+' of '+d.events.length:String(evs.length);if(own){cnt.setAttribute('x',82);cnt.setAttribute('y',y+rh-10)}
  if(own){[['+',8,()=>zoomRow(d.id,.4,.5)],['\u2212',32,()=>zoomRow(d.id,2.5,.5)],['\u27f2',56,()=>{delete rowView[d.id];draw()}]].forEach(([s,bx,fn])=>{const b=el('g',{style:'cursor:pointer'},defs);el('rect',{x:bx,y:y+rh-24,width:20,height:20,rx:5,fill:'var(--panel)',stroke:'var(--line)'},b);const q=el('text',{x:bx+10,y:y+rh-9.5,'text-anchor':'middle','font-size':13,fill:s==='\u27f2'&&!rowView[d.id]?'var(--mute)':'var(--ink)'},b);q.textContent=s;b.addEventListener('click',ev=>{ev.stopPropagation();fn()})})}
  rowsGeo.push({id:d.id,y0:y,y1:y+rh,a:rv.a,b:rv.b});
  const clip=el('g',{},svg);
  for(const it of items){if(it.es&&it.es.length>1){const g=el('g',{style:'cursor:pointer'},clip);const col=COL(DATA.indexOf(d));const yy=y+30+AX;
    el('circle',{cx:it.x,cy:yy,r:11,fill:col,'fill-opacity':.88,stroke:'var(--bg)','stroke-width':2},g);const q=el('text',{x:it.x,y:yy+4,'text-anchor':'middle','font-size':11,'font-weight':700,fill:'var(--bg)'},g);q.textContent=it.es.length;
    const ti=el('title',{},g);ti.textContent=it.es.length+' events here: tap to zoom in';g.addEventListener('click',ev=>{ev.stopPropagation();openCluster(d.id,it.es,own)});continue}
   const e=it.e||it.es[0],lv=it.lv||0;const g=el('g',{},clip);g.__e=e;const x=Xr(e.t),yy=(it.es?y+30+AX:y+16+AX+lv*17);const col=COL(DATA.indexOf(d));
   if(e.win){const xa=Xr(e.win.a),xb=e.win.b==null?W:Xr(e.win.b);el('rect',{x:xa,y:yy-8,width:Math.max(4,xb-xa),height:16,rx:4,fill:col,'fill-opacity':.10,stroke:col,'stroke-dasharray':'2 3','stroke-opacity':.6},g);if(e.win.b==null)el('text',{x:W-14,y:yy+4,fill:col,'font-size':11},g).textContent='\u2192'}
   if(e.e){const xe=Xr(e.e);el('rect',{x:x,y:yy-3,width:Math.max(3,xe-x),height:6,fill:col,'fill-opacity':.25,stroke:col,'stroke-dasharray':'3 2'},g)}
   const dash=e.st==='single'||e.st==='inferred';
   marker(KIND[e.k]||'circle',x,yy,5,col,e.st==='inferred'||e.p==='year'||e.p==='month',dash,g);
   if(e.st==='disputed'){el('circle',{cx:x,cy:yy,r:9,fill:'none',stroke:'var(--c1)','stroke-width':1.5},g)}
   if(showLab){const tt=el('text',{x:x+9,y:yy+4,fill:'var(--ink)','font-size':11},g);tt.textContent=e.l.length>46?e.l.slice(0,44)+'\u2026':e.l;tt.style.pointerEvents='none'}
   g.addEventListener('mouseenter',()=>{svg.setAttribute('aria-description',e.l)});const ti=el('title',{},g);ti.textContent=fmt(e)+': '+e.l}
  y+=rh});
 if(!digs.length){const t=el('text',{x:L,y:60,fill:'var(--mute)'},svg);t.textContent='No excavation selected.'}
 const TH=Math.max(H,y+10);svg.setAttribute('viewBox',`0 0 ${W} ${TH}`);svg.style.height=TH+'px';svg.__ppy=pw}
function show(e){const d=DATA.find(x=>x.id===e.dig);const p=document.getElementById('panel');
 const links=[];if(e.link)links.push(`<a href="${e.link}" target="_blank" rel="noopener">Open the source</a>`);
 if(d.slug&&!window.ATLAS_PRIVATE)links.push(`<a href="../digs/${d.slug}/">Read the excavation</a>`);if(d.slug&&!window.ATLAS_PRIVATE)links.push(`<a href="../digs/${d.slug}/timeline/">Excavation timeline</a>`);
 p.innerHTML=`<p class="mono">${d.title}</p><h2>${esc(e.l)}</h2><p class="mono">${fmt(e)} · ${esc(e.lane)}</p><p>${esc(e.d)}</p>`+(e.alt?`<p class="note">Another source gives ${new Date(e.alt.t).toUTCString().slice(5,16)}: ${esc(e.alt.note)}</p>`:'')+
 (e.pl?`<p class="note">Place: <b>${esc(e.pl.name)}</b>${e.pl.lat!=null?' ('+e.pl.lat+', '+e.pl.lon+', '+esc(e.pl.precision)+')':''}${e.pl.note?'<br>'+esc(e.pl.note):''}${e.pl.source?'<br><span class="mono">'+esc(e.pl.source)+'</span>':''}</p>`:'')+(e.win?`<p class="note"><b>Time window:</b> ${fmt({t:e.win.a,p:'day'})} to ${e.win.b==null?'open (no end date)':fmt({t:e.win.b,p:'day'})}${e.win.cv?'<br>Certainly covers: '+fmt({t:e.win.cv[0],p:'day'})+' to '+fmt({t:e.win.cv[1],p:'day'}):''}<br>Start: ${esc(e.win.bn)}<br>End: ${esc(e.win.en)}</p>`:'')+(e.node&&e.co?`<p class="note">Date basis: <b>${esc(e.db||'not recorded')}</b> &middot; independent origins: <b>${e.co.independent}</b> (read directly: ${e.co.read})${e.co.declared?'':' &middot; independence not yet declared'}</p>`:'')+(e.node?`<p class="note">Shared node <b>${esc(e.node)}</b>${e.sh&&e.sh.length?' &middot; also used in: '+e.sh.map(s=>esc((DATA.find(x=>x.id===s)||{title:s}).title)).join(', '):''}</p>`:'')+`<p class="mono">kind: ${SHAPE_LABEL[KIND[e.k]]||e.k} · status: ${e.st}</p><p><b>Sources</b></p><ul>`+e.src.map(s=>`<li>${s.url?`<a href="${s.url}" target="_blank" rel="noopener">${esc(s.title)}</a>`:esc(s.title)}<br><span class="note">${esc(s.auth)}</span></li>`).join('')+`</ul><p>${links.join(' · ')}</p>`}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function zoomTo(d){const ev=d.events.filter(e=>e.axis===state.axis);if(!ev.length)return;const a=Math.min(...ev.map(e=>e.t)),b=Math.max(...ev.map(e=>e.e||e.t));const p=(b-a)*0.08+86400000*3;view={a:a-p,b:b+p};draw()}
function zoom(f,cx){const w=view.b-view.a,c=view.a+w*cx;const nw=Math.max(60000,Math.min(t1-t0,w*f));view={a:c-nw*cx,b:c+nw*(1-cx)};draw()}
function build(){const f=document.getElementById('filters');f.innerHTML='<span>excavations:</span>';DATA.forEach((d,i)=>{const b=document.createElement('button');b.className='chip';b.style.borderColor=COL(i);b.textContent=d.title;b.onclick=()=>{state.off.has(d.id)?state.off.delete(d.id):state.off.add(d.id);b.classList.toggle('off',state.off.has(d.id));draw()};f.appendChild(b)});
 const add=(label,set,vals)=>{const s=document.createElement('span');s.textContent=' '+label+':';f.appendChild(s);vals.forEach(v=>{const b=document.createElement('button');b.className='chip off';b.textContent=v;b.onclick=()=>{set.has(v)?set.delete(v):set.add(v);b.classList.toggle('off',!set.has(v));draw()};f.appendChild(b)})};
 add('kind',state.kinds,[...new Set(allEv.map(e=>e.k))]);add('status',state.statuses,[...new Set(allEv.map(e=>e.st))]);
 const q=document.createElement('input');q.type='search';q.placeholder='search events';q.oninput=()=>{state.q=q.value.toLowerCase();draw()};f.appendChild(q);
 if(allEv.some(e=>e.axis==='narrative')){const n=document.getElementById('axNarr');n.disabled=false;n.title='';n.onclick=()=>{state.axis='narrative';n.classList.add('on');document.getElementById('axReal').classList.remove('on');fitAll()};document.getElementById('axReal').onclick=()=>{state.axis='real';document.getElementById('axReal').classList.add('on');n.classList.remove('on');fitAll()}}}
function fitAll(){const ev=allEv.filter(e=>e.axis===state.axis);if(ev.length){let a=Math.min(...ev.map(e=>e.t)),b=Math.max(...ev.map(e=>e.e||e.t));const p=(b-a)*0.04+86400000*30;view={a:a-p,b:b+p}}draw()}
function syncScale(){stage.scrollTop=0;const b=document.getElementById('scaleBtn'),own=state.scale==='own';b.classList.toggle('on',own);b.textContent=own?'Each excavation on its own scale':'All excavations on one shared axis';
 for(const id of ['fit','zin','zout']){const x=document.getElementById(id);x.disabled=own;x.title=own?'Switch to the shared axis to zoom and compare digs':''}if(!own&&!window.__fitted){window.__fitted=1;fitAll();return}draw()}
document.getElementById('viewTl').onclick=()=>setView('tl');const vm=document.getElementById('viewMap');if(!placed.length){vm.disabled=true;vm.title='No event has a place yet'}else vm.onclick=()=>setView('map');
document.getElementById('scaleBtn').onclick=()=>{state.scale=state.scale==='own'?'shared':'own';syncScale()};
document.getElementById('fit').onclick=fitAll;document.getElementById('zin').onclick=()=>zoom(.5,.5);document.getElementById('zout').onclick=()=>zoom(2,.5);
svg.addEventListener('wheel',e=>{if(!(e.ctrlKey||e.metaKey||e.shiftKey))return;e.preventDefault();const r=svg.getBoundingClientRect();const cx=Math.min(1,Math.max(0,(e.clientX-r.left-LW())/(r.width-LW()-14)));const T=tgt(e.clientY);if(!T)return;if(T.key==='*')zoom(e.deltaY<0?.8:1.25,cx);else zoomRow(T.key,e.deltaY<0?.8:1.25,cx)},{passive:false});
function clampV(v){let w=v.b-v.a;const lo=3600000,hi=40000*YEAR;if(w<lo){const c=(v.a+v.b)/2;v={a:c-lo/2,b:c+lo/2}}if(w>hi){const c=(v.a+v.b)/2;v={a:c-hi/2,b:c+hi/2}}return v}
function getV(key){return key==='*'?view:(rowView[key]||(rowsGeo.find(r=>r.id===key)&&{a:rowsGeo.find(r=>r.id===key).a,b:rowsGeo.find(r=>r.id===key).b}))}
function setV(key,v){v=clampV(v);if(key==='*')view=v;else rowView[key]=v;draw()}
function zoomRow(id,f,cx){const v=getV(id);if(!v)return;const w=v.b-v.a,c=v.a+w*cx,nw=w*f;setV(id,{a:c-nw*cx,b:c+nw*(1-cx)})}
function openCluster(id,es,own){const a=Math.min(...es.map(e=>e.t)),b=Math.max(...es.map(e=>e.e||e.t));
 if(b-a<3600000){const p=document.getElementById('panel');p.innerHTML='<p class="mono">'+es.length+' events at about the same time</p><ul class="clist">'+es.map((e,i)=>'<li><a href="#" data-i="'+i+'">'+esc(e.l)+'</a><br><span class="note">'+esc(fmt(e))+'</span></li>').join('')+'</ul>';p.querySelectorAll('a[data-i]').forEach(x=>x.onclick=ev=>{ev.preventDefault();show(es[+x.dataset.i])});return}
 const pad=(b-a)*.2+3600000;setV(own?id:'*',{a:a-pad,b:b+pad})}
const ptrs=new Map();let G=null,moved=false;
function tgt(cy){if(state.scale!=='own')return{key:'*'};const r=svg.getBoundingClientRect(),y=cy-r.top;const g=rowsGeo.find(g=>y>=g.y0&&y<g.y1);return g?{key:g.id}:null}
function startG(){const ps=[...ptrs.values()];if(!ps.length){G=null;return}const mx=ps.reduce((s,p)=>s+p.x,0)/ps.length,my=ps.reduce((s,p)=>s+p.y,0)/ps.length;const T=tgt(my);if(!T){G=null;return}const v=getV(T.key);if(!v){G=null;return}
 G={key:T.key,v0:{a:v.a,b:v.b},x0:mx,d0:ps.length>1?Math.hypot(ps[0].x-ps[1].x,ps[0].y-ps[1].y):0,n:ps.length}}
svg.addEventListener('pointerdown',e=>{ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});moved=false;startG()});
window.addEventListener('pointerup',e=>{ptrs.delete(e.pointerId);startG()});window.addEventListener('pointercancel',e=>{ptrs.delete(e.pointerId);startG()});
window.addEventListener('pointermove',e=>{if(!ptrs.has(e.pointerId)||!G)return;ptrs.set(e.pointerId,{x:e.clientX,y:e.clientY});const ps=[...ptrs.values()];const pw=stage.clientWidth-LW()-14,L=LW();const r=svg.getBoundingClientRect();
 const mx=ps.reduce((s,p)=>s+p.x,0)/ps.length;const w0=G.v0.b-G.v0.a;
 if(ps.length>1&&G.d0){moved=true;const d=Math.hypot(ps[0].x-ps[1].x,ps[0].y-ps[1].y);const nw=w0*G.d0/Math.max(d,10);const tc=G.v0.a+((G.x0-r.left-L)/pw)*w0;setV(G.key,{a:tc-((mx-r.left-L)/pw)*nw,b:tc-((mx-r.left-L)/pw)*nw+nw})}
 else if(ps.length===1&&Math.abs(mx-G.x0)>5){moved=true;const dt=-(mx-G.x0)/pw*w0;setV(G.key,{a:G.v0.a+dt,b:G.v0.b+dt})}});
svg.addEventListener('click',e=>{if(moved){e.stopPropagation();e.preventDefault();moved=false}},true);
svg.addEventListener('dblclick',e=>{const T=tgt(e.clientY);if(!T)return;const r=svg.getBoundingClientRect();const cx=Math.min(1,Math.max(0,(e.clientX-r.left-LW())/(r.width-LW()-14)));if(T.key==='*')zoom(.4,cx);else zoomRow(T.key,.4,cx)});
window.addEventListener('resize',draw);build();fitAll();syncScale();
</script></body></html>"""

def build_atlas_html(subjects, private=False):
    data = load(subjects)
    page = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    if private: page = page.replace("<script>\nconst DATA", "<script>window.ATLAS_PRIVATE=true;\nconst DATA", 1)
    return page, data

if __name__ == "__main__":
    out = sys.argv[1]; allm = "--all" in sys.argv
    cfg = yaml.safe_load(open(os.path.join(ROOT, "build", "site.yaml")))
    subs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(SUBJ, "*", "timeline.yaml"))) if allm else cfg["publish"]
    page, data = build_atlas_html(subs, private=allm)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); open(out, "w", encoding="utf-8").write(page)
    print("atlas:", out, "|", len(data), "digs,", sum(len(d["events"]) for d in data), "events")
