from datetime import datetime, timedelta


def time_ago(time):
    local_time = time + timedelta(hours=7)
    now = datetime.now()
    delta = now - local_time

    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f'{seconds} giây trước'

    minutes = seconds // 60

    if minutes < 60:
        return f'{minutes} phút trước'

    hours = minutes // 60

    if hours < 24:
        return f'{hours} giờ trước'

    days = hours // 24

    return f'{days} ngày trước'
