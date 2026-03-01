from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import HomeworkTaskForm, LessonForm, LessonNoteForm, LessonObjectiveForm, LessonResourceForm
from .mixins import CurrentSchoolRequiredMixin
from .models import HomeworkTask, Lesson, LessonNote, LessonObjective, LessonResource


class LessonListView(LoginRequiredMixin, CurrentSchoolRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/lesson_list.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return (
            Lesson.objects.filter(school=self.current_school)
            .select_related('group', 'student')
            .order_by('-start_datetime')
        )


class LessonDetailView(LoginRequiredMixin, CurrentSchoolRequiredMixin, DetailView):
    model = Lesson
    template_name = 'lessons/lesson_detail.html'
    context_object_name = 'lesson'

    def get_queryset(self):
        return (
            Lesson.objects.filter(school=self.current_school)
            .select_related('group', 'student')
            .prefetch_related('objectives', 'resources', 'homework_tasks', 'notes')
        )


class LessonCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/lesson_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.current_school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.current_school
        form.instance.tutor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.pk})


class LessonUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = Lesson
    form_class = LessonForm
    template_name = 'lessons/lesson_form.html'

    def get_queryset(self):
        return Lesson.objects.filter(school=self.current_school)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['school'] = self.current_school
        return kwargs

    def form_valid(self, form):
        form.instance.school = self.current_school
        form.instance.tutor = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.pk})


class LessonObjectiveCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = LessonObjective
    form_class = LessonObjectiveForm
    template_name = 'lessons/objective_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=kwargs['lesson_id'], school=self.current_school)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.lesson.pk})


class LessonResourceCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = LessonResource
    form_class = LessonResourceForm
    template_name = 'lessons/resource_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=kwargs['lesson_id'], school=self.current_school)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.lesson.pk})


class HomeworkTaskCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = HomeworkTask
    form_class = HomeworkTaskForm
    template_name = 'lessons/homework_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=kwargs['lesson_id'], school=self.current_school)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.lesson.pk})


class LessonNoteCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = LessonNote
    form_class = LessonNoteForm
    template_name = 'lessons/note_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.lesson = get_object_or_404(Lesson, pk=kwargs['lesson_id'], school=self.current_school)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.lesson = self.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.lesson.pk})
