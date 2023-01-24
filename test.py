#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

lineBreak = "<br>"

# Check if list is sorted
isSorted = lambda l: all(l[i] <= l[i+1] for i in range(len(l) - 1))

# Returns a list of lists. Each list is one row.
def readCsv(filename):
  data = []
  with open(filename, encoding='utf-8', errors='ignore') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
      data.append(list(map(lambda x: x.lower(), row)))
  return list(filter(None, data)) # Remove empty rows


def checkSorted(data):
  unsortedList = []
  for r, row in enumerate(data):
    for c in range(3):
      synonymer = row[c].split(lineBreak)
      if not isSorted(synonymer):
        unsortedList.append((r, c, row[c], synonymer, lineBreak.join(sorted(synonymer))))
  return unsortedList


def main():
  exitCode = 0
  data = readCsv(sys.argv[1])

  unsorted = checkSorted(data)

  if len(unsorted) > 0:
    exitCode |= 32
    print("Følgende endringer må gjøres pga. usorterte oppføringer:\n")
    for r, c, error, correct in unsorted:
      print("Rad", r + 1, "kolonne", c + 1, ":", error, "-->", correct)

  sys.exit(exitCode)


main()
