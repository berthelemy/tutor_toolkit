from django.db import models
from django.conf import settings


class School(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class SchoolMembership(models.Model):
    ROLE_ADMIN = 'admin'
    ROLE_TUTOR = 'tutor'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_TUTOR, 'Tutor'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_TUTOR)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('user', 'school')]
        indexes = [
            models.Index(fields=['user', 'school']),
        ]

    def __str__(self) -> str:
        return f"{self.user} @ {self.school}"
