#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Bruk:
#     python yaml_til_json.py INN_YAML UT_JSON
#
# INN_YAML: sti til YAML-fil
# UT_JSON:  sti til resultatfil i JSON-format

import sys
import yaml
import json

if len(sys.argv) != 3:
    sys.exit("Bruk: python yaml_til_json.py INN_YAML UT_JSON")

inn_yaml = sys.argv[1]
ut_json  = sys.argv[2]

# ------------------------------------------------------------
# 1. Last YAML
# ------------------------------------------------------------

with open(inn_yaml, encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ------------------------------------------------------------
# 2. Skriv JSON
# ------------------------------------------------------------

with open(ut_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
