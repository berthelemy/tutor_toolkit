from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from schools.models import School
from students.models import Student, StudentGroup


class Lesson(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    tutor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    start_datetime = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)

    group = models.ForeignKey(StudentGroup, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-start_datetime']
        indexes = [
            models.Index(fields=['school', 'start_datetime']),
        ]

    def clean(self):
        super().clean()

        if self.duration_minutes <= 0:
            raise ValidationError({'duration_minutes': _('Duration must be greater than 0.')})

        if (self.group is None and self.student is None) or (self.group is not None and self.student is not None):
            raise ValidationError(_('A lesson must have exactly one of group or student set.'))

        if self.school_id is not None:
            if self.group is not None and self.group.school_id != self.school_id:
                raise ValidationError({'group': _('Selected group is not in the current school.')})

            if self.student is not None and self.student.school_id != self.school_id:
                raise ValidationError({'student': _('Selected student is not in the current school.')})

    def __str__(self) -> str:
        target = self.group or self.student
        return f"{self.start_datetime} - {target}"


class LessonObjective(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='objectives')
    text = models.TextField()

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.text


class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.title


class HomeworkTask(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='homework_tasks')
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.description


class LessonNote(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='notes')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:
        return self.content
