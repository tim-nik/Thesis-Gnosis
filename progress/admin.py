from django.contrib import admin
from .models import LessonCompletion, PointsEvent

@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ("user","lesson","completed_at")
    search_fields = ("user__username","lesson__title")
    list_filter = ("completed_at",)

@admin.register(PointsEvent)
class PointsEventAdmin(admin.ModelAdmin):
    list_display = ("user","reason","points","created_at","ref_id")
    search_fields = ("user__username","ref_id")
    list_filter = ("reason","created_at")
