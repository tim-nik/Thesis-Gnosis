from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from elearning.models import Lesson
from .models import LessonCompletion, PointsEvent

@login_required
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    
    obj, created = LessonCompletion.objects.get_or_create(user=request.user, lesson=lesson)
    if created:
        
        PointsEvent.objects.create(user=request.user, reason="lesson_complete", points=10, ref_id=str(lesson.id))
    return redirect("courses:lesson_detail", lesson_id=lesson.id)
