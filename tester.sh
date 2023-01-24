#!/bin/bash
DATABASE="verifiserte_termer.csv"
EXITCODE=0

# Check if CSV is valid
csvlint-v0.2.0-linux-amd64/csvlint "${DATABASE}" || EXITCODE=$((EXITCODE | 1))

EMPTYCOMMENT="$(grep ',\s\+$' ${DATABASE})"
if [[ ${EMPTYCOMMENT} ]]; then
  echo "====================================="
  echo "== Følgende linjer har tom merknad =="
  echo "====================================="
  echo "${EMPTYCOMMENT}"
  echo
  EXITCODE=$((EXITCODE | 2))
fi

if [[ "$(grep -Ec "^\s*$" ${DATABASE})" -ne 0 ]]; then
  echo "=============================="
  echo "== Følgende linjer er tomme =="
  echo "=============================="
  grep -n '^\s*$' "${DATABASE}"
  echo
  EXITCODE=$((EXITCODE | 4))
fi

DUPLICATES="$(sort ${DATABASE} | uniq -d)"
if [[ ${DUPLICATES} ]]; then
  echo "============================================="
  echo "== Ordlista inneholder følgende duplikater =="
  echo "============================================="
  echo "${DUPLICATES}"
  echo
  EXITCODE=$((EXITCODE | 8))
fi

MISSINGQUOTES="$(grep -v ',\s\+$' ${DATABASE} | cut -d',' -f 4- | grep -vE '^$|^".*"$')"
if [[ ${MISSINGQUOTES} ]]; then
  echo "=============================================="
  echo "== Følgende merknader mangler anførselstegn =="
  echo "=============================================="
  echo "${MISSINGQUOTES}"
  echo
  EXITCODE=$((EXITCODE | 16))
fi

if [[ ${EXITCODE} -ne 0 ]]; then
  exit ${EXITCODE}
fi

# Execute more complicated python tests
python3 test.py "${DATABASE}"
