from django.test import TestCase
from django.contrib.auth import get_user_model


class TestsModel(TestCase):

    def test_create_user_with_regular_email(self):
        """
        Test creating new user with email
        """
        email = 'reqularuser@email.com'
        password = 'regularpass123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_new_user_with_normalized_email(self):
        """
        Test creating user with normalized email (password is None by default)
        """
        email = "NormalizedEmail@EMAIl.COM"
        user = get_user_model().objects.create_user(email)

        username, domain = email.split("@")
        expected_email = '@'.join([username, domain.lower()])
        self.assertEqual(user.email, expected_email)

    def test_create_user_with_no_email(self):
        """
        Test creating user with no email returns error
        """
        email = None

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email)

    def test_create_super_user(self):
        """
        Test creating superuser
        """
        email = "superuser@email.com"
        password = "superpass123"
        user = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
