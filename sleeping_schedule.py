import datetime

import pandas as pd

import get_service

service = get_service.service

start_date = datetime.datetime(2018, 12, 14, tzinfo=datetime.timezone.utc).astimezone()
now = datetime.datetime.utcnow().astimezone().isoformat()
events_result = service.events().list(calendarId='primary', maxResults=2500,
                                      singleEvents=True,
                                      timeMin=start_date,
                                      timeMax=now,
                                      orderBy='startTime').execute()
events = [event for event in events_result.get('items', []) if event["summary"] == 'Sen']
sleeping_schedule = dict()
if not events:
    print('No events found.')
for event in events:
    start = datetime.datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date')))
    end = datetime.datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date')))
    working_hours = end - start

    sleeping_schedule.setdefault(end.date(), datetime.timedelta())
    sleeping_schedule[end.date()] += working_hours

with open("sleeping_schedule_file.csv", "w+") as file:
    for date in sleeping_schedule:
        print(date)
        print(date, sleeping_schedule[date], sep=',', file=file)

data = pd.DataFrame({'Date': list(sleeping_schedule.keys()), 'hours': list(sleeping_schedule.values())})
print(data.head())
