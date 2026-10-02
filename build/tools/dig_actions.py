"""Links that let a signed-in contributor start work on an open step of a dig.

Used by build_site.py. "Start this step" opens a pre-filled GitHub issue (form: .github/ISSUE_TEMPLATE/dig-step.yml).
GitHub handles sign-in. If the person has write access, the dig agent (.github/workflows/dig-agent.yml) picks it up.
Anyone else's issue stays a plain suggestion for a maintainer."""
import html
from urllib.parse import urlencode

REPO = "https://github.com/ev-aan/stratah"


def _clean(s):
    return " ".join(str(s or "").split())


def start_url(subject, claim_id, step):
    q = {"template": "dig-step.yml", "title": f"Dig step: {subject}" + (f" / {claim_id}" if claim_id else ""),
         "subject": subject, "claim": claim_id or "", "next_step": _clean(step)[:1500]}
    return f"{REPO}/issues/new?{urlencode(q)}"


def start_link(subject, claim):
    """HTML link for a claim that has open work (a next_step), or "" if there is none."""
    step = claim.get("next_step")
    if not step or not subject:
        return ""
    url = html.escape(start_url(subject, claim.get("id"), step))
    return (f'<p class="small"><a href="{url}" rel="nofollow">Start this step &rarr;</a> '
            f'(signs you in with GitHub; trusted contributors can send it to the dig agent)</p>')
