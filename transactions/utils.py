from datetime import datetime, timedelta


def _calculate_next_date(start_date: datetime, interval: str) -> datetime:
    if interval == "WEEKLY":
        return start_date + timedelta(weeks=1)

    if interval == "MONTHLY":
        month = start_date.month + 1
        year = start_date.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1

        import calendar
        day = min(start_date.day, calendar.monthrange(year, month)[1])
        return start_date.replace(year=year, month=month, day=day)

    if interval == "YEARLY":
        try:
            return start_date.replace(year=start_date.year + 1)
        except ValueError:
            return start_date.replace(year=start_date.year + 1, day=28)

    return start_date