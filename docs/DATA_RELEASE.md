# Data release (private for now)

Owner decision, 2026-10-02: data downloads stay private for the time being.

## What exists
`python3 build/tools/export_release.py` writes a release to `private/exports/<build-id>/`: CSV (nodes, sources, links, claims, claim-to-node), GeoJSON (placed nodes) and GraphML, with a README, SHA256 checksums and a build id.
`private/` is git-ignored, so nothing here is committed or published. The tool refuses to write anywhere else, the site builder does not read it, and the deploy workflow fails if the built site contains an export file.

## What it is not
- It is not a verified dataset. A node records what a source shows with its date; the judgement is in the claims (see the README inside each release).
- The checksum manifest is not signed. A signature proves the manifest is ours, and needs a key that only the owner should hold. Do not generate a release key in a cloud session: the session is thrown away. When you want to sign: create a key on your own computer, publish its fingerprint on the site, and run `gpg --armor --detach-sign SHA256SUMS.txt` on each release.

## Still public
Each excavation page links to its own `claims.yaml` and sources manifest, and the repository is the source of the whole record. Those are separate from this release. If you want those links taken down as well, say so.

## To open a release later
Move it out of `private/`, sign it, and add a download page generated from `build/site.yaml`. Until then, do neither.
