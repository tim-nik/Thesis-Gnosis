from django.contrib import admin
from .models import Course, Chapter, Lesson, UserProgress

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created_at")
    search_fields = ("title", "slug")
    ordering = ("title",)
    prepopulated_fields = {"slug": ("title",)}

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("title", "order")
    ordering = ("order",)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order", "created_at")
    list_filter = ("course",)
    search_fields = ("title",)
    ordering = ("course", "order", "id")
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "chapter", "order", "created_at")
    list_filter = ("chapter__course", "chapter")
    search_fields = ("title",)
    ordering = ("chapter", "order", "id")




admin.site.register(UserProgress)
