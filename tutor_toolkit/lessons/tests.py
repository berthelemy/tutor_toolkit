from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from schools.context_processors import SESSION_SCHOOL_ID_KEY
from schools.models import School, SchoolMembership
from students.models import Student

from .models import Lesson

# Create your tests here.


class LessonModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tutor', password='password123')
        self.school = School.objects.create(name='School 1')
        self.student = Student.objects.create(school=self.school, first_name='Alice', last_name='A')

    def test_lesson_requires_exactly_one_target(self):
        lesson = Lesson(
            school=self.school,
            tutor=self.user,
            start_datetime=timezone.now(),
            duration_minutes=60,
            group=None,
            student=None,
        )

        with self.assertRaises(ValidationError):
            lesson.full_clean()

    def test_lesson_duration_must_be_positive(self):
        lesson = Lesson(
            school=self.school,
            tutor=self.user,
            start_datetime=timezone.now(),
            duration_minutes=0,
            student=self.student,
        )

        with self.assertRaises(ValidationError):
            lesson.full_clean()


class LessonViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tutor', password='password123')

        self.school_1 = School.objects.create(name='School 1')
        self.school_2 = School.objects.create(name='School 2')

        SchoolMembership.objects.create(user=self.user, school=self.school_1, role=SchoolMembership.ROLE_TUTOR)

        self.student_1 = Student.objects.create(school=self.school_1, first_name='Alice', last_name='A')
        self.student_2 = Student.objects.create(school=self.school_2, first_name='Bob', last_name='B')

        self.lesson_school_1 = Lesson.objects.create(
            school=self.school_1,
            tutor=self.user,
            start_datetime=timezone.now(),
            duration_minutes=60,
            student=self.student_1,
        )
        self.lesson_school_2 = Lesson.objects.create(
            school=self.school_2,
            tutor=self.user,
            start_datetime=timezone.now(),
            duration_minutes=60,
            student=self.student_2,
        )

    def _login_and_set_school(self, school: School) -> None:
        self.client.login(username='tutor', password='password123')
        session = self.client.session
        session[SESSION_SCHOOL_ID_KEY] = school.id
        session.save()

    def test_lesson_list_requires_login(self):
        response = self.client.get(reverse('lessons:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_lesson_detail_other_school_returns_404(self):
        self._login_and_set_school(self.school_1)

        response = self.client.get(reverse('lessons:detail', kwargs={'pk': self.lesson_school_2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_lesson_edit_other_school_returns_404(self):
        self._login_and_set_school(self.school_1)

        response = self.client.get(reverse('lessons:edit', kwargs={'pk': self.lesson_school_2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_lesson_list_is_scoped_to_current_school(self):
        self._login_and_set_school(self.school_1)

        response = self.client.get(reverse('lessons:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertNotContains(response, 'Bob')
