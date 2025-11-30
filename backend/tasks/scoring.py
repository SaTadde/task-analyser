from datetime import date
from .config import TASK_ANALYZER_CONFIG
from datetime import datetime
from .date_intel import business_days_until

    
def calculate_score(task):
    today = date.today()

    # 1. Urgency (how close deadline is)

    today = datetime.now().date()
    days_left = business_days_until(task["due_date"], today)

    if days_left < 0:
        urgency = 10   # overdue = extremely urgent
    elif days_left == 0:
        urgency = 9
    elif days_left == 1:
        urgency = 8
    elif days_left <= 3:
        urgency = 7
    elif days_left <= 7:
        urgency = 5
    else:
        urgency = 2

    urgency = max(0, 10 - max(0, days_left))
    urgency = min(10, urgency)

    # 2. Importance
    importance = int(task["importance"])

    # 3. Effort reduction
    effort = int(task["estimated_hours"])
    effort_penalty = max(1, effort / 10)

    # Weighted scoring
    score = (
        urgency * TASK_ANALYZER_CONFIG["URGENCY_WEIGHT"] +
        importance * TASK_ANALYZER_CONFIG["IMPORTANCE_WEIGHT"]
    ) / effort_penalty

    explanation = (
        f"Urgency={urgency}, Importance={importance}, Effort={effort}"
    )

    return round(score, 2), explanation


def strategy_fastest(tasks):
    return sorted(tasks, key=lambda t: int(t["estimated_hours"]))


def strategy_high_impact(tasks):
    return sorted(tasks, key=lambda t: int(t["importance"]), reverse=True)


def strategy_deadline_driven(tasks):
    return sorted(tasks, key=lambda t: t["due_date"])
