from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from .models import School, SchoolMembership


SESSION_SCHOOL_ID_KEY = 'current_school_id'


def school_context(request: HttpRequest) -> dict[str, Any]:
    if not request.user.is_authenticated:
        return {
            'current_school': None,
            'school_memberships': [],
        }

    memberships = (
        SchoolMembership.objects.select_related('school')
        .filter(user=request.user, is_active=True)
        .order_by('school__name')
    )

    current_school = None
    current_school_id = request.session.get(SESSION_SCHOOL_ID_KEY)

    if current_school_id is not None:
        current_school = School.objects.filter(id=current_school_id).first()

    if current_school is None and memberships:
        current_school = memberships[0].school
        request.session[SESSION_SCHOOL_ID_KEY] = current_school.id

    return {
        'current_school': current_school,
        'school_memberships': memberships,
    }
