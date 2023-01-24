#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

lineBreak = "<br>"

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
  cell = cell.replace("\n", lineBreak).replace("<br/>", lineBreak)
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
  return lineBreak.join(sorted(set(synonyms)))


# Sjekker om alle celler er standardiserte
def checkStandardized(data):
  errors = []
  for r, row in enumerate(data):
    for c in range(3):
      std = standardizeCell(row[c])
      if std != row[c]:
        errors.append((r, c, row[c], std))
  return errors

def main():
  exitCode = 0
  data = readCsv(sys.argv[1])

  nonstandard = checkStandardized(data)

  if len(nonstandard) > 0:
    exitCode |= 32
    print("\nFølgende endringer må gjøres (merk mulig fjerning av mellomrom):\n")
    for r, c, error, correct in nonstandard:
      print("Rad", r + 1, "kolonne", c + 1 , ":", error, "-->", correct)
    print()

  sys.exit(exitCode)


main()
