from django.contrib import admin

from .models import HomeworkTask, Lesson, LessonNote, LessonObjective, LessonResource


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('start_datetime', 'duration_minutes', 'school', 'tutor', 'group', 'student')
    list_filter = ('school',)
    search_fields = ('group__name', 'student__first_name', 'student__last_name', 'tutor__username')


@admin.register(LessonObjective)
class LessonObjectiveAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'text')


@admin.register(LessonResource)
class LessonResourceAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'title', 'url')


@admin.register(HomeworkTask)
class HomeworkTaskAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'due_date', 'is_completed')


@admin.register(LessonNote)
class LessonNoteAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'created_at')
