from __future__ import annotations

from django import forms

from .models import Student, StudentGroup


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name']


class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = StudentGroup
        fields = ['name', 'students']

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        if school is not None:
            self.fields['students'].queryset = Student.objects.filter(school=school).order_by('last_name', 'first_name')
        else:
            self.fields['students'].queryset = Student.objects.none()
