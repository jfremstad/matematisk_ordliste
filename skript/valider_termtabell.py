#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

LINE_BREAK = "<br>"
NUMBER_OF_LANGUAGE_COLUMNS = 3

ERR_DUPLICATE_ROW = 32
ERR_NONSTANDARD_ROW = 128


def trim(s):
    """Removes repeated spaces and trims the ends of the string."""
    return " ".join(s.split())


def read_csv(filename):
    """Reads a CSV file and returns a list of lists, each representing a row."""
    with open(filename, encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        data = [list(map(str.casefold, row)) for row in reader]
    return list(filter(None, data))  # Remove empty rows


def standardize_cell(cell):
    """Standardizes a cell's content."""
    # Remove alternate line breaks
    cell = (
        cell.replace("\r\n", LINE_BREAK)
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


def check_standardized(data):
    """Checks if all cells are standardized and returns a list of non-standard cells."""
    errors = []
    for r, row in enumerate(data):
        for c in range(NUMBER_OF_LANGUAGE_COLUMNS):
            std = standardize_cell(row[c])
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

    nonstandard = check_standardized(data)

    if nonstandard:
        exit_code |= ERR_NONSTANDARD_ROW
        print("\nFølgende endringer må gjøres (merk mulig fjerning av mellomrom):\n")
        for r, c, error, correct in nonstandard:
            print("Rad", r + 1, "kolonne", c + 1, ":", error, "-->", correct)
        print()

    duplicate_rows = check_duplicate_rows(data)

    if duplicate_rows:
        exit_code |= ERR_DUPLICATE_ROW
        print("\nFølgende rader er duplikater opp til kommentar:\n")
        for row in duplicate_rows:
            print(row)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
