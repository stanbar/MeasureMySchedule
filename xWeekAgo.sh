#!/bin/bash
LAST_N_WEEKS=${1:-1}

# PhD
venv/bin/python ./cli.py 9 9 $LAST_N_WEEKS "" 1
cp out/phd/csv/latest.csv out/phd.csv
# stasbar
venv/bin/python ./cli.py 15 9 $LAST_N_WEEKS "" 1
cp out/stasbar-sp-z-o-o/csv/latest.csv out/stasbar.csv
# Dancing
venv/bin/python ./cli.py 4 9 $LAST_N_WEEKS "" 1
cp out/dancing/csv/latest.csv out/dancing.csv
# Friends
venv/bin/python ./cli.py 7 9 $LAST_N_WEEKS "" 1
cp out/friends/csv/latest.csv out/friends.csv
# Self-investement
venv/bin/python ./cli.py 8 9 $LAST_N_WEEKS "" 1
cp out/self-investment/csv/latest.csv out/self-investment.csv
# Health
venv/bin/python ./cli.py 3 9 $LAST_N_WEEKS "" 1
cp out/health/csv/latest.csv out/health.csv
# Flow
venv/bin/python ./cli.py 5 9 $LAST_N_WEEKS "" 1
cp out/flow/csv/latest.csv out/flow.csv
# Psychology
venv/bin/python ./cli.py 18 9 $LAST_N_WEEKS "" 1
cp out/psychology/csv/latest.csv out/psychology.csv
