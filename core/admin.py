from django.contrib import admin
from .models import Course, Chapter, Lesson, Quiz, Question, Answer, UserProgress

admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(UserProgress)
