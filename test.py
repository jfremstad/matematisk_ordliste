#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
import re


# Check if list is sorted
def isSorted(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

# Returns a list of lists. Each list is one row.
def readcsv(filename):
    data = []
    with open(filename, encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(list(map(lambda x:x.lower(), row)))
    return list(filter(None, data)) # Remove empty lists

def checkSorted(data):
    EXITCODE = 0
    errorlist = []
    for row in data:
        for col in range(3):
            synonyms = row[col].split("<br>")
            if not isSorted(row[col].split("<br>")):
                errorlist.append(row[col])
                EXITCODE = 32

    if EXITCODE == 32:
        print("Endringer som må gjøres:\n")
        for error in errorlist:
            print(error, "-->", "<br>".join(sorted(error.split("<br>"))))
    sys.exit(EXITCODE)


def main():
    data = readcsv(sys.argv[1])
    checkSorted(data)

main()
