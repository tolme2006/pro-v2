from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class DashboardViewTests(TestCase):
    def test_dashboard_renders_for_authenticated_user(self):
        user = get_user_model().objects.create_user(username='admin', password='secret1234')
        self.client.force_login(user)
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_dashboard_redirects_anonymous_user_to_login(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 302)
