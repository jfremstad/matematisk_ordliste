import csv
import re

# Define a dictionary of patterns to search for in the Merknad field.
# Each key is the output column name, and the value is a regex to capture the desired text.
# For example, if Merknad contains a line like "Ordklasse: substantiv", we want to extract "substantiv".
# Similarly for genus, uttale, synonym, etc.
patterns_remove = {
    "flertallsform norsk": r"[Nn]orsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform bokmål": r"[Bb]okmål [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform nynorsk": r"[Nn]ynorsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "flertallsform engelsk": r"[Ee]ngelsk [Ff]lertall(?:sform)?:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus": r"[Gg]enus:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus bokmål": r"[Gg]enus [Bb]okmål:\s*(.*?)\s*($|,|;|\.|<br>)",
    "genus nynorsk": r"[Gg]enus [Nn]ynorsk:\s*(.*?)\s*($|,|;|\.|<br>)",
    "uttale": r"[Uu]ttale:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    "uttale bokmål": r"[Uu]ttale [Bb]okmål:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    "uttale nynorsk": r"[Uu]ttale [Nn]ynorsk:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    "uttale engelsk": r"[Uu]ttale [Ee]ngelsk:\s*\[(.*?)\]\s*($|,|;|\.|<br>)",
    "ordklasse": r"[Oo]rdklasse:\s*(.*?)\s*($|,|;|\.|<br>)",
    "synonym": r"[Ss]ynonym:\s*(.*?)\s*($|,|;|\.|<br>)"
}

patterns_dont_remove = {
    "bruksområde1": r"Oversettelsen gjelder bruk i(?:nnen)? (?:blant annet)? ([^\.]+) og utelukker ikke at termen kan benyttes ulikt i andre sammenhenger\.",
    "bruksområde2": r"Legg merke til at denne oversettelsen gjelder innen ([^\.]+)\.",
    "bruksområde3": r"Oversettelsen gjelder bruk i ([^\.]+) og utelukker ikke at termen kan benyttes ulikt i andre sammenhenger\."
}

def custom_strip(s :str) -> str:
    s = re.sub(r"^(\s*<br>\s*)+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(\s*<br>\s*)+$", "", s, flags=re.IGNORECASE)
    s = re.sub(r"(\s*<br>\s*<br>)+", "", s, flags=re.IGNORECASE)
    return s

input_file = "verifiserte_termer.csv"
output_file = "verifiserte_termer2.csv"

with open(input_file, "r", encoding="utf-8") as infile, open(
    output_file, "w", newline="", encoding="utf-8"
) as outfile:
    reader = csv.DictReader(infile)

    # Prepare output fieldnames
    fieldnames = [
        "tillatt term bokmål",
        "tillatt term nynorsk",
        "tillatt term engelsk",
        "anbefalt term bokmål",
        "anbefalt term nynorsk",
        "anbefalt term engelsk",
        "flertallsform bokmål",
        "flertallsform nynorsk",
        "flertallsform engelsk",
        "genus bokmål",
        "genus nynorsk",
        "uttale bokmål",
        "uttale nynorsk",
        "uttale engelsk",
        "ordklasse",
        "bruksområde",
        "synonym",
        "merknad",
    ]

    writer = csv.DictWriter(
        outfile, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_MINIMAL,
    )
    writer.writeheader()

    for row in reader:
        # Extract the terms
        tillatt_bokmaal = row.get("Bokmål", "").strip()
        tillatt_nynorsk = row.get("Nynorsk", "").strip()
        tillatt_engelsk = row.get("Engelsk", "").strip()
        merknad = row.get("Merknad", "").strip()

        # Parse the merknad field for each pattern
        extracted_data = {}
        for col, pattern in {**patterns_remove, **patterns_dont_remove}.items():
            match = re.search(pattern, merknad, flags=re.IGNORECASE | re.DOTALL)
            if match:
                extracted_data[col] = match.group(1).strip()
            else:
                extracted_data[col] = ""

        # Now remove all occurrences of these patterns from Merknad
        # This will remove the keys (like "Ordklasse:"), the captured text, and trailing punctuation/delimiters
        for col, pattern in patterns_remove.items():
            merknad = re.sub(pattern, "", merknad, flags=re.IGNORECASE | re.DOTALL)

        # Check if the merknad contains the recommended Bokmål term sentence
        # Pattern: Begge skrivemåtene brukes på norsk, men X anbefales.
        anbefalt_norsk_match = re.search(
            r"norsk,\s*men\s+(.*?)\s+anbefales\.",
            merknad,
            flags=re.IGNORECASE,
        )
        if anbefalt_norsk_match:
            anbefalt_norsk = anbefalt_norsk_match.group(1).strip()
            tillatt_bokmaal = re.sub(
                anbefalt_norsk, "", tillatt_bokmaal, flags=re.IGNORECASE
            )
            tillatt_nynorsk = re.sub(
                anbefalt_norsk, "", tillatt_nynorsk, flags=re.IGNORECASE
            )
        else:
            anbefalt_norsk = ""

        # Check if the merknad contains the recommended Bokmål term sentence
        # Pattern: Begge skrivemåtene brukes på bokmål, men X anbefales.
        anbefalt_bokmaal_match = re.search(
            r"bokmål,\s*men\s+(.*?)\s+anbefales\.",
            merknad,
            flags=re.IGNORECASE,
        )
        if anbefalt_bokmaal_match:
            anbefalt_bokmaal = anbefalt_bokmaal_match.group(1).strip()
            tillatt_bokmaal = re.sub(anbefalt_bokmaal, "", tillatt_bokmaal, flags=re.IGNORECASE)
        else:
            anbefalt_bokmaal = ""

        # Check if the merknad contains the recommended nynorsk term sentence
        # Pattern: Begge skrivemåtene brukes på nynorsk, men X anbefales.
        anbefalt_nynorsk_match = re.search(
            r"nynorsk,\s*men\s+(.*?)\s+anbefales\.",
            merknad,
            flags=re.IGNORECASE,
        )
        if anbefalt_nynorsk_match:
            anbefalt_nynorsk = anbefalt_nynorsk_match.group(1).strip()
            tillatt_nynorsk = re.sub(
                anbefalt_nynorsk, "", tillatt_nynorsk, flags=re.IGNORECASE
            )
        else:
            anbefalt_nynorsk = ""

        # Check if the merknad contains the recommended engelsk term sentence
        # Pattern: Begge skrivemåtene brukes på engelsk, men X anbefales.
        anbefalt_engelsk_match = re.search(
            r"engelsk,\s*men\s+(.*?)\s+anbefales\.",
            merknad,
            flags=re.IGNORECASE,
        )
        if anbefalt_engelsk_match:
            anbefalt_engelsk = anbefalt_engelsk_match.group(1).strip()
            tillatt_engelsk = re.sub(
                anbefalt_engelsk, "", tillatt_engelsk, flags=re.IGNORECASE
            )
        else:
            anbefalt_engelsk = ""

        # Write the transformed row
        writer.writerow(
            {
                "anbefalt term bokmål": custom_strip(anbefalt_bokmaal)
                + custom_strip(anbefalt_norsk),
                "anbefalt term nynorsk": custom_strip(anbefalt_nynorsk)
                + custom_strip(anbefalt_norsk),
                "anbefalt term engelsk": custom_strip(anbefalt_engelsk),
                "tillatt term bokmål": custom_strip(tillatt_bokmaal),
                "tillatt term nynorsk": custom_strip(tillatt_nynorsk),
                "tillatt term engelsk": custom_strip(tillatt_engelsk),
                "flertallsform bokmål": extracted_data["flertallsform bokmål"]
                + extracted_data["flertallsform norsk"],
                "flertallsform nynorsk": extracted_data["flertallsform nynorsk"]
                + extracted_data["flertallsform norsk"],
                "flertallsform engelsk": extracted_data["flertallsform engelsk"],
                "genus bokmål": extracted_data["genus bokmål"]
                + extracted_data["genus"],
                "genus nynorsk": extracted_data["genus nynorsk"]
                + extracted_data["genus"],
                "uttale bokmål": extracted_data["uttale bokmål"]
                + extracted_data["uttale"],
                "uttale nynorsk": extracted_data["uttale nynorsk"],
                "uttale engelsk": extracted_data["uttale engelsk"],
                "ordklasse": extracted_data["ordklasse"],
                "bruksområde": extracted_data["bruksområde1"]
                + extracted_data["bruksområde2"]
                + extracted_data["bruksområde3"],
                "synonym": extracted_data["synonym"],
                "merknad": custom_strip(merknad),
            }
        )
