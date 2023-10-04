#!/bin/bash

DATABASE="./verifiserte_termer.csv"

ERR_DB_NOT_FOUND=1
ERR_PYTHON_NOT_FOUND=2

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

# Validate term table with python script
if command_exists python3; then
  python3 ./skript/valider_termtabell.py "${DATABASE}"
  # Capture the exit code of the Python script
  PYTHON_SCRIPT_EXITCODE=$?
  # OR it with the existing EXITCODE
  EXITCODE=$((EXITCODE | PYTHON_SCRIPT_EXITCODE))
else
  echo "Feil: Python3 ikke funnet."
  EXITCODE=$((EXITCODE | ERR_PYTHON_NOT_FOUND))
fi

# Check if EXITCODE is 0
if [[ ${EXITCODE} -eq 0 ]]; then
  echo "Alle sjekker ble gjennomført uten feil."
fi

exit ${EXITCODE}
