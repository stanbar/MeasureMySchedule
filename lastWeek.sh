#!/bin/bash

# PhD
venv/bin/python ./cli.py 1 7 "" 1
cp out/phd/csv/Mar-2022_to_Apr-2022.csv out/phd.csv
# stasbar
venv/bin/python ./cli.py 2 7 "" 1
cp out/stasbar-sp-z-o-o/csv/Mar-2022_to_Apr-2022.csv out/stasbar.csv
# Dancing
venv/bin/python ./cli.py 16 7 "" 1
cp out/dancing/csv/Mar-2022_to_Apr-2022.csv out/dancing.csv
# Friends
venv/bin/python ./cli.py 15 7 "" 1
cp out/friends/csv/Mar-2022_to_Apr-2022.csv out/friends.csv
# Self-investement
venv/bin/python ./cli.py 12 7 "" 1
cp out/self-investement/csv/Mar-2022_to_Apr-2022.csv out/self-investment.csv
# Health
venv/bin/python ./cli.py 14 7 "" 1
cp out/health/csv/Mar-2022_to_Apr-2022.csv out/health.csv
# Flow
venv/bin/python ./cli.py 17 7 "" 1
cp out/flow/csv/Mar-2022_to_Apr-2022.csv out/flow.csv
