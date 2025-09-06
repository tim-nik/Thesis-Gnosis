from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_completions")
    lesson = models.ForeignKey("elearning.Lesson", on_delete=models.CASCADE, related_name="completions")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.user.username} → {self.lesson.title}"

   

class PointsEvent(models.Model):
    REASONS = [
        ("lesson_complete", "Ολοκλήρωση μαθήματος"),
        ("quiz_attempt",    "Σκορ κουίζ"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="points_events")
    reason = models.CharField(max_length=32, choices=REASONS)
    points = models.IntegerField(default=0)
    ref_id = models.CharField(max_length=64, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} +{self.points} ({self.reason})"

class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badges")
    slug = models.CharField(max_length=64, db_index=True)  
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(max_length=120, blank=True)  
    awarded_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)  

    class Meta:
        unique_together = ("user", "slug")

    def __str__(self):
        return f"{self.user} → {self.slug}"
