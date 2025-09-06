from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt, AttemptAnswer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'is_published', 'created_at')
    list_filter = ('is_published', 'lesson__chapter__course')
    search_fields = ('title', 'lesson__title')
    inlines = [QuestionInline]

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'order')
    list_filter = ('quiz',)
    search_fields = ('text',)
    inlines = [ChoiceInline]

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'total', 'submitted_at')
    list_filter = ('quiz', 'submitted_at')
    search_fields = ('user__username', 'quiz__title')

@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_choice', 'is_correct')
    list_filter = ('is_correct', 'question__quiz')
