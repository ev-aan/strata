# Import note: Teti Pyramid Texts dig (two batches)

Provenance: uploaded by the owner on 2026-10-02 as two zip files (`Teti.zip`: 11 files; `Teti2.zip`: 12 files), the output of the chat recorded in `SOURCE_CHAT.md`. Copied here **verbatim and unedited** into `batch1/` and `batch2/`. Corrections go in new entries, not edits.
Files: `subject.yaml`, `utterance_schema.yaml`, `utterances_index.yaml` and 8 utterance files (PT 1-7, 23, 32, 213, 217, 246, 273-274, 373) in batch 1; `utterances_index.yaml` and 11 utterance files (PT 247, 260, 301, 302, 304, 364, 427-435, 510, 534, 539, 570) in batch 2.

## Mechanical check run here (2026-10-02, PyYAML)
- **0 of 19 utterance files parse as shipped, and the batch 2 index does not parse.** Only `subject.yaml`, `utterance_schema.yaml` and the batch 1 index parse.
- **Cause (same in all 19):** a `ritual_class:` list is followed by a `note:` key at the same indent as the list items. In a scratch copy, rewriting that one block to `ritual_class: {classes: [...], note: ...}` makes 15 of 19 files parse; the other four (pt_246, pt_304, pt_364, pt_427_435) have a second indentation fault in a `reading:`/`scholar:` list. The batch 2 index has its new utterance entries appended as list items under a mapping key (`adding_utterances:`), so the YAML structure is wrong.
- The chat reported the files as built and gave line counts; nothing in it shows them parsed.
- **Primary text:** every utterance file has the hieroglyphic field marked `searched_gap` (19 of 19) and 15 of 19 mark the transliteration the same way. The record therefore contains no hieroglyphic text at all.
- **Evidence states** counted in the files: 3 `established`, 14 `contested`, 18 `proposed`; 65 translation entries.
- **Source quality:** Wikipedia is cited 26 times, Madain Project 7, Egypt Fun Tours 3, Memphis Tours 1, Dailynewsegypt 1. Under the project rule Wikipedia is orientation only and never an anchor; the tourism pages are not acceptable anchors.
- **Rights:** the translation entries (Faulkner 1969, Allen 2005, Mercer 1952) need checking for how much text is quoted before anything is published.

## What is not a blocker
The chat said Sethe's critical edition could not be fetched. It is on the Internet Archive (see SOURCE_CHAT.md review note 1), so the hieroglyphic anchor can be sourced from page images.

## Not done
No file was repaired or converted; no claim was checked against Sethe, Allen or Faulkner.
