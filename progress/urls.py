from django.urls import path
from . import views

app_name = "progress"
urlpatterns = [
    path("lessons/<int:lesson_id>/complete/", views.complete_lesson, name="lesson_complete"),
]
