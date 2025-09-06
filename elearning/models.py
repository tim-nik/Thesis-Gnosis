from django.db import models
from django.conf import settings
from django.utils.text import slugify



class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.title or f"Course {self.pk}"

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)[:50]
        super().save(*args, **kwargs)

    class Meta:
        ordering = ("title",)  



class Chapter(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="chapters")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    class Meta:
        ordering = ("order", "id")  
        constraints = [
            
            models.UniqueConstraint(
                fields=["course", "order"],
                name="uniq_chapter_order_per_course",
            ),
        ]



class Lesson(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="lessons")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.chapter.title})"

    class Meta:
        ordering = ("order", "id")  
        constraints = [
            
            models.UniqueConstraint(
                fields=["chapter", "order"],
                name="uniq_lesson_order_per_chapter",
            ),
        ]



class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress")
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    quiz_scores = models.JSONField(default=dict)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Progress in {self.course.title}"
