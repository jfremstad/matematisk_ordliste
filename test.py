#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys

# Check if list is sorted
def isSorted(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

# Returns a list of lists. Each list is one row.
def readCsv(filename):
    data = []
    with open(filename, encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            data.append(list(map(lambda x: x.lower(), row)))
    return list(filter(None, data)) # Remove empty lists

def checkSorted(data):
    errorList = []
    for row in data:
        for col in range(3):
            if not isSorted(row[col].split("<br>")):
                errorList.append(row[col])

    if len(errorList) > 0:
        print("Endringer som må gjøres:\n")
        for error in errorList:
            print(error, "-->", "<br>".join(sorted(error.split("<br>"))))
    
    exitCode = 32 if len(errorList) > 0 else 0
    sys.exit(exitCode)


def main():
    data = readCsv(sys.argv[1])
    checkSorted(data)

main()
