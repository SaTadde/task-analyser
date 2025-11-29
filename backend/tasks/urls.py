from django.urls import path
from .views import AnalyzeTasks, SuggestTasks

urlpatterns = [
    path('analyze/', AnalyzeTasks.as_view()),
    path('suggest/', SuggestTasks.as_view()),
]
