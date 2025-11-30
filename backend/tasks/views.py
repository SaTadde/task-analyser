from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .validator import validate_task, TaskValidationError
from .dependency_check import detect_cycle
from .config import TASK_ANALYZER_CONFIG

from .scoring import (
    calculate_score,
    strategy_fastest,
    strategy_high_impact,
    strategy_deadline_driven
)


class AnalyzeTasks(APIView):
    def post(self, request):
        raw_tasks = request.data

        # ---------------------------
        # STEP 1: VALIDATE EACH TASK
        # ---------------------------
        validated_tasks = []
        for t in raw_tasks:
            try:
                validated_tasks.append(validate_task(t))
            except TaskValidationError as e:
                return Response(
                    {"error": "Invalid task data", "details": e.args[0]},
                    status=400
                )

        # ---------------------------------------
        # STEP 2: CIRCULAR DEPENDENCY DETECTION
        # ---------------------------------------
        # STEP 2: CIRCULAR DEPENDENCY DETECTION (new behavior)
        has_cycle, cycle_nodes = detect_cycle(validated_tasks)
        

        # ---------------------------
        # STEP 3: APPLY STRATEGY
        # ---------------------------
        strategy = request.query_params.get("strategy", "smart")

        # FASTEST WINS
        if strategy == "fastest":
            sorted_tasks = strategy_fastest(validated_tasks)

        # HIGH IMPACT
        elif strategy == "high_impact":
            sorted_tasks = strategy_high_impact(validated_tasks)

        # DEADLINE DRIVEN
        elif strategy == "deadline":
            sorted_tasks = strategy_deadline_driven(validated_tasks)

        # SMART BALANCE (DEFAULT)
        else:
            for task in validated_tasks:
                score, explanation = calculate_score(task)
                task["score"] = score
                task["explanation"] = explanation

            sorted_tasks = sorted(
                validated_tasks,
                key=lambda t: t["score"],
                reverse=True
            )

        return Response({
            "tasks": sorted_tasks,
            "has_cycle": has_cycle,
            "cycle_nodes": cycle_nodes
        })



class SuggestTasks(APIView):
    def post(self, request):
        raw_tasks = request.data

        # ---------------------------
        # STEP 1: VALIDATE TASKS
        # ---------------------------
        validated_tasks = []
        for t in raw_tasks:
            try:
                validated_tasks.append(validate_task(t))
            except TaskValidationError as e:
                return Response(
                    {"error": "Invalid task data", "details": e.args[0]},
                    status=400
                )

        # ---------------------------------------
        # STEP 2: CIRCULAR DEPENDENCY DETECTION
        # ---------------------------------------
        # if TASK_ANALYZER_CONFIG["CHECK_CIRCULAR_DEPENDENCIES"]:
        #     if detect_cycle(validated_tasks):
        #         return Response(
        #             {"error": "Circular dependency detected"},
        #             status=400
        #         )
        has_cycle, cycle_nodes = detect_cycle(validated_tasks)

        # ---------------------------
        # STEP 3: SMART SCORE
        # ---------------------------
        for task in validated_tasks:
            score, explanation = calculate_score(task)
            task["score"] = score
            task["explanation"] = explanation

        ranked = sorted(validated_tasks, key=lambda t: t["score"], reverse=True)

        # ---------------------------
        # STEP 4: TOP 3
        # ---------------------------
        top3 = ranked[:3]

        return Response({
            "suggested_tasks": top3,
            "has_cycle": has_cycle,
            "cycle_nodes": cycle_nodes,
            "note": "Top 3 tasks using Smart Balance scoring."
    })

