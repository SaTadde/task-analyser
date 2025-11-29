TASK_ANALYZER_CONFIG = {
    # Validation behavior
    "ALLOW_PAST_DATES": True,           # Reject or allow overdue tasks
    "CHECK_CIRCULAR_DEPENDENCIES": True,

    # Defaults for missing fields
    "DEFAULT_IMPORTANCE": 5,
    "DEFAULT_ESTIMATED_HOURS": 1,

    # Limits
    "MAX_ESTIMATED_HOURS": 100,

    # Scoring weights (can be tuned)
    "URGENCY_WEIGHT": 1.0,
    "IMPORTANCE_WEIGHT": 1.0,
    "EFFORT_WEIGHT": 1.0,   # higher effort reduces score
}
