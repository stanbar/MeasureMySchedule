from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
import os
from get_service import service
from typing import NamedTuple

nowDate = datetime.now(timezone.utc).astimezone()
fromDate = (
    datetime(2019, 5, 14, tzinfo=timezone.utc).astimezone().replace(hour=0, minute=0)
)


def last_months(last_months: int):
    from_date = nowDate.replace(day=1, hour=0, minute=0, second=0) - relativedelta(
        months=last_months
    )

    to_date = (
        from_date.replace(day=1) + relativedelta(months=last_months) - relativedelta(minutes=1)
    )

    return from_date, to_date


def last_days(last_days: int):
    from_date = nowDate.replace(hour=0, minute=0, second=0) - relativedelta(
        days=last_days
    )
    to_date = nowDate.replace(hour=0, minute=0, second=0) - relativedelta(seconds=1)

    return from_date, to_date


def from_to(month_from: int, month_to: int, year=None):
    from_date = (
        datetime(year=datetime.now().year, month=month_from, day=1, tzinfo=timezone.utc)
        .astimezone()
        .replace(hour=0, minute=0)
    )
    if from_date < datetime(2019, 5, 14, tzinfo=timezone.utc).astimezone().replace(
        hour=0, minute=0
    ):
        from_date = (
            datetime(2019, 5, 14, 0, 0, tzinfo=timezone.utc)
            .astimezone()
            .replace(hour=0, minute=0)
        )

    to_date = (
            datetime(year=datetime.now().year, month=month_to, day=1, tzinfo=timezone.utc) + relativedelta(months=1) - relativedelta(minutes=1)
    )

    return from_date, to_date


class Result(NamedTuple):
    by_date: dict
    by_task: dict


def execute(calendar_ids, from_date, to_date, filter: str) -> Result:
    by_date = dict()
    by_task = dict()
    for calendar_id in calendar_ids:
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                maxResults=2500,
                singleEvents=True,
                timeMax=to_date.isoformat(),
                timeMin=from_date.isoformat(),
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        if not events:
            print("No events found.")

        # https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#get
        for event in events:
            title = event["summary"]

            # handle filter
            if filter is not None and filter.lower() not in title.lower():
                continue

            description = event.get("description")
            start = datetime.fromisoformat(
                event["start"].get("dateTime", event["start"].get("date"))
            )
            if start < fromDate:
                start = fromDate
            end = datetime.fromisoformat(
                event["end"].get("dateTime", event["end"].get("date"))
            )
            if end > nowDate:
                end = nowDate
            working_hours = end - start
            print(
                f'date: "{end.date()}" title: "{title}"; description: "{description}"'
            )
            by_date.setdefault(end.date(), timedelta())
            by_date[end.date()] += working_hours
            if description and description.startswith("FEEL"):
                by_task.setdefault(description, timedelta())
                by_task[description] += working_hours
            else:
                by_task.setdefault(title, timedelta())
                by_task[title] += working_hours

    return Result(by_date, by_task)
