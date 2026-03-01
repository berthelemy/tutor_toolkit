from django.contrib import admin

from .models import Student, StudentGroup


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school')
    list_filter = ('school',)
    search_fields = ('first_name', 'last_name')


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    list_filter = ('school',)
    search_fields = ('name',)
