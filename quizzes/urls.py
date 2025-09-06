from django.urls import path
from . import views

app_name = "quizzes"

urlpatterns = [
    path("courses/lessons/<int:lesson_id>/quiz/", views.quiz_take, name="quiz_take"),
    path("courses/quiz/<int:attempt_id>/result/", views.quiz_result, name="quiz_result"),
]
