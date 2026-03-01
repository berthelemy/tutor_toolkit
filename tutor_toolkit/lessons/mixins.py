from __future__ import annotations

from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from schools.utils import get_current_school


class CurrentSchoolRequiredMixin:
    current_school = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.current_school = get_current_school(request)
        if self.current_school is None:
            messages.error(request, 'Please select a school.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
