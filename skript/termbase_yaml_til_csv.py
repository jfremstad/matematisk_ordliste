#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bruk:
#     python termbase_yaml_til_csv.py INN_YAML SKJEMA_JSON UT_CSV
#
# SKJEMA_JSON: sti til JSON Schema, bestemmer rekkefølge på kolonner
# INN_YAML:    sti til YAML som skal konverteres
# UT_CSV:     sti til resultatfilen i CSV-format

import sys
import yaml
import json
import csv

if len(sys.argv) != 4:
    sys.exit("Bruk: python termbase_yaml_til_csv.py SKJEMA_JSON INN_YAML UT_CSV")

skjema_json = sys.argv[1]
inn_yaml   = sys.argv[2]
ut_csv    = sys.argv[3]

# ------------------------------------------------------------
# 1. Last YAML
# ------------------------------------------------------------

with open(inn_yaml, encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ------------------------------------------------------------
# 2. Last JSON-skjema og hent ordnet rekkefølge på felter
# ------------------------------------------------------------

with open(skjema_json, encoding="utf-8") as f:
    schema = json.load(f)

def ordered_fields_from_schema(schema_obj):
    """Returnerer liste av kolonnenavn basert på skjemaets rekkefølge."""
    fields = []

    props = schema_obj.get("properties", {})
    for key, value in props.items():
        if "properties" in value:
            # Nøstet objekt - flatlegg til "key subkey"
            for subkey in value["properties"]:
                fields.append(f"{key} {subkey}")
        else:
            fields.append(key)

    return fields

schema_fields = ordered_fields_from_schema(schema["items"])

# ------------------------------------------------------------
# 3. Finn andre felt som finnes i YAML men ikke i skjema - tilføy på slutten
# ------------------------------------------------------------

yaml_fields = set()

for entry in data:
    for key, value in entry.items():
        if isinstance(value, dict):
            for subkey in value:
                yaml_fields.add(f"{key} {subkey}")
        else:
            yaml_fields.add(key)

extra_fields = sorted(yaml_fields - set(schema_fields))

# den endelige rekkefølgen
feltnavn = schema_fields + extra_fields

# ------------------------------------------------------------
# 4. Skriv CSV
# ------------------------------------------------------------

def flatten_list(v):
    """Gjør om YAML-lister til <br>-separerte strenger."""
    if isinstance(v, list):
        return "<br>".join(str(x) for x in v)
    return v

with open(ut_csv, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=feltnavn)
    writer.writeheader()

    for entry in data:
        row = {c: "" for c in feltnavn}

        for key, value in entry.items():
            if isinstance(value, dict):
                for subkey, subval in value.items():
                    row[f"{key} {subkey}"] = flatten_list(subval)
            else:
                row[key] = flatten_list(value)

        writer.writerow(row)
