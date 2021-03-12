#! /bin/sh

# Merge documents or exit if scripr fails
set -eu

printf "\nMerge documents %s to %s...\n" "${@:4}" "$1"

python3 /xlsx_to_ini_with_ref.py $1 $2 $3 "${@:4}" || { printf "\nUnable merge to %s file.\n" "$1"; exit 1; }

printf "\nSuccessfully merged to %s file.\n" "$1"