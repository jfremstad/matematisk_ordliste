#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import yaml

input_file = "verifiserte_termer.csv"
output_file = "termbase.yaml"
schema_file = "termbase_skjema.json"

patterns_remove = {
    "flertallsform norsk": r"[Nn]orsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform bokmål": r"[Bb]okmål [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform nynorsk": r"[Nn]ynorsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform engelsk": r"[Ee]ngelsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus": r"[Gg]enus:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus bokmål": r"[Gg]enus [Bb]okmål:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus nynorsk": r"[Gg]enus [Nn]ynorsk:\s*(.*?)\s*($|,|;|\.|<br>)",
    # "uttale": r"[Uu]ttale:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    # "uttale bokmål": r"[Uu]ttale [Bb]okmål:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    # "uttale nynorsk": r"[Uu]ttale [Nn]ynorsk:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    # "uttale engelsk": r"[Uu]ttale [Ee]ngelsk:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    "ordklasse": r"[Oo]rdklasse:\s*(.*?)\s*($|,|;|\.|<br>)",
    "synonym": r"[Ss]ynonym:\s*(.*?)\s*($|,|;|\.|<br>)"
}

patterns_dont_remove = {
    "bruksområde1": r"Oversettelsen gjelder bruk i(?:nnen)?(?: blant annet| for eksempel)? (?!blant annet|for eksempel)([^\.,]+),? og utelukker ikke at termen kan benyttes ulikt i andre sammenhenger\.",
    "bruksområde2": r"Legg merke til at denne oversettelsen gjelder innen ([^\.,]+)\.",
    "bruksområde3": r"Oversettelsen gjelder bruk i ([^\.,]+),? og må ikke",
    "bruksområde4": r"Oversettelsen gjelder(?: blant annet| for eksempel)? (?:omhandlende|når det er snakk om) ([^\.,]+),? og utelukker ikke",
}

def custom_strip(s: str) -> str:
    s = re.sub(r"^(\s*<br>\s*)+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(\s*<br>\s*)+$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s*<br>(\s*<br>)+", "", s, flags=re.IGNORECASE)
    return s.strip()

def prune_empty(obj):
    if isinstance(obj, dict):
        cleaned = {k: prune_empty(v) for k, v in obj.items()}
        cleaned = {k: v for k, v in cleaned.items() if v not in ("", None, {}, [])}
        return cleaned
    if isinstance(obj, list):
        cleaned = [prune_empty(x) for x in obj]
        cleaned = [x for x in cleaned if x not in ("", None, {}, [])]
        return cleaned
    if isinstance(obj, str):
        return obj.strip()
    return obj

def split_br(value):
    if not isinstance(value, str):
        return value
    parts = [p.strip() for p in value.split("<br>") if p.strip()]
    if len(parts) <= 1:
        return parts[0] if parts else ""
    return parts

def is_empty_term(x):
    return x in ("", [], None)

def is_singleton(x):
    return isinstance(x, str)

with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    all_entries = []

    for row in reader:
        tillatt_bm = row.get("Bokmål", "").strip()
        tillatt_nn = row.get("Nynorsk", "").strip()
        tillatt_en = row.get("Engelsk", "").strip()
        merknad = row.get("Merknad", "").strip()

        extracted = {}
        for col, pattern in {**patterns_remove, **patterns_dont_remove}.items():
            m = re.search(pattern, merknad, flags=re.IGNORECASE | re.DOTALL)
            extracted[col] = m.group(1).strip() if m else ""

        for col, pattern in patterns_remove.items():
            merknad = re.sub(pattern, "", merknad, flags=re.IGNORECASE | re.DOTALL)

        m_norsk = re.search(
            r"norsk,\s*men\s+(.*?)\s+(anbefales|er vesentlig mer utbredt)\.",
            merknad, flags=re.IGNORECASE
        )
        if m_norsk:
            anbefalt_norsk = m_norsk.group(1).strip()
            tillatt_bm = re.sub(anbefalt_norsk, "", tillatt_bm, flags=re.IGNORECASE)
            tillatt_nn = re.sub(anbefalt_norsk, "", tillatt_nn, flags=re.IGNORECASE)
        else:
            anbefalt_norsk = ""

        m_bm = re.search(r"bokmål,\s*men\s+(.*?)\s+anbefales\.", merknad, flags=re.IGNORECASE)
        anbefalt_bm = m_bm.group(1).strip() if m_bm else ""

        m_nn = re.search(r"nynorsk,\s*men\s+(.*?)\s+anbefales\.", merknad, flags=re.IGNORECASE)
        anbefalt_nn = m_nn.group(1).strip() if m_nn else ""

        m_en = re.search(r"engelsk,\s*men\s+(.*?)\s+anbefales\.", merknad, flags=re.IGNORECASE)
        anbefalt_en = m_en.group(1).strip() if m_en else ""

        entry = {
            "anbefalt": {
                "bokmål":  split_br("<br>".join(sorted((custom_strip(anbefalt_bm) + custom_strip(anbefalt_norsk)).split("<br>")))),
                "nynorsk": split_br("<br>".join(sorted((custom_strip(anbefalt_nn) + custom_strip(anbefalt_norsk)).split("<br>")))),
                "engelsk": split_br("<br>".join(sorted(custom_strip(anbefalt_en).split("<br>")))),
            },
            "tillatt": {
                "bokmål":  split_br("<br>".join(sorted(custom_strip(tillatt_bm).split("<br>")))),
                "nynorsk": split_br("<br>".join(sorted(custom_strip(tillatt_nn).split("<br>")))),
                "engelsk": split_br("<br>".join(sorted(custom_strip(tillatt_en).split("<br>")))),
            },
            "flertallsform": {
                "bokmål":  split_br(re.sub(r"\s*/\s*", "<br>", extracted["flertallsform bokmål"] + extracted["flertallsform norsk"])),
                "nynorsk": split_br(re.sub(r"\s*/\s*", "<br>", extracted["flertallsform nynorsk"] + extracted["flertallsform norsk"])),
                "engelsk": split_br(re.sub(r"\s*/\s*", "<br>", extracted["flertallsform engelsk"])),
            },
            "genus": {
                "bokmål":  split_br(re.sub(r"\s*/\s*", "<br>", extracted["genus bokmål"] + extracted["genus"])),
                "nynorsk": split_br(re.sub(r"\s*/\s*", "<br>", extracted["genus nynorsk"] + extracted["genus"])),
            },
            # "uttale": {
            #     "bokmål":  split_br(extracted["uttale bokmål"] + extracted["uttale"]),
            #     "nynorsk": split_br(extracted["uttale nynorsk"]),
            #     "engelsk": split_br(extracted["uttale engelsk"]),
            # },
            "ordklasse":     split_br(re.sub("/", "<br>", extracted["ordklasse"])),
            "bruksområde":   split_br(re.sub(r"\s*(/| og )\s*", "<br>", extracted["bruksområde1"] + extracted["bruksområde2"] + extracted["bruksområde3"] + extracted["bruksområde4"])),
            "synonym":       split_br(re.sub(r"\s*/\s*", "<br>", extracted["synonym"])),
            "merknad":       custom_strip(merknad),
        }

        # # Hvis det bare er én tillatt term, gjør den anbefalt
        # for lang in ("bokmål", "nynorsk", "engelsk"):
        #     a = entry["anbefalt"].get(lang)
        #     t = entry["tillatt"].get(lang)

        #     if is_empty_term(a) and is_singleton(t):
        #         entry["anbefalt"][lang] = t
        #         entry["tillatt"][lang] = ""


        def normalize_to_list(x):
            if x in ("", None):
                return []
            if isinstance(x, list):
                return [e.strip() for e in x if e.strip()]
            return [x.strip()]

        for lang in ("bokmål", "nynorsk", "engelsk"):
            a = normalize_to_list(entry["anbefalt"].get(lang))
            t = normalize_to_list(entry["tillatt"].get(lang))

            # Fjern anbefalte fra tillatt
            t = [w for w in t if w.lower() not in {z.lower() for z in a}]

            # kollaps lister med bare ett element
            entry["anbefalt"][lang] = a[0] if len(a) == 1 else a
            entry["tillatt"][lang]   = t[0] if len(t) == 1 else t if t else ""

        entry = prune_empty(entry)
        all_entries.append(entry)

    outfile.write(f"# $schema: {schema_file}\n")
    yaml.dump(all_entries, outfile, allow_unicode=True, sort_keys=False)
