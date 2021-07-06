import time
from datetime import datetime


def now_timestamp(utc=True):
    """
    获取当前时间戳
    """
    if utc is True:
        now = datetime.utcnow()
    else:
        now = datetime.now()
    timestamp = time.mktime(now.timetuple())
    return timestamp
