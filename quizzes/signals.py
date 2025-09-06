from django.db.models.signals import post_save
from django.dispatch import receiver
from quizzes.models import QuizAttempt, AttemptAnswer
from progress.models import PointsEvent
from progress.badges import evaluate_achievements

REASON = "quiz_attempt"  

def _calc_points_for_attempt(attempt: QuizAttempt) -> int:
    
    total = AttemptAnswer.objects.filter(attempt=attempt).count()
    if total == 0:
        return 0
    correct = AttemptAnswer.objects.filter(attempt=attempt, is_correct=True).count()
    points = correct * 5
    if correct == total:
        points += 10
    return points

@receiver(post_save, sender=QuizAttempt)
def award_points_for_quiz(sender, instance: QuizAttempt, **kwargs):
    
    
    points = _calc_points_for_attempt(instance)
    if points <= 0:
        
        return

    ref = f"quiz:{instance.quiz_id}:user:{instance.user_id}"  
    ev, created = PointsEvent.objects.get_or_create(
        user=instance.user,
        ref_id=ref,
        defaults={"points": points, "reason": REASON},
    )
    if not created and points > ev.points:
        
        ev.points = points
        ev.reason = REASON
        ev.save(update_fields=["points", "reason"])

    evaluate_achievements(instance.user)
