from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from .context_processors import SESSION_SCHOOL_ID_KEY
from .models import SchoolMembership


@login_required
@require_POST
def switch_school(request: HttpRequest) -> HttpResponse:
    next_url = request.POST.get('next') or '/'
    school_id = request.POST.get('school_id')

    if not school_id:
        messages.error(request, _('Please select a school.'))
        return redirect(next_url)

    membership_exists = SchoolMembership.objects.filter(
        user=request.user,
        school_id=school_id,
        is_active=True,
    ).exists()

    if not membership_exists:
        messages.error(request, _('You do not have access to that school.'))
        return redirect(next_url)

    request.session[SESSION_SCHOOL_ID_KEY] = int(school_id)
    messages.success(request, _('School switched.'))
    return redirect(next_url)
