#!/usr/bin/env python3
"""Mechanical syntax repair of the imported Teti files. Originals are never edited; this returns repaired TEXT.
Only indentation/structure is changed. No content is added or removed."""
import re

def fix_ritual_class(t):
    # `ritual_class:` list followed by a sibling `note:` at the list's indent is invalid YAML.
    # Rewrite to ritual_class: {classes: [...], note: ...} by nesting the list under `classes:`.
    out, lines, i = [], t.split("\n"), 0
    while i < len(lines):
        if lines[i].rstrip() == "ritual_class:":
            out.append(lines[i]); out.append("  classes:"); i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                out.append("  " + lines[i]); i += 1
            continue
        out.append(lines[i]); i += 1
    return "\n".join(out)

def fix_second_fault(t, path=""):
    # (a) `translation_disputes:` list followed by a sibling `note:` at the list's own indent: nest the list under `readings:`.
    lines, out, i = t.split("\n"), [], 0
    while i < len(lines):
        m = re.match(r"^(\s*)translation_disputes:\s*$", lines[i])
        if m:
            ind = m.group(1)
            out.append(lines[i]); out.append(ind + "  readings:"); i += 1
            while i < len(lines) and (lines[i].startswith(ind + "  - ") or lines[i].startswith(ind + "    ") and not lines[i].startswith(ind + "  note:")):
                out.append("  " + lines[i]); i += 1
            continue
        out.append(lines[i]); i += 1
    t = "\n".join(out)
    # (b) a quoted scalar followed by trailing text on the same line: quote the whole thing.
    t = re.sub(r'^(\s*reading: )"(\'I am Nut, the Granary\')" — (taking the epithet literally as agricultural storage)$', r'\1"\2 — \3"', t, flags=re.M)
    return t

def fix_index2(t):
    # batch 2 appended its utterance entries as list items under a mapping key (`adding_utterances:`).
    # Move that block (from the BATCH 2 marker to the next top-level key) to the end of the `utterances:` list.
    lines = t.split("\n")
    mk = next(i for i, l in enumerate(lines) if "BATCH 2 UTTERANCES" in l)
    end = next((i for i in range(mk + 1, len(lines)) if re.match(r"^[a-z_]+:", lines[i])), len(lines))
    block = lines[mk:end]
    rest = lines[:mk] + lines[end:]
    # insert before the `adding_utterances:` key (the end of the utterances list)
    at = next(i for i, l in enumerate(rest) if l.startswith("adding_utterances:"))
    # step back over the comment banner that precedes it
    while at > 0 and (rest[at - 1].startswith("#") or rest[at - 1].strip() == ""):
        at -= 1
    return "\n".join(rest[:at] + [""] + block + [""] + rest[at:])

def repair(path, text):
    if path.endswith("utterances_index.yaml") and "batch2" in path:
        text = fix_index2(text)
    if re.search(r"/pt_[0-9_]+\.yaml$", path):
        text = fix_ritual_class(text)
        text = fix_second_fault(text, path)
    return text
