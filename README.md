# MeasureMySchedule

Tool for measuring Google Calendar schedule

## Installation

To generate PDFs install [wkhtmltopdf](https://wkhtmltopdf.org)

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Obtain Google API `credentials.json` by following [this docs](https://developers.google.com/calendar/quickstart/python).

## Usage

Execute CLI flow with

`python ./cli.py`

the output can be found in

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
