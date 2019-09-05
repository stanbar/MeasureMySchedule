# MeasureMySchedule
Python utils for measuring Google Calendar schedule

## Installation
```
git clone https://github.com/stasbar/MeasureMySchedule.git
cd MeasureMySchedule
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Obtain Google API `credentials.json` by following [this docs](https://developers.google.com/calendar/quickstart/python).

## Usage
### print_calendars.py
Will let you find `calendarId` required to filter your schedule.

### working_schedule.py
```
Usage:
  working_schedule.py all
  working_schedule.py [--prev] month MONTH [to MONTHS-COUNT]
  working_schedule.py (-h | --help)

Options:
  -h --help     Show this screen.
  --last        use MONTH to shift back from current month
```


