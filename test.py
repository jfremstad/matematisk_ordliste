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
            data.append(row)
    return data

def checkSorted(data):
    EXITCODE = 0
    errorlist = []
    for i in data:
        for j in range(3):
            synonyms = i[j].split("/")
            for k in synonyms:
                if " " in k and len(synonyms) != 1 and k[-1] != " " and k[0] != " ":
                    EXITCODE = 2
                    print(i[j].split("/"))
            if not isSorted(re.sub(" ?/ ?", "/", i[j]).split("/")):
                errorlist.append(i[j])
                EXITCODE = 5
    if EXITCODE == 5:
        print("Endringer som må gjøres:\n")
        for i in errorlist:
            print(i, "-->", "/".join(sorted(i.split("/"))))
    sys.exit(EXITCODE)


def main():
    data = readcsv(sys.argv[1])
    checkSorted(data)

main()
