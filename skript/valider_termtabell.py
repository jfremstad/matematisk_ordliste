#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

LINE_BREAK = "<br>"

NUMBER_OF_COLUMNS = 4
NUMBER_OF_LANGUAGE_COLUMNS = 3
COMMENT_COLUMN = NUMBER_OF_LANGUAGE_COLUMNS

ERR_INVALID_CSV = 128
ERR_INCOMPLETE_ROW = 64
ERR_NONSTANDARD_ROW = 32
ERR_DUPLICATE_ROW = 16


def trim(s):
    """Removes repeated spaces and trims the ends of the string."""
    return " ".join(s.split())


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
            print("Feil: ugyldig CSV-fil.")
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
    cell = (
        translation.replace("\r\n", LINE_BREAK)
        .replace("\n", LINE_BREAK)
        .replace("<br/>", LINE_BREAK)
        .replace("<br />", LINE_BREAK)
        .replace("<br></br>", LINE_BREAK)
    )
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
    comment = comment.strip()

    if not comment:
        return comment

    if not comment.startswith('"'):
        comment = '"' + comment
    if not comment.endswith('"'):
        comment = comment + '"'

    if comment == '""':
        return ""

    return comment


def check_standardized(data):
    """Checks if all cells are standardized and returns a list of non-standard cells."""
    errors = []
    for r, row in enumerate(data):
        for c in range(len(row)):
            std = standardize_cell(row[c], c)
            if std != row[c]:
                errors.append((r, c, row[c], std))

    return errors


def check_duplicate_rows(data):
    """Checks for duplicate rows ignoring the comment."""
    rows = tuple(",".join(row[:NUMBER_OF_LANGUAGE_COLUMNS]) for row in data)
    duplicates = set(row for row in rows if rows.count(row) > 1)
    return duplicates


def main():
    exit_code = 0

    data = read_csv(sys.argv[1])

    # Check for incomplete rows
    incomplete_rows = check_incomplete_rows(data)

    if incomplete_rows:
        print("\nFeil: følgende rader er ufullstendige:")
        print(*(i + 1 for i in incomplete_rows), sep=",")
        exit_code |= ERR_INCOMPLETE_ROW

    # Compare to standardization
    nonstandard = check_standardized(data)

    if nonstandard:
        exit_code |= ERR_NONSTANDARD_ROW
        print(
            "\nFeil: følgende endringer må gjøres (merk mulig fjerning av mellomrom):\n"
        )
        for r, c, error, correct in nonstandard:
            print("Rad", r + 1, "kolonne", c + 1, ":", error, "-->", correct)
        print()

    # Check for duplicates
    duplicate_rows = check_duplicate_rows(data)

    if duplicate_rows:
        exit_code |= ERR_DUPLICATE_ROW
        print("\nFeil: følgende rader er duplikater sett bort ifra kommentar:\n")
        for row in duplicate_rows:
            print(row)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
