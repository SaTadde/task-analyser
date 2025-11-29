from datetime import datetime, date
from .config import TASK_ANALYZER_CONFIG

REQUIRED_FIELDS = ["title", "due_date", "estimated_hours", "importance", "dependencies"]


class TaskValidationError(Exception):
    pass


def validate_task(task):
    errors = {}

    # 1. Missing fields
    for field in REQUIRED_FIELDS:
        if field not in task:
            errors[field] = "Missing field"

    if errors:
        raise TaskValidationError(errors)

    # 2. Title validation
    if not isinstance(task["title"], str) or task["title"].strip() == "":
        errors["title"] = "Title must be a non-empty string"

    # 3. Date validation
    try:
        parsed_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
    except:
        errors["due_date"] = "Invalid date format. Use YYYY-MM-DD"

    if "ALLOW_PAST_DATES" in TASK_ANALYZER_CONFIG:
        allow = TASK_ANALYZER_CONFIG["ALLOW_PAST_DATES"]
        if not allow and parsed_date < date.today():
            errors["due_date"] = "Past due dates are not allowed"

    # 4. Estimated hours
    try:
        hours = int(task["estimated_hours"])
        if hours <= 0:
            errors["estimated_hours"] = "Must be a positive integer"
        if hours > TASK_ANALYZER_CONFIG["MAX_ESTIMATED_HOURS"]:
            errors["estimated_hours"] = "Exceeds allowed max"
    except:
        errors["estimated_hours"] = "Must be an integer"

    # 5. Importance
    try:
        imp = int(task["importance"])
        if imp < 1 or imp > 10:
            errors["importance"] = "Must be between 1 and 10"
    except:
        errors["importance"] = "Must be an integer"

    if errors:
        raise TaskValidationError(errors)

    # If all good → replace string date with date object
    task["due_date"] = parsed_date

    return task
