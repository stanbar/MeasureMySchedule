#!/bin/bash

# PhD
venv/bin/python ./cli.py 1 7 "" 1
cp out/phd/csv/latest.csv out/phd.csv
# stasbar
venv/bin/python ./cli.py 2 7 "" 1
cp out/stasbar-sp-z-o-o/csv/latest.csv out/stasbar.csv
# Dancing
venv/bin/python ./cli.py 16 7 "" 1
cp out/dancing/csv/latest.csv out/dancing.csv
# Friends
venv/bin/python ./cli.py 15 7 "" 1
cp out/friends/csv/latest.csv out/friends.csv
# Self-investement
venv/bin/python ./cli.py 12 7 "" 1
cp out/self-investment/csv/latest.csv out/self-investment.csv
# Health
venv/bin/python ./cli.py 14 7 "" 1
cp out/health/csv/latest.csv out/health.csv
# Flow
venv/bin/python ./cli.py 17 7 "" 1
cp out/flow/csv/latest.csv out/flow.csv
