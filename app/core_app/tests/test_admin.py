from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class TestAdmin(TestCase):

    def setUp(self):
        """
        Runs before every test in a class, creates test variables
        """
        # logged in admin
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(email="superuser@email.com",
                                                                    password="superpass123")
        self.client.force_login(self.admin_user)

        # exists regular user
        self.user = get_user_model().objects.create_user(email="regulaeuser@email.com",
                                                         password="regularpass123",
                                                         name="Basic user")

    def test_users_listed(self):
        """
        Tests that users are listed on user page
        """
        url = reverse('admin:core_app_user_changelist')  # format {{ app_label }}_{{ model_name }}_changelist
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_page_change(self):
        """
        Test that user edit page works
        """
        url = reverse('admin:core_app_user_change', args=[self.user.id])  # e.g., admin/core_app/user/1
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """
        Test that create user page works
        """
        url = reverse('admin:core_app_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
