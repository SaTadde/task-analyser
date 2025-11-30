from datetime import datetime, timedelta

# OPTIONAL: Add real holiday dates here (India example)
PUBLIC_HOLIDAYS = {
    "2025-01-26",  # Republic Day
    "2025-08-15",  # Independence Day
    "2025-10-02",  # Gandhi Jayanti
    "2025-12-25",  # Christmas
}


def is_weekend(date_obj):
    return date_obj.weekday() >= 5  # 5 = Sat, 6 = Sun


def is_holiday(date_obj):
    return date_obj.strftime("%Y-%m-%d") in PUBLIC_HOLIDAYS


def business_days_until(due_date, today=None):
    """
    Returns the number of *business* days between today and the due date.
    Weekends + holidays are skipped.
    """

    if today is None:
        today = datetime.now().date()

    if due_date < today:
        return -1  # overdue task

    days = 0
    curr = today

    while curr < due_date:
        curr += timedelta(days=1)

        # skip weekends + holidays
        if is_weekend(curr) or is_holiday(curr):
            continue

        days += 1

    return days
