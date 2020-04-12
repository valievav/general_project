from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """
    Helper function to create user
    """
    return get_user_model().objects.create_user(**params)


class TestPublicUserApi(TestCase):
    """
    Tests the user API public (when user is not logged in)
    """
    
    def setUp(self):
        """
        Runs before every test in a class, creates test variables
        """
        self.client = APIClient()
        self.payload = {
            'email': 'valid@email.com',
            'password': 'validpass123',
            'name': 'Valid User',
        }
        
    def create_valid_user(self):
        """
        Test creating user with valid payload is successful
        """
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)  # check that pass is not returned in response

    def test_user_exists(self):
        """
        Test creating user that already exists fails
        """
        create_user(**self.payload)
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Tests that password is more > 5 char
        """
        payload_short_pass = {
            'email': 'valid@email.com',
            'password': 'no',
            'name': 'User name',
        }
        response = self.client.post(CREATE_USER_URL, payload_short_pass)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload_short_pass['email']).exists()
        self.assertFalse(user_exists)  # check that user was not created
