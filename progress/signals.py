# singal για πόντους
from django.db.models.signals import post_save
from django.dispatch import receiver
from progress.badges import evaluate_achievements
from progress.models import LessonCompletion, PointsEvent

@receiver(post_save, sender=LessonCompletion)
def on_lesson_completed(sender, instance, created, **kwargs):
    if created:
        evaluate_achievements(instance.user)

@receiver(post_save, sender=PointsEvent)
def on_points_event(sender, instance, created, **kwargs):
   
    evaluate_achievements(instance.user)
