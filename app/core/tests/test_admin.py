from django.test import Client, TestCase
from django.urls import reverse

from utils.help_test_utils import create_superuser, create_user


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.admin_user = create_superuser()
        self.client.force_login(self.admin_user)

        self.user = create_user()

    def test_users_list_page(self):
        url = reverse('admin:core_user_changelist')
        r = self.client.get(url)

        self.assertContains(r, self.user.name)
        self.assertContains(r, self.user.email)

    def test_user_detail_page(self):
        url = reverse('admin:core_user_change', args=[self.user.id])
        r = self.client.get(url)

        self.assertEqual(r.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        r = self.client.get(url)

        self.assertEqual(r.status_code, 200)
