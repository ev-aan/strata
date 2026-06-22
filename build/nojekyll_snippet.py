# ----------------------------------------------------------------------
# ADD THIS to build.py, at the end of whatever writes the site/ directory
# (after site/index.html and any per-subject pages are written).
#
# WHY: GitHub Pages runs Jekyll by default, which ignores files/folders
# beginning with "_" and can mangle output. An empty .nojekyll disables it.
# Harmless for Netlify/local. One line, no downside.
# ----------------------------------------------------------------------

from pathlib import Path

def finalize_site(site_dir: str = "site") -> None:
    out = Path(site_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / ".nojekyll").write_text("")  # disable Jekyll on Pages

# Call finalize_site("site") as the last line of your build, e.g.:
#
#   if __name__ == "__main__":
#       ...                      # existing arg parsing + per-subject build
#       finalize_site("site")    # <-- add this
