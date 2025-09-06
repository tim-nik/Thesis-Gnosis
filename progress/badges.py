from dataclasses import dataclass
from typing import Callable, Dict
from django.apps import apps
from django.utils import timezone
from progress.models import LessonCompletion
from .models import UserBadge

@dataclass(frozen=True)
class BadgeRule:
    slug: str
    title: str
    description: str
    icon: str  
    condition: Callable[[dict], bool]  


from django.db.models import Count, Q, F, Sum

def collect_metrics(user):
    
    from quizzes.models import QuizAttempt, AttemptAnswer
    from progress.models import LessonCompletion, PointsEvent
    from elearning.models import Course, Lesson

    
    completed_count = (
        LessonCompletion.objects
        .filter(user=user)
        .values("lesson_id").distinct().count()
    )

    
    per_attempt = (
        AttemptAnswer.objects
        .filter(attempt__user=user)
        .values("attempt_id")
        .annotate(total=Count("id"),
                  correct=Count("id", filter=Q(is_correct=True)))
    )
    perfect_exists = per_attempt.filter(total__gt=0, total=F("correct")).exists()

    
    points = PointsEvent.objects.filter(user=user).aggregate(s=Sum("points"))["s"] or 0

    
    any_course_complete = False
    for c in Course.objects.all():
        total = Lesson.objects.filter(chapter__course=c).count()
        if total == 0:
            continue
        done = (
            LessonCompletion.objects
            .filter(user=user, lesson__chapter__course=c)
            .values("lesson_id").distinct().count()
        )
        if done == total:
            any_course_complete = True
            break

    return {
        "completed_count": completed_count,
        "perfect_exists": perfect_exists,
        "any_course_complete": any_course_complete,
        "points": points,
    }

#  6 
BADGES = [
    BadgeRule(
        slug="first_lesson",
        title="Πρώτα Βήματα",
        description="Ολοκλήρωσε 1 μάθημα",
        icon="/badges/first_steps.svg",  
        condition=lambda m: m["completed_count"] >= 1,
    ),
    BadgeRule(
        slug="perfect_quiz",
        title="Αριστούχος",
        description="Τέλειο σκορ σε ένα κουίζ",
        icon="/badges/valedictorian.svg",
        condition=lambda m: m["perfect_exists"],
    ),
    BadgeRule(
        slug="course_complete_any",
        title="Ολοκλήρωση Μαθήματος",
        description="Ολοκλήρωσε ολόκληρο το μάθημα",
        icon="/badges/complete_course.svg",
        condition=lambda m: m["any_course_complete"],
    ),
    BadgeRule(
        slug="points_50",
        title="Ήρωας των Πόντων",
        description="Φτάσε τους 50 πόντους",
        icon="/badges/50.svg",
        condition=lambda m: m["points"] >= 50,
    ),
    BadgeRule(
        slug="points_100",
        title="Κατακτητής Πόντων",
        description="Φτάσε τους 100 πόντους",
        icon="/badges/100.svg",
        condition=lambda m: m["points"] >= 100,
    ),
    BadgeRule(
        slug="points_200",
        title="Πρωταθλητής Πόντων",
        description="Φτάσε τους 200 πόντους",
        icon="/badges/200.svg",
        condition=lambda m: m["points"] >= 200,
    ),
]


def evaluate_achievements(user) -> int:
    
    metrics = collect_metrics(user)
    awarded_now = 0

    owned = set(UserBadge.objects.filter(user=user).values_list("slug", flat=True))

    for rule in BADGES:
        if rule.slug in owned:
            continue
        if rule.condition(metrics):
            UserBadge.objects.create(
                user=user,
                slug=rule.slug,
                title=rule.title,
                description=rule.description,
                icon=rule.icon,
                awarded_at=timezone.now(),
            )
            awarded_now += 1

    return awarded_now
