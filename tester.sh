#!/bin/bash
DATABASE="verifiserte_termer.csv"

# Check if CSV is valid
csvlint-v0.2.0-linux-amd64/csvlint "$DATABASE" || exit 1

# Check for empty comments
if [[ "$(grep -c ",\s\+$" $DATABASE)" -ne 0 ]]; then
  echo "==============================="
  echo " Tom merknad i følgende linjer "
  echo "==============================="
  grep ",\s\+$" "$DATABASE"
  exit 2
fi
