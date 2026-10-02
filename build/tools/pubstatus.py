"""Rendering of publication status (build/SCHEMA.md, Publication status). Used by build_site.py.

Pure functions: they take already-loaded YAML and return HTML. They never decide a status; they show
what `publication:` in the manifest and `source_notices` / `flagged_sources` in claims.yaml say."""
import html

E = lambda s: html.escape(str(s if s is not None else ""))

LABEL = {"retracted": "Retracted source", "withdrawn": "Withdrawn source",
         "expression_of_concern": "Source with an expression of concern",
         "corrected": "Corrected source", "unpublished": "Unpublished source"}


def pub_of(manifest, sid):
    s = manifest.get(sid) or {}
    p = s.get("publication")
    return p if isinstance(p, dict) and p.get("status") else None


def _notice_ref(n):
    n = " ".join(str(n or "").split())
    return f'<a href="{E(n)}">{E(n)}</a>' if n.startswith(("http://", "https://")) else E(n)


def _detail(p):
    bits = []
    if p.get("date"):
        bits.append(f'Notice dated {E(p["date"])}.')
    if p.get("reason"):
        bits.append(E(" ".join(str(p["reason"]).split())))
    if p.get("notice"):
        bits.append("Notice: " + _notice_ref(p["notice"]))
    return " ".join(bits)


def claim_notice_html(c, manifest):
    """A visible notice on a claim that lists `flagged_sources`. Empty string when it lists none."""
    out = ""
    for sid in c.get("flagged_sources") or []:
        p = pub_of(manifest, sid)
        label = LABEL.get(p["status"], "Source with a recorded publication status") if p else "Source flagged (status not recorded)"
        title = (manifest.get(sid) or {}).get("title") or sid
        out += (f'<div class="pubnote" role="note"><b>{E(label)}.</b> This claim cites '
                f'<a href="#{E(sid)}">{E(" ".join(str(title).split()))}</a>. ' + (_detail(p) if p else "") + '</div>')
    return out


def notices_html(d, manifest):
    """The `source_notices` list shown first on the page. Empty string when there are none."""
    items = ""
    for n in d.get("source_notices") or []:
        if not isinstance(n, dict):
            continue
        sid = n.get("source")
        p = pub_of(manifest, sid)
        label = LABEL.get(p["status"], "Source notice") if p else "Source notice"
        items += (f'<li><b>{E(label)}.</b> {E(" ".join(str(n.get("notice", "")).split()))} '
                  f'<a class="small" href="#{E(sid)}">The source</a></li>')
    if not items:
        return ""
    return ('<section class="pubnote" aria-label="Source notices"><p><b>Source notices.</b> '
            'Some sources this page discusses are retracted, corrected or unpublished.</p>'
            f'<ul class="l">{items}</ul></section>')


def source_li_extra(s):
    """Tag and id for one entry of the Sources list. ('', '') when no status is recorded."""
    p = s.get("publication") if isinstance(s.get("publication"), dict) else None
    if not p or not p.get("status"):
        return "", ""
    st = str(p["status"]).replace("_", " ")
    when = f' {E(p["date"])}' if p.get("date") and p["status"] != "published" else ""
    chk = f' (looked up {E(p["checked"])})' if p.get("checked") else ""
    return f' <span class="small">· publication: <b>{E(st)}</b>{when}{chk}</span>', f' id="{E(s.get("id"))}"'


def sources_note(manifest_list):
    """One sentence under the Sources heading, only for a dig that records any publication status."""
    if not any(isinstance(s.get("publication"), dict) for s in manifest_list):
        return ""
    return ('<p class="small">Publication status is recorded only for sources someone looked up. '
            'A source with no status shown has not been checked for a retraction or correction; that is not the same as clean.</p>')
