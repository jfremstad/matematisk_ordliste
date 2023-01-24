#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

lineBreak = "<br>"
numberOfLanguageColumns = 3

# Fjerner gjentatte mellomrom og trimmer endene
trim = lambda s: ' '.join(s.split())

# Returns a list of lists. Each list is one row.
def readCsv(filename):
  data = []
  with open(filename, encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      data.append(list(map(str.casefold, row)))
  return list(filter(None, data)) # Remove empty rows

# Standardiserer en celle
def standardizeCell(cell):
  # Fjern alternative linjebytter
  cell = cell.replace("\r\n", lineBreak).replace("\n", lineBreak).replace("<br/>", lineBreak).replace("<br />", lineBreak).replace("<br></br>", lineBreak)
  # Del opp
  synonyms = cell.split(lineBreak)
  # Trim mellomrom
  synonyms = map(trim, synonyms)
  # Fjern tomme synonymer
  synonyms = filter(lambda x: x != "", synonyms)
  # Fjern duplikater
  synonyms = set(synonyms)
  # Sorter
  synonyms = sorted(synonyms)
  # Sett sammen
  return lineBreak.join(synonyms)

# Sjekker om alle celler er standardiserte
def checkStandardized(data):
  errors = []
  for r, row in enumerate(data):
    for c in range(numberOfLanguageColumns):
      std = standardizeCell(row[c])
      if std != row[c]:
        errors.append((r, c, row[c], std))
  return errors

# Sjekk for duplikate rader ved ignorering av kommentar
def checkDuplicateRows(data):
  rows = tuple(",".join(row[:numberOfLanguageColumns]) for row in data)
  duplicates = set(row for row in rows if rows.count(row) > 1)
  return duplicates


def main():
  exitCode = 0
  data = readCsv(sys.argv[1])

  nonstandard = checkStandardized(data)

  if nonstandard:
    exitCode |= 32
    print("\nFølgende endringer må gjøres (merk mulig fjerning av mellomrom):\n")
    for r, c, error, correct in nonstandard:
      print("Rad", r + 1, "kolonne", c + 1 , ":", error, "-->", correct)
    print()

  duplicateRows = checkDuplicateRows(data)
  
  if duplicateRows:
    exitCode |= 64
    print("\nFølgende rader er duplikater opp til kommentar:\n")
    for row in duplicateRows:
      print(row)

  sys.exit(exitCode)


main()
