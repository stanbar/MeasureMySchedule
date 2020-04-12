from datetime import datetime

def starting_date(calendar_id):
    if(calendar_id == 'a8sfsb3mjdjpmlugufrsbrqu40@group.calendar.google.com'):
        # Master Thesis
        return None
    if(calendar_id == 'stasbar1995@gmail.com'):
        # general calendaer
        return None
    if(calendar_id == 'jrlvs1halm7i3q32472tpaq334@group.calendar.google.com'):
        # sleep
        return datetime(2018, 12, 14, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
    if(calendar_id == 'p56scqq1jcbou0djtdcsebrchg@group.calendar.google.com'):
        # Stellot
        return datetime(2019, 10, 1, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
    if(calendar_id == '8ekhu84i727iv8f8nkju326qmg@group.calendar.google.com'):
        # stasbar sp.z o.o.
        return datetime(2019, 5, 14, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
    if(calendar_id == 'i5lg1jhj0icms3ho9d67e88o1o@group.calendar.google.com'):
        # ZDRone
        return datetime(2019, 1, 14, tzinfo=datetime.timezone.utc).astimezone().replace(hour=0, minute=0)
    if(calendar_id == '76k2cbn06li92mc3d61a64f504@group.calendar.google.com'):
        # KTI
        return None