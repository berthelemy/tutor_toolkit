from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _

from students.models import Student, StudentGroup

from .models import HomeworkTask, Lesson, LessonNote, LessonObjective, LessonResource


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['start_datetime', 'duration_minutes', 'group', 'student']
        labels = {
            'start_datetime': _('Date and time'),
            'duration_minutes': _('Duration (minutes)'),
            'group': _('Group'),
            'student': _('Student'),
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)

        self.school = school

        self.fields['start_datetime'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        )
        self.fields['start_datetime'].input_formats = [
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d %H:%M:%S',
        ]
        self.fields['start_datetime'].help_text = _('Format: YYYY-MM-DD HH:MM (or use the picker)')

        if self.instance and self.instance.pk and self.instance.start_datetime:
            self.initial['start_datetime'] = self.instance.start_datetime.strftime('%Y-%m-%dT%H:%M')

        if school is not None:
            self.fields['group'].queryset = StudentGroup.objects.filter(school=school).order_by('name')
            self.fields['student'].queryset = Student.objects.filter(school=school).order_by('last_name', 'first_name')
        else:
            self.fields['group'].queryset = StudentGroup.objects.none()
            self.fields['student'].queryset = Student.objects.none()

    def clean(self):
        cleaned_data = super().clean()

        if self.school is not None:
            self.instance.school = self.school

        group = cleaned_data.get('group')
        student = cleaned_data.get('student')

        if (group is None and student is None) or (group is not None and student is not None):
            raise forms.ValidationError(_('Please choose exactly one of Group or Student.'))

        if self.school is not None:
            if group is not None and group.school_id != self.school.id:
                self.add_error('group', _('Selected group is not in the current school.'))
            if student is not None and student.school_id != self.school.id:
                self.add_error('student', _('Selected student is not in the current school.'))

        return cleaned_data


class LessonObjectiveForm(forms.ModelForm):
    class Meta:
        model = LessonObjective
        fields = ['text']


class LessonResourceForm(forms.ModelForm):
    class Meta:
        model = LessonResource
        fields = ['title', 'url', 'notes']


class HomeworkTaskForm(forms.ModelForm):
    class Meta:
        model = HomeworkTask
        fields = ['description', 'due_date', 'is_completed']


class LessonNoteForm(forms.ModelForm):
    class Meta:
        model = LessonNote
        fields = ['content']
