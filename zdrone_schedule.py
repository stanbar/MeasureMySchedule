"""
Usage:
  zdrone_schedule.py all
  zdrone_schedule.py [--prev] month MONTH [to MONTHS-COUNT]
  zdrone_schedule.py (-h | --help)

Options:
  -h --help     Show this screen.
  --last        use MONTH to shift back from current month
"""

import datetime
import os
import pandas as pd
import pdfkit
from dateutil.relativedelta import relativedelta
import get_service
from utils import strfdelta
from docopt import docopt

nowDate = datetime.datetime.now(datetime.timezone.utc).astimezone()
fromDate = datetime.datetime(2019, 1, 14, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
toDate = nowDate
if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['all']:
        fromDate = datetime.datetime(2019, 1, 14, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
        toDate = nowDate

    elif arguments['month']:
        month = int(arguments['MONTH'])
        if arguments['--prev']:
            fromDate = nowDate.replace(day=1, hour=0, minute=0, second=0) - relativedelta(months=month)
        else:
            fromDate = datetime.datetime(year=datetime.datetime.now().year, month=month, day=1,
                                         tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)

        if fromDate < datetime.datetime(2019, 1, 14, tzinfo=datetime.timezone.utc) \
                .astimezone().replace(hour=0, minute=0):
            fromDate = datetime.datetime(2019, 1, 14, 0, 0, tzinfo=datetime.timezone.utc) \
                .astimezone().replace(hour=0, minute=0)

        if arguments['to']:
            monthsCount = int(arguments['MONTHS-COUNT'])
        else:
            monthsCount = 1
        toDate = fromDate.replace(day=1) + relativedelta(months=monthsCount) - relativedelta(minutes=1)

print('From', fromDate)
print('To', toDate)
service = get_service.service

if fromDate.year == toDate.year and fromDate.month == toDate.month:
    file_name = fromDate.strftime("%b-%Y")
else:
    file_name = f'{fromDate.strftime("%b-%Y")}_to_{toDate.strftime("%b-%Y")}'

csv_file_path = f'out/csv/{file_name}.csv'
html_file_path = f'out/html/{file_name}.html'
pdf_file_path = f'out/pdf/{file_name}.pdf'
os.makedirs('out/csv', exist_ok=True)
os.makedirs('out/html', exist_ok=True)
os.makedirs('out/pdf', exist_ok=True)

events_result = service.events().list(calendarId="i5lg1jhj0icms3ho9d67e88o1o@group.calendar.google.com",
                                      maxResults=2500,
                                      singleEvents=True,
                                      timeMax=toDate.isoformat(),
                                      timeMin=fromDate.isoformat(),
                                      orderBy='startTime').execute()
events = events_result.get('items', [])
working_schedule = dict()
if not events:
    print('No events found.')
for event in events:
    start = datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
    if start < fromDate:
        start = fromDate
    end = datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
    if end > toDate:
        end = toDate
    working_hours = end - start

    working_schedule.setdefault(end.date(), datetime.timedelta())
    working_schedule[end.date()] += working_hours

with open(csv_file_path, "w+") as file:
    print("Data", "Czas pracy", sep=',', file=file)
    for date in working_schedule:
        print(date, working_schedule[date], sep=',', file=file)

dataFrameable = dict()
for key, value in working_schedule.items():
    dataFrameable[key] = (value,)

df = pd.DataFrame.from_dict(dataFrameable, orient='index', columns=['Czas pracy'])
total_duration_iso = strfdelta(df["Czas pracy"].sum(), "{H}h")

df = df.applymap(lambda entry: strfdelta(entry, "{H}h {M}m"))
df.loc['Suma'] = total_duration_iso

df.to_html(html_file_path, header=True, index=True)
pdfkit.from_file(html_file_path, pdf_file_path)
