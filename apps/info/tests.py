from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.info.models import Tblinfo


def _sample_data(**overrides):
    data = {
        'title': 'Sample Title',
        'description': 'Sample description.',
        'status': 'active',
    }
    data.update(overrides)
    return data


class TblinfoModelTests(TestCase):
    def test_str_returns_title(self):
        info = Tblinfo.objects.create(**_sample_data())
        self.assertEqual(str(info), 'Sample Title')


class InfoPageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='staff', password='secret1234')
        self.client.force_login(self.user)

    def test_info_list_page_renders(self):
        response = self.client.get(reverse('info:info_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info/list.html')

    def test_info_list_page_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('info:info_list'))

        self.assertEqual(response.status_code, 302)


class InfoCrudAjaxTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='staff', password='secret1234')
        self.client.force_login(self.user)
        self.info = Tblinfo.objects.create(**_sample_data())

    def test_create(self):
        response = self.client.post(reverse('info:info_save_ajax'), {
            'title': 'New Record',
            'description': 'Created via AJAX.',
            'status': 'inactive',
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Tblinfo.objects.filter(title='New Record', status='inactive').exists())

    def test_update(self):
        response = self.client.post(reverse('info:info_save_ajax'), {
            'id': self.info.id,
            'title': 'Updated Title',
            'description': 'Updated description.',
            'status': 'inactive',
        })

        self.assertEqual(response.status_code, 200)
        self.info.refresh_from_db()
        self.assertEqual(self.info.title, 'Updated Title')
        self.assertEqual(self.info.status, 'inactive')

    def test_create_requires_title(self):
        response = self.client.post(reverse('info:info_save_ajax'), {
            'title': '',
            'description': 'No title.',
            'status': 'active',
        })

        self.assertEqual(response.status_code, 400)

    def test_get_single(self):
        response = self.client.get(reverse('info:info_get_ajax', args=[self.info.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Sample Title')

    def test_delete(self):
        response = self.client.post(reverse('info:info_delete_ajax', args=[self.info.id]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tblinfo.objects.filter(pk=self.info.id).exists())
