from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from schools.models import School, SchoolMembership

# Create your tests here.


class I18nSmokeTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tutor', password='password123')
        self.school = School.objects.create(name='School 1')
        SchoolMembership.objects.create(user=self.user, school=self.school, role=SchoolMembership.ROLE_TUTOR)

    def test_set_language_to_french_translates_nav(self):
        self.client.login(username='tutor', password='password123')

        response = self.client.post(
            reverse('set_language'),
            data={'language': 'fr', 'next': reverse('home')},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Accueil')
