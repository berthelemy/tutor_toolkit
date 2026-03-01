from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import StudentForm, StudentGroupForm
from .mixins import CurrentSchoolRequiredMixin
from .models import Student, StudentGroup


class StudentListView(LoginRequiredMixin, CurrentSchoolRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(school=self.current_school).order_by('last_name', 'first_name')


class StudentCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        form.instance.school = self.current_school
        return super().form_valid(form)


class StudentUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def get_queryset(self):
        return Student.objects.filter(school=self.current_school)


class GroupListView(LoginRequiredMixin, CurrentSchoolRequiredMixin, ListView):
    model = StudentGroup
    template_name = 'students/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return StudentGroup.objects.filter(school=self.current_school).prefetch_related('students').order_by('name')


class GroupCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = StudentGroup
    form_class = StudentGroupForm
    template_name = 'students/group_form.html'
    success_url = reverse_lazy('students:groups')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.current_school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.current_school
        return super().form_valid(form)


class GroupUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = StudentGroup
    form_class = StudentGroupForm
    template_name = 'students/group_form.html'
    success_url = reverse_lazy('students:groups')

    def get_queryset(self):
        return StudentGroup.objects.filter(school=self.current_school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.current_school
        return kwargs
