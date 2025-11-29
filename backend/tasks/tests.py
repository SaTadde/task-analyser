from django.test import TestCase
from datetime import date
from .scoring import calculate_score
from rest_framework.test import APIClient

class ScoringTests(TestCase):
    def test_urgency_increases_score(self):
        task_urgent = {
            "title": "Urgent Task",
            "due_date": date.today(),  # today = max urgency
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }

        task_late = {
            "title": "Later Task",
            "due_date": date(2025, 12, 31),  # far away
            "estimated_hours": 3,
            "importance": 5,
            "dependencies": []
        }

        score_urgent, _ = calculate_score(task_urgent)
        score_late, _ = calculate_score(task_late)

        self.assertGreater(score_urgent, score_late)


    def test_importance_increases_score(self):
        low = {
            "title": "Low importance",
            "due_date": date.today(),
            "estimated_hours": 3,
            "importance": 2,
            "dependencies": []
        }

        high = {
            "title": "High importance",
            "due_date": date.today(),
            "estimated_hours": 3,
            "importance": 10,
            "dependencies": []
        }

        score_low, _ = calculate_score(low)
        score_high, _ = calculate_score(high)

        self.assertGreater(score_high, score_low)


    def test_less_effort_gives_higher_score(self):
        easy = {
            "title": "Easy task",
            "due_date": date.today(),
            "estimated_hours": 1,
            "importance": 5,
            "dependencies": []
        }

        hard = {
            "title": "Hard task",
            "due_date": date.today(),
            "estimated_hours": 10,
            "importance": 5,
            "dependencies": []
        }

        score_easy, _ = calculate_score(easy)
        score_hard, _ = calculate_score(hard)

        self.assertGreater(score_easy, score_hard)


class SuggestEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_suggest_returns_top_three(self):
        tasks = [
            {
                "title": "Task A",
                "due_date": "2025-11-30",
                "estimated_hours": 3,
                "importance": 8,
                "dependencies": []
            },
            {
                "title": "Task B",
                "due_date": "2025-11-25",
                "estimated_hours": 1,
                "importance": 3,
                "dependencies": []
            },
            {
                "title": "Task C",
                "due_date": "2025-12-10",
                "estimated_hours": 7,
                "importance": 9,
                "dependencies": []
            }
        ]

        response = self.client.post("/api/tasks/suggest/", tasks, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["suggested_tasks"]), 3)
