from django.db import models
import json

class Task(models.Model):
    title = models.CharField(max_length=255)
    due_date = models.DateField()
    estimated_hours = models.FloatField()
    importance = models.IntegerField()
    dependencies_raw = models.TextField(default="[]")

    @property
    def dependencies(self):
        try:
            return json.loads(self.dependencies_raw)
        except:
            return []

    @dependencies.setter
    def dependencies(self, value):
        self.dependencies_raw = json.dumps(value)

    def __str__(self):
        return self.title
