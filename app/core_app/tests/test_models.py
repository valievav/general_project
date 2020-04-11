from django.test import TestCase
from django.contrib.auth import get_user_model


class TestsModel(TestCase):

    def test_create_user_with_email(self):
        """Test creating new user with email """
        email = 'randomtest@email.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
