import get_service

service = get_service.service

calendars_result = service.calendarList().list().execute()
calendars = calendars_result.get('items', [])
for cal in calendars:
    print(cal)
