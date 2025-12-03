#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bruk:
#     python kvalitetssjekk_termbase.py SKJEMA_JSON YAML_FIL
#
# SKJEMA_JSON: sti til JSON-skjemaet (f.eks. termbase_skjema.json)
# YAML_FIL:   sti til YAML-filen som skal valideres
#
# Skriptet leser inn skjemaet og YAML-filen, validerer strukturen mot skjemaet,
# sjekker rekkefølgen av felter, ser etter overlapp mellom anbefalt/tillatt,
# og detekterer globale konflikter mellom oppføringer. Alle feil rapporteres
# og påvirker returverdien via OR av feilkoder.

import json
import yaml
from jsonschema import validate, ValidationError
from itertools import combinations


# === FEILKODER ===
SCHEMA_VALIDATION   =  2
FIELD_ORDER_ERROR   =  4
LOCAL_OVERLAP_ERROR =  8
GLOBAL_CONFLICT_ERR = 16


def load_schema(schema_path):
    """Les inn JSON-skjemaet fra fil."""
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(yaml_path):
    """Les inn YAML-filen som skal valideres."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def flatten_terms(value):
    """
    Normaliser et felt som kan være en streng, liste eller None
    til en liste med renskede strenger.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()]
    if isinstance(value, list):
        return [v.strip() for v in value]
    return []


def check_field_order(entry, schema_properties):
    """
    Sjekk at feltene i en oppføring følger samme rekkefølge
    som definert i JSON-skjemaet. Kun felter som faktisk finnes
    i oppføringen tas i betraktning.
    """
    keys = list(entry.keys())
    expected = list(schema_properties.keys())
    restricted = [k for k in keys if k in expected]
    expected = [k for k in expected if k in restricted]
    return restricted == expected, restricted, expected


def check_local_overlap(anbefalt, tillatt):
    """
    Sjekk overlapp mellom anbefalt.* og tillatt.* for én oppføring.
    Returnerer et dict med språk → liste av overlappende termer.
    """
    overlaps = {}
    for lang in ["bokmål", "nynorsk", "engelsk"]:
        a = flatten_terms(anbefalt.get(lang)) if anbefalt else []
        t = flatten_terms(tillatt.get(lang)) if tillatt else []
        o = sorted(set(a) & set(t))
        if o:
            overlaps[lang] = o
    return overlaps


def entry_lang_terms(entry):
    """
    Returner et dict lang → sett av alle termer i denne oppføringen
    (kombinerer anbefalt.* og tillatt.* for hvert språk).
    """
    langs = ["bokmål", "nynorsk", "engelsk"]
    out = {lang: set() for lang in langs}
    for field in ("anbefalt", "tillatt"):
        obj = entry.get(field, {}) or {}
        for lang in langs:
            for t in flatten_terms(obj.get(lang)):
                out[lang].add(t)
    return out


def index_by_language(data):
    """
    Bygg opp et invertert indeks:
        index[lang][term] = liste over oppføringsindekser som inneholder termen.
    """
    langs = ["bokmål", "nynorsk", "engelsk"]
    index = {lang: {} for lang in langs}

    for i, entry in enumerate(data):
        for field in ("anbefalt", "tillatt"):
            obj = entry.get(field, {}) or {}
            for lang in langs:
                for t in flatten_terms(obj.get(lang)):
                    index[lang].setdefault(t, []).append(i)
    return index


def language_pairs(index_lang):
    """
    Gitt ett språk sin indeks: term → [oppføringer],
    returner mengden av alle par (i, j), i < j, som deler minst én term.
    """
    pairs = set()
    for entries in index_lang.values():
        if len(entries) >= 2:
            for i, j in combinations(entries, 2):
                if i < j:
                    pairs.add((i, j))
                else:
                    pairs.add((j, i))
    return pairs


def compute_global_conflicts(data):
    """
    Effektiv deteksjon av globale konflikter:
    Et par (i, j) er i konflikt dersom de deler minst én bokmål-term,
    minst én nynorsk-term, og minst én engelsk-term.

    Overlappingen per språk kan være forskjellige termer (t1, t2, t3).
    """
    index = index_by_language(data)

    bok_pairs = language_pairs(index["bokmål"])
    nyn_pairs = language_pairs(index["nynorsk"])
    eng_pairs = language_pairs(index["engelsk"])

    conflict_pairs = bok_pairs & nyn_pairs & eng_pairs

    conflicts = []
    for (i, j) in sorted(conflict_pairs):
        entry_i = entry_lang_terms(data[i])
        entry_j = entry_lang_terms(data[j])
        overlaps = {
            lang: sorted(entry_i[lang] & entry_j[lang])
            for lang in ("bokmål", "nynorsk", "engelsk")
        }
        conflicts.append({
            "entries": (i, j),
            "overlap": overlaps
        })

    return conflicts


def main(schema_path, yaml_path):
    """Kjør alle valideringsstegene på gitt skjema og YAML-fil og returner feilkode."""
    error_flags = 0

    schema = load_schema(schema_path)
    data = load_yaml(yaml_path)

    try:
        validate(instance=data, schema=schema)
    except (OSError, ValidationError) as e:
        print(f"Skjemavalidering feilet: {e}")
        return SCHEMA_VALIDATION


    schema_properties = schema["items"]["properties"]

    # 1. Feltrekkefølge
    for i, entry in enumerate(data):
        ok, found, expected = check_field_order(entry, schema_properties)
        if not ok:
            error_flags |= FIELD_ORDER_ERROR
            print(f"Oppføring {i}: feil rekkefølge på felter.")
            print(f"  Funnet:    {found}")
            print(f"  Forventet: {expected}")

    # 2. Lokal overlapp
    for i, entry in enumerate(data):
        local = check_local_overlap(entry.get("anbefalt"), entry.get("tillatt"))
        if local:
            error_flags |= LOCAL_OVERLAP_ERROR
            print(f"Oppføring {i}: overlapp funnet:")
            for lang, terms in local.items():
                print(f"  {lang}: {terms}")

    # 3. Globale konflikter
    conflicts = compute_global_conflicts(data)

    for c in conflicts:
        error_flags |= GLOBAL_CONFLICT_ERR
        print(f"Oppføringene {c['entries']} er i konflikt:")
        for lang, terms in c["overlap"].items():
            print(f"  {lang}: {terms}")

    return error_flags


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Bruk: python kvalitetssjekk_termbase.py <skjema.json> <data.yaml>")
        sys.exit(1)

    exitcode = main(sys.argv[1], sys.argv[2])

    if not exitcode:
        print("Alt er i orden.")

    sys.exit(exitcode)
