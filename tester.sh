#!/bin/bash
DATABASE="verifiserte_termer.csv"

# Check if CSV is valid
csvlint-v0.2.0-linux-amd64/csvlint "$DATABASE" || exit 1

# Check for empty comments or empty lines
if [[ "$(grep -Ec ",\s+$|^\s*$" $DATABASE)" -ne 0 ]]; then
  echo "======================================================="
  echo "             Det er feil i følgende linjer             "
  echo "======================================================="
  grep -En ",\s+$|^\s*$" "$DATABASE"
  exit 2
fi

python3 test.py "$DATABASE"
