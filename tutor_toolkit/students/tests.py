from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from schools.context_processors import SESSION_SCHOOL_ID_KEY
from schools.models import School, SchoolMembership

from .models import Student

# Create your tests here.


class StudentViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tutor', password='password123')

        self.school_1 = School.objects.create(name='School 1')
        self.school_2 = School.objects.create(name='School 2')

        SchoolMembership.objects.create(user=self.user, school=self.school_1, role=SchoolMembership.ROLE_TUTOR)

        self.student_school_1 = Student.objects.create(school=self.school_1, first_name='Alice', last_name='A')
        self.student_school_2 = Student.objects.create(school=self.school_2, first_name='Bob', last_name='B')

    def _login_and_set_school(self, school: School) -> None:
        self.client.login(username='tutor', password='password123')
        session = self.client.session
        session[SESSION_SCHOOL_ID_KEY] = school.id
        session.save()

    def test_student_list_requires_login(self):
        response = self.client.get(reverse('students:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_student_list_redirects_to_home_if_no_school_membership(self):
        User = get_user_model()
        user_no_membership = User.objects.create_user(username='nomember', password='password123')
        self.client.login(username='nomember', password='password123')

        response = self.client.get(reverse('students:list'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('home'))

    def test_student_list_is_scoped_to_current_school(self):
        self._login_and_set_school(self.school_1)

        response = self.client.get(reverse('students:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertNotContains(response, 'Bob')

    def test_student_edit_other_school_returns_404(self):
        self._login_and_set_school(self.school_1)

        response = self.client.get(reverse('students:edit', kwargs={'pk': self.student_school_2.pk}))
        self.assertEqual(response.status_code, 404)
