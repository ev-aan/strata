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
                        "alt": ({"t": ms(e["alt_time"]), "note": e.get("alt_note", "")} if e.get("alt_time") else None)})
        if evs: data.append({"id": sub, "title": title_dig, "tl_title": tl.get("title", ""), "slug": slug, "events": sorted(evs, key=lambda x: x["t"])})
    return data

TEMPLATE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Atlas: events across the digs</title>
<meta name="description" content="Every dated event in the Stratah digs on one zoomable timeline, left to right from past to future, filterable, each dot linking to its source.">
<style>
:root{--bg:#F5F2EC;--panel:#fff;--ink:#1A1814;--mid:#4A4640;--mute:#6f6962;--line:rgba(26,24,20,.16);--c0:#1f5fa8;--c1:#a8541a;--c2:#2a7a5a;--c3:#8a3b72;--c4:#6a6a2a;--c5:#a02c3c;--c6:#2c6f8f;--c7:#7a5a1a}
@media (prefers-color-scheme:dark){:root{--bg:#16150f;--panel:#1d1b14;--ink:#ece8de;--mid:#c3beb2;--mute:#a09a8d;--line:rgba(236,232,222,.2);--c0:#6fb0ff;--c1:#ffa24a;--c2:#5ccaa5;--c3:#e08cc8;--c4:#cfcf6a;--c5:#ff8a98;--c6:#7cc7ea;--c7:#e0bd6a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Georgia,sans-serif;display:flex;flex-direction:column;height:100vh}
header{padding:10px 16px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}h1{font:500 18px Georgia,serif;margin:0;letter-spacing:.04em}
.tog,.chip,button{font:12px ui-monospace,monospace;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:99px;padding:3px 11px;cursor:pointer}.chip.off{opacity:.35}.tog.on{background:var(--ink);color:var(--bg)}button:disabled,.tog:disabled{opacity:.4;cursor:not-allowed}
#filters{padding:6px 16px;border-bottom:1px solid var(--line);display:flex;flex-wrap:wrap;gap:6px;align-items:center;font:12px ui-monospace,monospace;color:var(--mute)}
input[type=search]{font:13px system-ui;padding:3px 10px;border:1px solid var(--line);border-radius:99px;background:var(--panel);color:var(--ink);width:170px}
main{flex:1;display:flex;min-height:0}#stage{flex:1;min-width:0;position:relative;overflow:hidden;touch-action:none}svg{width:100%;height:100%;display:block;cursor:grab}svg:active{cursor:grabbing}
#panel{width:340px;max-width:44vw;border-left:1px solid var(--line);background:var(--panel);padding:14px;overflow:auto;font-size:14px}#panel h2{font:500 16px Georgia,serif;margin:.2em 0 .4em}.mono{font:11.5px ui-monospace,monospace;color:var(--mute)}
a{color:var(--c0)}.note{color:var(--mute);font-size:13px}.rowlabel{font:600 12px system-ui;cursor:pointer}
@media (max-width:760px){#filters{display:none}#filters.open{display:flex;max-height:34vh;overflow:auto}main{flex-direction:column}#panel{width:100%;max-width:none;height:30vh;border-left:0;border-top:1px solid var(--line)}}
</style></head><body>
<header><h1>ATLAS</h1><span class="mono">time runs left (past) to right (future); wheel or pinch to zoom, drag to pan</span>
<span><button class="tog on" id="axReal">Real-world time</button> <button class="tog" id="axNarr" disabled title="No narrative timelines yet">Narrative time</button></span>
<span><button id="ftog" onclick="document.getElementById('filters').classList.toggle('open')">Filters</button> <button id="fit">Fit all</button> <button id="zin">+</button> <button id="zout">&minus;</button></span></header>
<div id="filters"></div>
<main><div id="stage"><svg id="svg" role="img" aria-label="Timeline of events across the digs"></svg></div>
<aside id="panel"><h2>Pick a dot</h2><p class="note">Each row is one dig. Click a dot for what happened, how we know, and the source. Shapes show the kind of source; a dashed, pale dot means one source or a date only.</p>
<p class="note">Rows share one time axis, so far-apart events in different digs are visible side by side. Narrative time (when a story says something happened) is kept apart from real-world time and switches in once narrative events exist.</p></aside></main>
<script>
const DATA=__DATA__;
const KIND={data:'circle',document:'hex',official:'square',witness:'diamond',analysis:'down',media:'up'};
const SHAPE_LABEL={circle:'machine-recorded data',hex:'a primary document',square:'an official statement',diamond:'a person’s account',down:'a scholar’s account',up:'a news report'};
const NS='http://www.w3.org/2000/svg';const svg=document.getElementById('svg'),stage=document.getElementById('stage');
const state={axis:'real',off:new Set(),kinds:new Set(),statuses:new Set(),q:''};let W=800,H=500;
const allEv=DATA.flatMap(d=>d.events.map(e=>Object.assign({dig:d.id},e)));
let t0=Math.min(...allEv.map(e=>e.t)),t1=Math.max(...allEv.map(e=>e.e||e.t));const pad=(t1-t0)*0.04+86400000*30;t0-=pad;t1+=pad;
let view={a:t0,b:t1};const YEAR=365.2425*86400000;
function el(n,a,p){const x=document.createElementNS(NS,n);for(const k in a)x.setAttribute(k,a[k]);if(p)p.appendChild(x);return x}
function fmt(e){const d=new Date(e.t);const y=d.getUTCFullYear(),m=d.getUTCMonth(),dd=d.getUTCDate();const M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 const Y=v=>v<=0?(1-v)+' BCE':String(v);let s=e.p==='year'?Y(y):e.p==='month'?M[m]+' '+y:dd+' '+M[m]+' '+y;if(e.p==='exact'||e.p==='approx'){const hh=String(d.getUTCHours()).padStart(2,'0'),mm=String(d.getUTCMinutes()).padStart(2,'0');if(hh+mm!=='1200'&&hh+mm!=='0000')s+=' '+hh+':'+mm+' UTC'}
 if(e.e){const f=new Date(e.e);s+=' to '+(e.p==='year'?'':f.getUTCDate()+' '+M[f.getUTCMonth()]+' ')+Y(f.getUTCFullYear())}return s+(e.p==='approx'?' (approx.)':e.p==='range'?' (range)':'')}
const COL=i=>'var(--c'+(i%8)+')';
function marker(k,x,y,r,col,hollow,dash,g,ev){let s;const sw=1.6;const at={fill:hollow?'none':col,'fill-opacity':hollow?1:.85,stroke:col,'stroke-width':sw};if(dash)at['stroke-dasharray']='3 2';
 if(k==='circle')s=el('circle',Object.assign({cx:x,cy:y,r:r},at),g);else if(k==='square')s=el('rect',Object.assign({x:x-r,y:y-r,width:2*r,height:2*r,rx:2},at),g);
 else if(k==='diamond')s=el('polygon',Object.assign({points:`${x},${y-r*1.3} ${x+r*1.3},${y} ${x},${y+r*1.3} ${x-r*1.3},${y}`},at),g);
 else if(k==='down')s=el('polygon',Object.assign({points:`${x-r*1.2},${y-r} ${x+r*1.2},${y-r} ${x},${y+r*1.2}`},at),g);else if(k==='up')s=el('polygon',Object.assign({points:`${x-r*1.2},${y+r} ${x+r*1.2},${y+r} ${x},${y-r*1.2}`},at),g);
 else{const p=[];for(let i=0;i<6;i++){const a=Math.PI/3*i;p.push((x+r*1.2*Math.cos(a))+','+(y+r*1.2*Math.sin(a)))}s=el('polygon',Object.assign({points:p.join(' ')},at),g)}
 s.style.cursor='pointer';s.addEventListener('click',ev=>{ev.stopPropagation();show(g.__e)});return s}
function ticks(a,b,w){const ppy=w/((b-a)/YEAR);let unit,step;const out=[];
 if(ppy>2400){unit='day';step=1}else if(ppy>180){unit='month';step=1}else if(ppy>60){unit='year';step=1}else if(ppy>25){unit='year';step=5}else if(ppy>6){unit='year';step=10}else if(ppy>2.5){unit='year';step=25}else if(ppy>0.6){unit='year';step=100}else if(ppy>0.25){unit='year';step=250}else if(ppy>0.12){unit='year';step=500}else{unit='year';step=1000}
 const A=new Date(a);let y=A.getUTCFullYear(),m=A.getUTCMonth(),d=A.getUTCDate();
 if(unit==='year'){const set=new Map();const k0=Math.floor(A.getUTCFullYear()/step)-1,k1=Math.ceil(new Date(b).getUTCFullYear()/step)+1;
  for(let k=Math.max(k0,1);k<=k1;k++){set.set(k*step,k*step)} for(let k=-k1-1;k<=-k0+1;k++){if(k>0)set.set(1-k*step,1-k*step)}
  for(const yy of [...set.keys()].sort((p,q)=>p-q)){const tt=new Date(0);tt.setUTCFullYear(yy,0,1);const tm=tt.getTime();if(tm>b||tm<a)continue;out.push([tm,yy<=0?(1-yy)+' BCE':String(yy)])}}
 else if(unit==='month'){const M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];const c=new Date(Date.UTC(y,m,1));while(c.getTime()<=b){if(c.getTime()>=a)out.push([c.getTime(),M[c.getUTCMonth()]+' '+c.getUTCFullYear()]);c.setUTCMonth(c.getUTCMonth()+1)}}
 else{const c=new Date(Date.UTC(y,m,d));while(c.getTime()<=b){if(c.getTime()>=a)out.push([c.getTime(),c.getUTCDate()+' '+c.toLocaleString('en',{month:'short',timeZone:'UTC'})+' '+c.getUTCFullYear()]);c.setUTCDate(c.getUTCDate()+1)}}
 return out}
function passes(e){if(state.off.has(e.dig))return false;if(e.axis!==state.axis)return false;if(state.kinds.size&&!state.kinds.has(e.k))return false;if(state.statuses.size&&!state.statuses.has(e.st))return false;
 if(state.q){const s=(e.l+' '+e.d+' '+e.lane).toLowerCase();if(!s.includes(state.q))return false}return true}
function draw(){W=stage.clientWidth;H=stage.clientHeight;svg.setAttribute('viewBox',`0 0 ${W} ${H}`);svg.innerHTML='';
 const L=150,R=14,T=34,pw=W-L-R;const X=t=>L+(t-view.a)/(view.b-view.a)*pw;
 const defs=el('g',{},svg);const digs=DATA.filter(d=>!state.off.has(d.id));
 // axis ticks
 const tk=ticks(view.a,view.b,pw);for(const [t,lab] of tk){const x=X(t);el('line',{x1:x,x2:x,y1:T-6,y2:H-4,stroke:'var(--line)','stroke-width':1},defs);const tx=el('text',{x:x+3,y:T-12,fill:'var(--mute)','font-size':11,'font-family':'ui-monospace,monospace'},defs);tx.textContent=lab}
 let y=T;const rowInfo=[];
 digs.forEach((d,ri)=>{const evs=d.events.filter(e=>passes(Object.assign({dig:d.id},e))).map(e=>Object.assign({dig:d.id},e));
  const vis=evs.filter(e=>{const x=X(e.t),xe=e.e?X(e.e):x;return xe>=L-20&&x<=W+20});
  const levels=[];const place=[];for(const e of vis){const x=X(e.t);let lv=0;while(lv<levels.length&&levels[lv]>x-14)lv++;if(lv===levels.length)levels.push(-1e9);levels[lv]=Math.max(x,e.e?X(e.e):x)+8;place.push([e,lv])}
  const rh=Math.max(46,22+levels.length*17);el('rect',{x:0,y:y,width:W,height:rh,fill:ri%2?'transparent':'rgba(128,128,128,.07)'},defs);
  const lab=el('text',{x:8,y:y+16,class:'rowlabel',fill:COL(DATA.indexOf(d))},defs);const words=d.title.split(' ');let line='',ln=0;for(const w of words){if((line+' '+w).length>20){const ts=el('tspan',{x:8,dy:ln?14:0},lab);ts.textContent=line;line=w;ln++;if(ln>2)break}else line=(line?line+' ':'')+w}if(ln<=2){const ts=el('tspan',{x:8,dy:ln?14:0},lab);ts.textContent=line}
  lab.addEventListener('click',()=>zoomTo(d));const cnt=el('text',{x:8,y:y+rh-6,fill:'var(--mute)','font-size':10.5,'font-family':'ui-monospace,monospace'},defs);cnt.textContent=evs.length+' of '+d.events.length+' events';
  const clip=el('g',{},svg);
  for(const [e,lv] of place){const g=el('g',{},clip);g.__e=e;const x=X(e.t),yy=y+16+lv*17;const col=COL(DATA.indexOf(d));
   if(e.e){const xe=X(e.e);el('rect',{x:x,y:yy-3,width:Math.max(3,xe-x),height:6,fill:col,'fill-opacity':.25,stroke:col,'stroke-dasharray':'3 2'},g)}
   const hollow=['day','month','year','approx'].includes(e.p)&&e.st!=='reported';const dash=e.st==='single'||e.st==='inferred';
   marker(KIND[e.k]||'circle',x,yy,5,col,e.st==='inferred'||e.p==='year'||e.p==='month',dash,g);
   if(e.st==='disputed'){el('circle',{cx:x,cy:yy,r:9,fill:'none',stroke:'var(--c1)','stroke-width':1.5},g)}
   if(pw/((view.b-view.a)/YEAR)>40){const tt=el('text',{x:x+9,y:yy+4,fill:'var(--ink)','font-size':11},g);tt.textContent=e.l.length>46?e.l.slice(0,44)+'…':e.l;tt.style.pointerEvents='none'}
   g.addEventListener('mouseenter',()=>{svg.setAttribute('aria-description',e.l)});const ti=el('title',{},g);ti.textContent=fmt(e)+': '+e.l}
  y+=rh});
 if(!digs.length){const t=el('text',{x:L,y:60,fill:'var(--mute)'},svg);t.textContent='No dig selected.'}
 svg.setAttribute('height',Math.max(H,y+10));svg.__ppy=pw}
function show(e){const d=DATA.find(x=>x.id===e.dig);const p=document.getElementById('panel');
 const links=[];if(e.link)links.push(`<a href="${e.link}" target="_blank" rel="noopener">Open the source</a>`);
 if(d.slug&&!window.ATLAS_PRIVATE)links.push(`<a href="../digs/${d.slug}/">Read the dig</a>`);if(d.slug&&!window.ATLAS_PRIVATE)links.push(`<a href="../digs/${d.slug}/timeline/">Dig timeline</a>`);
 p.innerHTML=`<p class="mono">${d.title}</p><h2>${esc(e.l)}</h2><p class="mono">${fmt(e)} · ${esc(e.lane)}</p><p>${esc(e.d)}</p>`+(e.alt?`<p class="note">Another source gives ${new Date(e.alt.t).toUTCString().slice(5,16)}: ${esc(e.alt.note)}</p>`:'')+
 `<p class="mono">kind: ${SHAPE_LABEL[KIND[e.k]]||e.k} · status: ${e.st}</p><p><b>Sources</b></p><ul>`+e.src.map(s=>`<li>${s.url?`<a href="${s.url}" target="_blank" rel="noopener">${esc(s.title)}</a>`:esc(s.title)}<br><span class="note">${esc(s.auth)}</span></li>`).join('')+`</ul><p>${links.join(' · ')}</p>`}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]))}
function zoomTo(d){const ev=d.events.filter(e=>e.axis===state.axis);if(!ev.length)return;const a=Math.min(...ev.map(e=>e.t)),b=Math.max(...ev.map(e=>e.e||e.t));const p=(b-a)*0.08+86400000*3;view={a:a-p,b:b+p};draw()}
function zoom(f,cx){const w=view.b-view.a,c=view.a+w*cx;const nw=Math.max(60000,Math.min(t1-t0,w*f));view={a:c-nw*cx,b:c+nw*(1-cx)};draw()}
function build(){const f=document.getElementById('filters');f.innerHTML='<span>digs:</span>';DATA.forEach((d,i)=>{const b=document.createElement('button');b.className='chip';b.style.borderColor=COL(i);b.textContent=d.title;b.onclick=()=>{state.off.has(d.id)?state.off.delete(d.id):state.off.add(d.id);b.classList.toggle('off',state.off.has(d.id));draw()};f.appendChild(b)});
 const add=(label,set,vals)=>{const s=document.createElement('span');s.textContent=' '+label+':';f.appendChild(s);vals.forEach(v=>{const b=document.createElement('button');b.className='chip off';b.textContent=v;b.onclick=()=>{set.has(v)?set.delete(v):set.add(v);b.classList.toggle('off',!set.has(v));draw()};f.appendChild(b)})};
 add('kind',state.kinds,[...new Set(allEv.map(e=>e.k))]);add('status',state.statuses,[...new Set(allEv.map(e=>e.st))]);
 const q=document.createElement('input');q.type='search';q.placeholder='search events';q.oninput=()=>{state.q=q.value.toLowerCase();draw()};f.appendChild(q);
 if(allEv.some(e=>e.axis==='narrative')){const n=document.getElementById('axNarr');n.disabled=false;n.title='';n.onclick=()=>{state.axis='narrative';n.classList.add('on');document.getElementById('axReal').classList.remove('on');fitAll()};document.getElementById('axReal').onclick=()=>{state.axis='real';document.getElementById('axReal').classList.add('on');n.classList.remove('on');fitAll()}}}
function fitAll(){const ev=allEv.filter(e=>e.axis===state.axis);if(ev.length){let a=Math.min(...ev.map(e=>e.t)),b=Math.max(...ev.map(e=>e.e||e.t));const p=(b-a)*0.04+86400000*30;view={a:a-p,b:b+p}}draw()}
document.getElementById('fit').onclick=fitAll;document.getElementById('zin').onclick=()=>zoom(.5,.5);document.getElementById('zout').onclick=()=>zoom(2,.5);
svg.addEventListener('wheel',e=>{e.preventDefault();const r=svg.getBoundingClientRect();const cx=Math.min(1,Math.max(0,(e.clientX-r.left-150)/(r.width-164)));zoom(e.deltaY<0?.8:1.25,cx)},{passive:false});
let drag=null;svg.addEventListener('pointerdown',e=>{drag={x:e.clientX,a:view.a,b:view.b}});window.addEventListener('pointerup',()=>drag=null);
window.addEventListener('pointermove',e=>{if(!drag)return;const pw=stage.clientWidth-164;const dt=-(e.clientX-drag.x)/pw*(drag.b-drag.a);view={a:drag.a+dt,b:drag.b+dt};draw()});
window.addEventListener('resize',draw);build();fitAll();
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
