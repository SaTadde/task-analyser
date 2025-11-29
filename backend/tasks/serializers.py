from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField()
    due_date = serializers.DateField()
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField()
    dependencies = serializers.ListField(child=serializers.CharField())

    score = serializers.FloatField(required=False)
    explanation = serializers.CharField(required=False)
