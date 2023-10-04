#!/bin/bash

DATABASE="./verifiserte_termer.csv"

ERR_DB_NOT_FOUND=1
ERR_CSVLINT_NOT_FOUND=2
ERR_PYTHON_NOT_FOUND=4
ERR_EMPTY_COMMENT=8
ERR_EMPTY_LINE=16
ERR_DUPLICATE=32
ERR_MISSING_QUOTES=64

EXITCODE=0

# Function to check if a command exists
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

# Check if database exists
if [[ ! -f "${DATABASE}" ]]; then
  echo "Feil: Databasefilen '${DATABASE}' ikke funnet."
  EXITCODE=$((EXITCODE | ERR_DB_NOT_FOUND))
  exit ${EXITCODE}
fi


# Check if CSV is valid
if command_exists csvlint; then
  csvlint "${DATABASE}" || EXITCODE=$((EXITCODE | ERR_CSVLINT_NOT_FOUND))
else
  echo "Feil: csvlint ikke funnet."
  EXITCODE=$((EXITCODE | ERR_CSVLINT_NOT_FOUND))
fi

EMPTYCOMMENT="$(grep ',\s\+$' "${DATABASE}")"
if [[ ${EMPTYCOMMENT} ]]; then
  echo "====================================="
  echo "== Følgende linjer har tom merknad =="
  echo "====================================="
  echo "${EMPTYCOMMENT}"
  echo
  EXITCODE=$((EXITCODE | ERR_EMPTY_COMMENT))
fi

if [[ "$(grep -Ec "^\s*$" "${DATABASE}")" -ne 0 ]]; then
  echo "=============================="
  echo "== Følgende linjer er tomme =="
  echo "=============================="
  grep -n '^\s*$' "${DATABASE}"
  echo
  EXITCODE=$((EXITCODE | ERR_EMPTY_LINE))
fi

DUPLICATES="$(sort "${DATABASE}" | uniq -d)"
if [[ ${DUPLICATES} ]]; then
  echo "============================================="
  echo "== Ordlista inneholder følgende duplikater =="
  echo "============================================="
  echo "${DUPLICATES}"
  echo
  EXITCODE=$((EXITCODE | ERR_DUPLICATE))
fi

MISSINGQUOTES="$(grep -v ',\s\+$' "${DATABASE}" | cut -d',' -f 4- | grep -vE '^$|^".*"$')"
if [[ ${MISSINGQUOTES} ]]; then
  echo "=============================================="
  echo "== Følgende merknader mangler anførselstegn =="
  echo "=============================================="
  echo "${MISSINGQUOTES}"
  echo
  EXITCODE=$((EXITCODE | ERR_MISSING_QUOTES))
fi

# Execute more complicated Python tests
if command_exists python3; then
  python3 ./skript/test.py "${DATABASE}"
else
  echo "Feil: Python3 ikke funnet."
  EXITCODE=$((EXITCODE | ERR_PYTHON_NOT_FOUND))
fi

# Check if EXITCODE is 0
if [[ ${EXITCODE} -eq 0 ]]; then
  echo "Alle sjekker ble gjennomført uten feil."
fi

exit ${EXITCODE}
