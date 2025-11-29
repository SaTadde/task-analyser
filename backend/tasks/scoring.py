from datetime import date
from .config import TASK_ANALYZER_CONFIG


def calculate_score(task):
    today = date.today()

    # 1. Urgency (how close deadline is)
    days_left = (task["due_date"] - today).days
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
