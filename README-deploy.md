# Pushing Strata online

Two paths. Pick one. **GitHub Pages** is recommended — it keeps your
existing CI and the new deploy in a single pipeline, no new accounts.

The principle stays intact in both: **the validation gate runs before
publish, so a dirty corpus can never reach the live site.** Conformance
and tests are deploy blockers, not advisory checks.

---

## Path A — GitHub Pages (recommended)

1. **Drop in the files** (paths relative to repo root):
   - `.github/workflows/deploy.yml`
   - Add the `.nojekyll` line to `build.py` (see `build/nojekyll_snippet.py`).

2. **Add a `requirements.txt`** at the repo root if you don't have one:
   ```
   pyyaml
   ```
   (List anything else the validator/build imports.)

3. **Turn on Pages**: repo → Settings → Pages → "Build and deployment" →
   Source: **GitHub Actions**. (Not "Deploy from a branch" — the workflow
   handles it.)

4. **Push to `main`.** Watch the Actions tab. Order is
   validate → build → deploy. The live URL appears on the `deploy` job
   when it finishes: `https://<user>.github.io/<repo>/`.

5. **Check the test invocation** in `deploy.yml` (the "Run validator test
   suite" step). I guessed at `tests/run.py` and `pytest`. Edit that one
   step to match how your 21-test suite actually runs, then push again.

### Custom domain (optional)
Settings → Pages → Custom domain. Add a `CNAME` file containing the
domain to the repo root (or let the UI create it). Point a DNS `CNAME`
record at `<user>.github.io`. Pages provisions HTTPS automatically.

---

## Path B — Netlify (one-file alternative)

1. Drop `netlify.toml` at the repo root.
2. netlify.com → "Add new site" → "Import from Git" → pick the repo.
3. It reads `netlify.toml` for build command + publish dir. Deploy.
4. Custom domain + HTTPS are handled in the Netlify dashboard.

Netlify rebuilds on every push and refuses to publish if the gate fails.

---

## What to confirm before the first green deploy

These are the spots where my memory of the repo might not match the
live field names / entry points. Each is a one-line edit:

- [ ] **Test command** — does the suite run via `pytest`, `tests/run.py`,
      `python -m tests`, or something else? Fix the validate step.
- [ ] **Conformance entry point** — workflow calls `python build/conformance.py`.
      Confirm that path.
- [ ] **Build entry point** — workflow calls `python build.py --all`.
      Confirm `--all` is the live flag.
- [ ] **Output dir** — workflow publishes `site/`. Confirm `build.py`
      writes there.
- [ ] **`.nojekyll`** — added to `build.py` output (Pages only).
- [ ] **`# RECONCILE` flags** — the four open contract decisions. The gate
      will deploy a corpus that still carries them; that's fine for going
      live, but they remain real until the full-repo conformance run closes
      them. Going online doesn't resolve them — flagging so it's a choice,
      not an oversight.

---

## How this maps to the architecture

The deploy pipeline is itself a small expression of the Strata discipline:
the build does not publish on the strength of "it probably still works"
(adoption weight). It publishes only on a passing material check —
conformance + tests (evidential weight). If you ever find yourself tempted
to add `continue-on-error: true` to the validate job to "just get it live,"
that's the disease asking for a costume. Don't.
