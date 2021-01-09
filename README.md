# MeasureMySchedule

Python utils for measuring Google Calendar schedule

## Installation

```console
git clone https://github.com/stasbar/MeasureMySchedule.git
cd MeasureMySchedule
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Obtain Google API `credentials.json` by following [this docs](https://developers.google.com/calendar/quickstart/python).

## Usage

Execute cli flow with

`python cli.py`

after completing all steps the program will output

```console
out
└── {calendar_name}
    ├── csv
    │   ├── {daterange}.csv
    ├── html
    │   ├── {daterange}.html
    └── pdf
        └── {daterange}.pdf
```
