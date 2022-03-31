# MeasureMySchedule

Tool for measuring Google Calendar schedule

# Installation

## wkhtmltopdf

To generate PDFs install [wkhtmltopdf](https://wkhtmltopdf.org)
```bash
brew install --cask wkhtmltopdf
```

## Python packages

```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Obtain Google API `credentials.json` by following [this docs](https://developers.google.com/calendar/quickstart/python).

# Usage

Execute CLI flow with

`python ./cli.py`

the output will be generated to the following directories:

```console
out
└── {calendar_name}
    ├── csv
    │   ├── {date-range}.csv
    ├── html
    │   ├── {date-range}.html
    └── pdf
        └── {date-range}.pdf
```
