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
            synonyms = row[col].split("/")
            for k in synonyms:
                if " " in k and len(synonyms) != 1 and " / " not in row[col]:
                    EXITCODE = 2
                    print("Mangler mellomrom rundt skråstrek: ", synonyms)
            if not isSorted(re.sub(" ?/ ?", "/", row[col]).split("/")):
                errorlist.append(row[col])
                EXITCODE = 5
    if EXITCODE == 5:
        print("Endringer som må gjøres:\n")
        for error in errorlist:
            print(error, "-->", "/".join(sorted(error.split("/"))))
    sys.exit(EXITCODE)


def main():
    data = readcsv(sys.argv[1])
    checkSorted(data)

main()
