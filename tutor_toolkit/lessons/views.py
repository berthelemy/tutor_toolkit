from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

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

    def get_lesson(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'], school=self.current_school)

    def form_valid(self, form):
        lesson = self.get_lesson()
        form.instance.lesson = lesson
        return super().form_valid(form)

    def get_success_url(self):
        lesson = self.get_lesson()
        return reverse('lessons:detail', kwargs={'pk': lesson.pk})


class LessonObjectiveUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = LessonObjective
    form_class = LessonObjectiveForm
    template_name = 'lessons/objective_form.html'

    def get_queryset(self):
        return LessonObjective.objects.filter(lesson__school=self.current_school)

    def form_valid(self, form):
        self.lesson = form.instance.lesson
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonObjectiveDeleteView(LoginRequiredMixin, CurrentSchoolRequiredMixin, DeleteView):
    model = LessonObjective
    template_name = 'lessons/confirm_delete.html'

    def get_queryset(self):
        return LessonObjective.objects.filter(lesson__school=self.current_school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonResourceUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = LessonResource
    form_class = LessonResourceForm
    template_name = 'lessons/resource_form.html'

    def get_queryset(self):
        return LessonResource.objects.filter(lesson__school=self.current_school)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonResourceDeleteView(LoginRequiredMixin, CurrentSchoolRequiredMixin, DeleteView):
    model = LessonResource
    template_name = 'lessons/confirm_delete.html'

    def get_queryset(self):
        return LessonResource.objects.filter(lesson__school=self.current_school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class HomeworkTaskUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = HomeworkTask
    form_class = HomeworkTaskForm
    template_name = 'lessons/homework_form.html'

    def get_queryset(self):
        return HomeworkTask.objects.filter(lesson__school=self.current_school)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class HomeworkTaskDeleteView(LoginRequiredMixin, CurrentSchoolRequiredMixin, DeleteView):
    model = HomeworkTask
    template_name = 'lessons/confirm_delete.html'

    def get_queryset(self):
        return HomeworkTask.objects.filter(lesson__school=self.current_school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonNoteUpdateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, UpdateView):
    model = LessonNote
    form_class = LessonNoteForm
    template_name = 'lessons/note_form.html'

    def get_queryset(self):
        return LessonNote.objects.filter(lesson__school=self.current_school)

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonNoteDeleteView(LoginRequiredMixin, CurrentSchoolRequiredMixin, DeleteView):
    model = LessonNote
    template_name = 'lessons/confirm_delete.html'

    def get_queryset(self):
        return LessonNote.objects.filter(lesson__school=self.current_school)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cancel_url'] = reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})
        return context

    def get_success_url(self):
        return reverse('lessons:detail', kwargs={'pk': self.object.lesson_id})


class LessonResourceCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = LessonResource
    form_class = LessonResourceForm
    template_name = 'lessons/resource_form.html'

    def get_lesson(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'], school=self.current_school)

    def form_valid(self, form):
        lesson = self.get_lesson()
        form.instance.lesson = lesson
        return super().form_valid(form)

    def get_success_url(self):
        lesson = self.get_lesson()
        return reverse('lessons:detail', kwargs={'pk': lesson.pk})


class HomeworkTaskCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = HomeworkTask
    form_class = HomeworkTaskForm
    template_name = 'lessons/homework_form.html'

    def get_lesson(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'], school=self.current_school)

    def form_valid(self, form):
        lesson = self.get_lesson()
        form.instance.lesson = lesson
        return super().form_valid(form)

    def get_success_url(self):
        lesson = self.get_lesson()
        return reverse('lessons:detail', kwargs={'pk': lesson.pk})


class LessonNoteCreateView(LoginRequiredMixin, CurrentSchoolRequiredMixin, CreateView):
    model = LessonNote
    form_class = LessonNoteForm
    template_name = 'lessons/note_form.html'

    def get_lesson(self):
        return get_object_or_404(Lesson, pk=self.kwargs['lesson_id'], school=self.current_school)

    def form_valid(self, form):
        lesson = self.get_lesson()
        form.instance.lesson = lesson
        return super().form_valid(form)

    def get_success_url(self):
        lesson = self.get_lesson()
        return reverse('lessons:detail', kwargs={'pk': lesson.pk})
