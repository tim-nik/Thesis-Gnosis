from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from progress.models import LessonCompletion, PointsEvent, UserBadge
from quizzes.models import QuizAttempt
from elearning.models import Course, Lesson
from progress.badges import BADGES

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)          
            return redirect("/courses/")          
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def profile(request):
    return render(request, "profile.html")

@login_required
def profile(request):
    u = request.user
    completed_ids = set(
        LessonCompletion.objects.filter(user=u).values_list("lesson_id", flat=True)
    )

    courses_data = []
    for c in Course.objects.all():
        lessons_qs = Lesson.objects.filter(chapter__course=c).order_by("chapter__order","order","id")
        total = lessons_qs.count()
        done = lessons_qs.filter(id__in=completed_ids).count()
        next_lesson = lessons_qs.exclude(id__in=completed_ids).first()
        courses_data.append({
            "course": c,
            "total_lessons": total,
            "completed_lessons": done,
            "next_lesson": next_lesson,
        })


    earned_slugs = set(UserBadge.objects.filter(user=request.user).values_list("slug", flat=True))
    badges_all = BADGES  

    context = {
        "completed_count": len(completed_ids),
        "quiz_attempts_count": QuizAttempt.objects.filter(user=u).count(),
        "total_points": PointsEvent.objects.filter(user=u).aggregate(s=Sum("points"))["s"] or 0,
        "courses_data": courses_data,
        "badges_all": badges_all,
        "badges_earned": earned_slugs,
    }
    return render(request, "profile.html", context)