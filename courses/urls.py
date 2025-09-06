from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),                        # /courses/
    path("<slug:slug>/", views.course_detail, name="course_detail"),        # /courses/math
    path("<int:course_id>/", views.course_detail_by_id, name="course_detail_by_id"),
    path("lessons/<int:lesson_id>/", views.lesson_detail, name="lesson_detail"),
]
