from __future__ import annotations

from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from lessons.models import Lesson
from schools.utils import get_current_school
from students.models import Student


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None


@login_required
def day_view(request: HttpRequest) -> HttpResponse:
    current_school = get_current_school(request)
    if current_school is None:
        return redirect('home')

    selected_date = _parse_date(request.GET.get('date')) or timezone.localdate()
    start_dt = timezone.make_aware(datetime.combine(selected_date, datetime.min.time()))
    end_dt = start_dt + timedelta(days=1)

    lessons = (
        Lesson.objects.filter(school=current_school, start_datetime__gte=start_dt, start_datetime__lt=end_dt)
        .select_related('group', 'student')
        .order_by('start_datetime')
    )

    return render(
        request,
        'dashboard/day.html',
        {
            'selected_date': selected_date,
            'lessons': lessons,
        },
    )


@login_required
def week_view(request: HttpRequest) -> HttpResponse:
    current_school = get_current_school(request)
    if current_school is None:
        return redirect('home')

    selected_date = _parse_date(request.GET.get('date')) or timezone.localdate()
    week_start = selected_date - timedelta(days=selected_date.weekday())
    start_dt = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))
    end_dt = start_dt + timedelta(days=7)

    lessons = (
        Lesson.objects.filter(school=current_school, start_datetime__gte=start_dt, start_datetime__lt=end_dt)
        .select_related('group', 'student')
        .order_by('start_datetime')
    )

    days = []
    for i in range(7):
        d = week_start + timedelta(days=i)
        day_start = timezone.make_aware(datetime.combine(d, datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        days.append(
            {
                'date': d,
                'lessons': [l for l in lessons if day_start <= l.start_datetime < day_end],
            }
        )

    return render(
        request,
        'dashboard/week.html',
        {
            'week_start': week_start,
            'selected_date': selected_date,
            'days': days,
        },
    )


@login_required
def student_view(request: HttpRequest) -> HttpResponse:
    current_school = get_current_school(request)
    if current_school is None:
        return redirect('home')

    students = Student.objects.filter(school=current_school).order_by('last_name', 'first_name')

    student_id = request.GET.get('student_id')
    selected_student = None
    lessons = Lesson.objects.none()

    if student_id:
        selected_student = students.filter(id=student_id).first()

    if selected_student is not None:
        start_date = _parse_date(request.GET.get('start'))
        end_date = _parse_date(request.GET.get('end'))

        lessons = Lesson.objects.filter(school=current_school).select_related('group', 'student')

        lessons = lessons.filter(
            Q(student=selected_student) | Q(group__students=selected_student)
        ).distinct()

        if start_date:
            start_dt = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
            lessons = lessons.filter(start_datetime__gte=start_dt)
        if end_date:
            end_dt = timezone.make_aware(datetime.combine(end_date, datetime.min.time())) + timedelta(days=1)
            lessons = lessons.filter(start_datetime__lt=end_dt)

        lessons = lessons.order_by('-start_datetime')

    return render(
        request,
        'dashboard/student.html',
        {
            'students': students,
            'selected_student': selected_student,
            'lessons': lessons,
            'start': request.GET.get('start', ''),
            'end': request.GET.get('end', ''),
        },
    )
