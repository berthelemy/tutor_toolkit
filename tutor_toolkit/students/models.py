from django.db import models

from schools.models import School


class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['school', 'last_name', 'first_name']),
        ]

    def __str__(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name


class StudentGroup(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(Student, related_name='groups', blank=True)

    class Meta:
        ordering = ['name']
        unique_together = [('school', 'name')]
        indexes = [
            models.Index(fields=['school', 'name']),
        ]

    def __str__(self) -> str:
        return self.name
