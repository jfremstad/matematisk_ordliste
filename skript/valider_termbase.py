#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import re
from collections import defaultdict

LINE_BREAK = "<br>"
ERR_INCOMPLETE = 1
ERR_NONSTANDARD = 2
ERR_DUPLICATES = 4
ERR_OVERLAP = 8

line_break_pattern = re.compile(r"((\r)?\n|<\s*br\s*/?>)", re.IGNORECASE)


def normalize_linebreaks(s):
    return line_break_pattern.sub(LINE_BREAK, s)


def trim(s):
    return " ".join(s.split())


from functools import cmp_to_key


def synonym_cmp(a, b):
    if a.lower() < b.lower():
        return -1
    if a.lower() > b.lower():
        return 1
    if a.startswith(b) and a != b:
        return -1
    if b.startswith(a) and a != b:
        return 1
    return 0


def standardize_synonyms(cell):
    cell = normalize_linebreaks(cell)
    parts = [trim(x) for x in cell.split(LINE_BREAK)]
    parts = [x for x in parts if x]
    parts = sorted(set(parts), key=cmp_to_key(synonym_cmp))
    return LINE_BREAK.join(parts)


def load_yaml(path):
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except:
        sys.exit("FEIL: kunne ikke lese YAML.")


def flatten(entry):
    t = entry.get("tillatt", {})
    return (
        t.get("bokmål", "").strip(),
        t.get("nynorsk", "").strip(),
        t.get("engelsk", "").strip(),
    )


def check_overlap(data):
    # check overlap between tillatt and anbefalt
    errors = []
    for idx, entry in enumerate(data, start=1):
        t = entry.get("tillatt", {})
        a = entry.get("anbefalt", {})

        for lang in ("bokmål", "nynorsk", "engelsk"):
            till = t.get(lang, "")
            anbef = a.get(lang, "")
            if not till or not anbef:
                continue

            till_set = {x.strip() for x in normalize_linebreaks(till).split(LINE_BREAK)}
            anbef_set = {
                x.strip() for x in normalize_linebreaks(anbef).split(LINE_BREAK)
            }

            overlap = till_set & anbef_set
            if overlap:
                errors.append((idx, lang, sorted(overlap)))

    return errors


def check_nonstandard(rows):
    problems = []
    for i, row in enumerate(rows):
        for c, cell in enumerate(row):
            std = standardize_synonyms(cell)
            if std != cell:
                problems.append((i, c, cell, std))
    return problems


def check_duplicates(rows):
    seen = [defaultdict(set) for _ in range(3)]
    dups = []

    for i, row in enumerate(rows):
        overlaps = set()
        for col, cell in enumerate(row):
            for syn in cell.split(LINE_BREAK):
                overlaps |= seen[col][syn]
                seen[col][syn].add(i)
        for j in overlaps:
            if all(
                set(a.split(LINE_BREAK)) & set(b.split(LINE_BREAK))
                for a, b in zip(row, rows[j])
            ):
                dups.append((i, j))

    uniq = []
    seen_pairs = set()
    for i, j in dups:
        key = tuple(sorted((i, j)))
        if key not in seen_pairs:
            uniq.append((i, j))
            seen_pairs.add(key)
    return uniq


def main():
    data = load_yaml(sys.argv[1])
    rows = [flatten(entry) for entry in data]

    exit_code = 0

    overlaps = check_overlap(data)
    if overlaps:
        print("\nFEIL: overlapp mellom anbefalt og tillatt:\n")
        for idx, lang, items in overlaps:
            print(f"Oppføring {idx}, {lang}: {', '.join(items)}")
        exit_code |= ERR_OVERLAP

    nonstd = check_nonstandard(rows)
    if nonstd:
        print("\nFEIL: ikke-standardiserte synonymer:\n")
        for i, c, old, new in nonstd:
            print(f"Oppføring {i+1}, kolonne {c+1}:\n  Nå:   {old}\n  Bør:  {new}\n")
        exit_code |= ERR_NONSTANDARD

    dup = check_duplicates(rows)
    if dup:
        print("\nFEIL: duplikater:\n")
        for i, j in dup:
            print(f"Oppføring {i+1} og {j+1} dupliserer hverandre.")
        exit_code |= ERR_DUPLICATES

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
