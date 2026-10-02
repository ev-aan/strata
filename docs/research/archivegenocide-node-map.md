# Research note: the Archive Genocide "Gaza Node Map" (read 2026-10-02)

Source read: https://archivegenocide.com/nodes/ (the page text, including its "How this was built" section) and the dataset README at /nodes/data/README.txt. Not read: the viewer's code, the data files, the footage, or the archive's other pages beyond the home page. Nothing on the site was checked against outside sources, and none of its claims about events is endorsed here. This note is about method.

## What it is
A graph viewer over an archive of 134,428 clips (videos and photos). Events (107,465) are clusters of clips; people, units, facilities and places are linked nodes; every link carries a stated reason and a grade. It is a finding aid over primary material, and its own README says so ("Nothing in it is verified reporting").

## About the source itself
It is an advocacy archive: it states its purpose as documentation for "legal accountability" and its titles use "genocide" as a settled description, which is a legal determination. Under our rules that is a source with a stated purpose (A-rules: test provenance, do not inherit its framing). The method below can be learned from without adopting its conclusions.

## Methods worth learning from
1. Events are built only from deterministic signals that can be recomputed (video fingerprint match, same post URL, same date and resolved place). Where a signal is missing the items stay apart, "because merging two distinct massacres into one node asserts something that did not happen".
2. Every link is graded: established (a deterministic signal) or possible (a lead, drawn dashed, never a finding). Every link carries a `why`.
3. Corroboration tiers count independent origins, not repeats: reposts of one file do not corroborate; separately filmed footage from separate archives does. The tier "describes corroboration within this archive, not truth".
4. Every date carries its basis (`date_source`: stated, post_proxy, retrospective_unknown). Most dates are publication dates and the README says so first.
5. Coordinates are place anchors resolved to a gazetteer id (OpenStreetMap), never produced by a model; events whose location is only inferred are left off the exported map and drawn hollow in the viewer.
6. Cumulative totals are held apart from per-incident figures so they cannot be summed; figures that were examined and rejected are published with the reason.
7. People are not merged on a short name: an identity node needs three or more name tokens.
8. Release integrity: a build id, SHA256SUMS for every file, a detached GPG signature, a published key fingerprint; open exports (CSV, GeoJSON, GraphML).
9. Viewer features: a query syntax (`cat:massacre place:rafah`), a basket and notes with export/import, shareable focus links (`#focus=<id>`), a no-JavaScript fallback listing every source, and a restricted assistant ("Iris") that helps navigate.

## Where Stratah already matches, and where it differs
- Matches: evidence kept apart from popularity; append-only history; sources before claims; a stated "what this is not"; place with source and precision (N9); shared nodes (N1 to N8).
- They are ahead on: automated, recomputable clustering at scale; graded links with reasons; independence-aware corroboration; date provenance; gazetteer ids; signed releases and open data exports; the explorer's query language and share links.
- We do something they do not: claim-level judgement (state, confidence, evidential weight, what would change it, anchors read directly), challenges answered in public, and a record of corrections. Their graph says what footage exists and how it connects; it deliberately does not say what is true.

## Candidates for Stratah (not decided)
- C1. Relations as graded links with a reason: `related: [{node, grade: established|possible, why}]`.
- C2. A `date_basis` on nodes: stated | derived | publication_proxy | inferred.
- C3. Independence-aware corroboration computed for each node from its sources (count independent origins, not citations), replacing the crude single/reported status.
- C4. Gazetteer ids for places (OSM or Pleiades), and a flag that keeps inferred places off the map by default.
- C5. A build id, checksums and a signed manifest for each release, plus GeoJSON and CSV exports of nodes.
- C6. A public "considered and rejected" list next to the challenges ledger.
- C7. Atlas: query syntax, share links to a node, saved baskets.
