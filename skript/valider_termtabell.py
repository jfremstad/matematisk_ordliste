#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import re
from collections import defaultdict

LINE_BREAK = "<br>"

NUMBER_OF_COLUMNS = 4
NUMBER_OF_LANGUAGE_COLUMNS = 3
COMMENT_COLUMN = NUMBER_OF_LANGUAGE_COLUMNS

ERR_INVALID_CSV = 128
ERR_INCOMPLETE_ROW = 64
ERR_NONSTANDARD_ROW = 32
ERR_DUPLICATE_TRANSLATION = 16


def trim(s):
    """Removes repeated spaces and trims the ends of the string."""
    return " ".join(s.split())


line_break_pattern = re.compile(
    r"((\\r)?\\n|<\s*(br|BR)\s*/>|<\s*(br|BR)\s*></\s*(br|BR)\s*>)"
)


def standardize_line_breaks(s):
    return line_break_pattern.sub(LINE_BREAK, s)


def process_csv_row(row):
    """Processes a CSV file's rows."""
    if len(row) < NUMBER_OF_COLUMNS:
        return tuple(map(str.casefold, row[:NUMBER_OF_LANGUAGE_COLUMNS]))
    else:
        return tuple(map(str.casefold, row[:NUMBER_OF_LANGUAGE_COLUMNS])) + (
            ",".join(row[NUMBER_OF_LANGUAGE_COLUMNS:]),
        )


def read_csv(filename):
    """Reads a CSV file and returns a list of lists, each representing a row."""
    with open(filename, encoding="utf-8") as csvfile:
        raw_data = None
        try:
            reader = csv.reader(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONE
            )
            raw_data = tuple(reader)
        except:
            print("FEIL: ugyldig CSV-fil.")
            sys.exit(ERR_INVALID_CSV)
        data = list(map(process_csv_row, raw_data))
    return data


def check_incomplete_rows(data):
    """Checks for incomplete rows."""
    return tuple(
        i
        for i, row in enumerate(data)
        if len(row) < NUMBER_OF_COLUMNS
        or any(cell.strip() == "" for cell in row[:NUMBER_OF_LANGUAGE_COLUMNS])
    )


def standardize_cell(cell, c):
    """Standardizes a cell's content."""
    if c < NUMBER_OF_LANGUAGE_COLUMNS:
        return standardize_translation(cell, c)
    elif c == COMMENT_COLUMN:
        return standardize_comment(cell)
    else:
        raise ValueError(f"Column index {c} not recognized.")


def standardize_translation(translation, c):
    """Standardizes a translation cell's content."""
    # Remove alternate line breaks
    cell = standardize_line_breaks(translation)
    # Split up
    synonyms = cell.split(LINE_BREAK)
    # Trim spaces
    synonyms = map(trim, synonyms)
    # Remove empty synonyms
    synonyms = filter(lambda x: x != "", synonyms)
    # Remove duplicates
    synonyms = set(synonyms)
    # Sort
    synonyms = sorted(synonyms)
    # Combine
    return LINE_BREAK.join(synonyms)


def standardize_comment(comment):
    """Standardizes a comment's contents."""
    comment = comment.strip().strip('"')

    if not comment:
        return comment

    comment = standardize_line_breaks(comment)

    return '"' + comment + '"'


def check_standardized(data):
    """Checks if all cells are standardized and returns a list of non-standard cells."""
    errors = []
    for r, row in enumerate(data):
        for c in range(len(row)):
            std = standardize_cell(row[c], c)
            if std != row[c]:
                errors.append((r, c, row[c], std))

    return errors


def check_duplicate_translations(data):
    """Checks for duplicate translations by searching for overlap in terms in every column."""
    duplicates_groups = []
    columns_to_rows = [defaultdict(set) for _ in range(NUMBER_OF_LANGUAGE_COLUMNS)]

    checked_rows = set()

    for i, row in enumerate(data):
        if i in checked_rows:
            continue

        possible_duplicates = set()
        duplicate_group = []

        # Update tracking and find the set of possible duplicates for this row
        for c, cell in enumerate(row[:NUMBER_OF_LANGUAGE_COLUMNS]):
            translation_set = set(cell.split(LINE_BREAK))
            for translation in translation_set:
                possible_duplicates.update(columns_to_rows[c][translation])

                # Add this row to the set of rows that have this translation in column c
                columns_to_rows[c][translation].add(i)

        # Remove the row itself from possible duplicates
        possible_duplicates.discard(i)

        for j in possible_duplicates:
            other_row = data[j]
            if all(
                set(cell.split(LINE_BREAK)) & set(other_cell.split(LINE_BREAK))
                for cell, other_cell in zip(
                    row[:NUMBER_OF_LANGUAGE_COLUMNS],
                    other_row[:NUMBER_OF_LANGUAGE_COLUMNS],
                )
            ):
                duplicate_group.append((i, row))
                duplicate_group.append((j, other_row))
                checked_rows.add(i)
                checked_rows.add(j)

        if duplicate_group:
            duplicates_groups.append(
                list(set(duplicate_group))
            )  # Remove duplicate tuples

    return duplicates_groups


def main():
    exit_code = 0

    data = read_csv(sys.argv[1])

    # Check for incomplete rows
    incomplete_rows = check_incomplete_rows(data)

    if incomplete_rows:
        exit_code |= ERR_INCOMPLETE_ROW
        print(f"\nFEIL: følgende rader ({len(incomplete_rows)}) er ufullstendige:")
        print(*(i + 1 for i in incomplete_rows), sep=", ")

    # Compare to standardization
    nonstandard = check_standardized(data)

    if nonstandard:
        exit_code |= ERR_NONSTANDARD_ROW
        print(f"\nFEIL: følgende korreksjoner ({len(nonstandard)}) må gjøres:\n")
        for r, c, error, correct in nonstandard:
            print(
                f"Rad {r + 1} kolonne {c + 1}:\n  Nåværende: {error}\n  Korrigert: {correct}"
            )
        print()

    # Check for duplicate translations
    duplicate_translations = check_duplicate_translations(data)

    if duplicate_translations:
        exit_code |= ERR_DUPLICATE_TRANSLATION
        print(
            f"\nFEIL: følgende duplikate oversettelser ({len(duplicate_translations)}) ble funnet:\n"
        )
        for g, duplicate_group in enumerate(duplicate_translations, 1):
            print(f"Gruppe {g} av duplikater:")
            for r, row in duplicate_group:
                print(f"Rad {r + 1}: {','.join(row)}")
            print()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
