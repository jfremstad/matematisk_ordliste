# Bruk:
#     python validate_yaml.py SKJEMA_JSON YAML_FIL
#
# SKJEMA_JSON:  sti til JSON-skjemaet (f.eks. termbase_skjema.json)
# YAML_FIL:     sti til YAML-filen som skal valideres
#
# Skriptet leser inn skjemaet og YAML-filen, validerer dem mot hverandre,
# og skriver "YAML er gyldig." hvis alt stemmer. Ved feil avsluttes
# programmet med en feilmelding som forklarer hva som ikke stemmer.

import sys
import yaml
import json
from jsonschema import validate, ValidationError

if len(sys.argv) != 3:
    sys.exit("Bruk: python validate_yaml.py SKJEMA_JSON YAML_FIL")

skjema_sti = sys.argv[1]
yaml_sti = sys.argv[2]

# ------------------------------------------------------------
# 1. Last JSON-skjema
# ------------------------------------------------------------

with open(skjema_sti, "r", encoding="utf-8") as f:
    skjema = json.load(f)

# ------------------------------------------------------------
# 2. Last YAML
# ------------------------------------------------------------

with open(yaml_sti, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

# ------------------------------------------------------------
# 3. Valider YAML-fil mot skjema
# ------------------------------------------------------------

try:
    validate(instance=data, schema=skjema)
except ValidationError as e:
    sys.exit(f"Validering mot skjema mislyktes:\n{e}")

print("YAML er gyldig.")
