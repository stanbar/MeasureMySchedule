
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import os
from get_service import service

nowDate = datetime.now(timezone.utc).astimezone()
fromDate = datetime(2019, 5, 14, tzinfo=timezone.utc).astimezone().replace(
    hour=0, minute=0)
toDate = nowDate


def last_months(calendar_id, last_months: int):
    from_date = nowDate.replace(
        day=1, hour=0, minute=0, second=0) - relativedelta(months=last_months)

    to_date = from_date.replace(
        day=1) + relativedelta(months=1) - relativedelta(minutes=1)

    return from_date, to_date


def from_to(calendar_id, month_from: int, month_to: int, year=None):
    from_date = datetime(year=datetime.now().year, month=month_from, day=1,
                         tzinfo=timezone.utc).astimezone().replace(hour=0, minute=0)
    if from_date < datetime(2019, 5, 14, tzinfo=timezone.utc) \
            .astimezone().replace(hour=0, minute=0):
        from_date = datetime(2019, 5, 14, 0, 0, tzinfo=timezone.utc) \
            .astimezone().replace(hour=0, minute=0)

    to_date = from_date.replace(
        day=1) + relativedelta(months=1) - relativedelta(minutes=1)

    return from_date, to_date


def execute(calendar_id, from_date, to_date) -> dict:
    events_result = service.events().list(calendarId=calendar_id,
                                          maxResults=2500,
                                          singleEvents=True,
                                          timeMax=to_date.isoformat(),
                                          timeMin=from_date.isoformat(),
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    working_schedule = dict()
    if not events:
        print('No events found.')
    for event in events:
        start = datetime.fromisoformat(
            event['start'].get('dateTime', event['start'].get('date')))
        if start < fromDate:
            start = fromDate
        end = datetime.fromisoformat(
            event['end'].get('dateTime', event['end'].get('date')))
        if end > toDate:
            end = toDate
        working_hours = end - start

        working_schedule.setdefault(end.date(), timedelta())
        working_schedule[end.date()] += working_hours

    return working_schedule
