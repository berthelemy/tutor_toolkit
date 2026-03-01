from __future__ import annotations

from typing import Optional

from django.http import HttpRequest

from .context_processors import SESSION_SCHOOL_ID_KEY
from .models import School, SchoolMembership


def get_current_school(request: HttpRequest) -> Optional[School]:
    if not request.user.is_authenticated:
        return None

    school_id = request.session.get(SESSION_SCHOOL_ID_KEY)
    if school_id is None:
        membership = (
            SchoolMembership.objects.select_related('school')
            .filter(user=request.user, is_active=True)
            .order_by('school__name')
            .first()
        )
        if membership is None:
            return None
        request.session[SESSION_SCHOOL_ID_KEY] = membership.school_id
        return membership.school

    membership_exists = SchoolMembership.objects.filter(
        user=request.user,
        school_id=school_id,
        is_active=True,
    ).exists()
    if not membership_exists:
        request.session.pop(SESSION_SCHOOL_ID_KEY, None)
        return None

    return School.objects.filter(id=school_id).first()
