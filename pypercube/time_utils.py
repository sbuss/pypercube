from datetime import datetime
from datetime import timedelta

STEP_10_SEC = long(1e4)
STEP_1_MIN = long(6e4)
STEP_5_MIN = long(3e5)
STEP_1_HOUR = long(36e5)
STEP_1_DAY = long(864e5)

STEP_CHOICES = (
        (STEP_10_SEC, "10 seconds"),
        (STEP_1_MIN, "1 minute"),
        (STEP_5_MIN, "5 minutes"),
        (STEP_1_HOUR, "1 hour"),
        (STEP_1_DAY, "1 day"))


def now():
    return datetime.utcnow()


def yesterday():
    return now() - timedelta(days=1)


def last_week():
    return now() - timedelta(days=7)


def start_of_month(timestamp=None):
    if not timestamp:
        timestamp = now()
    return datetime(year=timestamp.year, month=timestamp.month, day=1)
