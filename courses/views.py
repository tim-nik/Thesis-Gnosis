from django.shortcuts import render, get_object_or_404, redirect
from elearning.models import Course, Lesson
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from elearning.models import Lesson
from progress.models import LessonCompletion
from django.db.models import Count

def course_list(request):
    courses = Course.objects.all().order_by("title")
    return render(request, "courses/course_list.html", {"courses": courses})

def _context_for_course(course):
    
    chapters = course.chapters.prefetch_related("lessons").order_by("order", "id")
    
    lessons = (Lesson.objects
               .filter(chapter__course=course)
               .select_related("chapter")
               .order_by("chapter__order", "order", "id"))
    return {"course": course, "chapters": chapters, "lessons": lessons}

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    chapters = course.chapters.prefetch_related("lessons").order_by("order", "id")
    lessons = (Lesson.objects
               .filter(chapter__course=course)
               .order_by("chapter__order", "order", "id"))
    return render(request, "courses/course_detail.html",
                  {"course": course, "chapters": chapters, "lessons": lessons})

def course_detail_by_id(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    chapters = course.chapters.prefetch_related("lessons").order_by("order", "id")
    lessons = (Lesson.objects
               .filter(chapter__course=course)
               .order_by("chapter__order", "order", "id"))
    return render(request, "courses/course_detail.html",
                  {"course": course, "chapters": chapters, "lessons": lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = lesson.chapter.course
    chapter = lesson.chapter

    
    ordered = (Lesson.objects
               .filter(chapter__course=course)
               .select_related("chapter")
               .order_by("chapter__order", "order", "id")
               .values_list("id", flat=True))

    

    has_published_quiz = lesson.quizzes.filter(is_published=True).exists()

    ids = list(ordered)
    i = ids.index(lesson.id)
    prev_id = ids[i-1] if i > 0 else None
    next_id = ids[i+1] if i < len(ids)-1 else None

    completed = False
    if request.user.is_authenticated:
        completed = LessonCompletion.objects.filter(user=request.user, lesson=lesson).exists()

    # συνολικός αριθμός μαθημάτων  
    total_lessons = Lesson.objects.filter(chapter__course=course).count()
    completed_in_course = 0
    if request.user.is_authenticated:
        completed_in_course = LessonCompletion.objects.filter(
            user=request.user, lesson__chapter__course=course
        ).count()

    context = {
        "lesson": lesson, "chapter": chapter, "course": course,
        "prev_id": prev_id, "next_id": next_id,
        "has_published_quiz": has_published_quiz,
        "completed": completed,
        "total_lessons": total_lessons,
        "completed_in_course": completed_in_course,
    }

    return render(request, "courses/lesson_detail.html", context)


