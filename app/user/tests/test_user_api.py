from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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
        Prepares variables for each test
        """
        self.client = APIClient()
        self.payload = {
            'email': 'valid@email.com',
            'password': 'validpass123',
            'name': 'Valid User',
        }

        self.payload_invalid_pass = {
            'email': 'valid@email.com',
            'password': 'no',
            'name': 'User name',
        }

        self.payload_empty_pass = {
            'email': 'valid@email.com',
            'password': '',
            'name': 'User name',
        }

    def create_valid_user(self):
        """
        Tests creating user with valid payload is successful
        """
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)  # check that pass is not returned in response

    def test_user_exists(self):
        """
        Tests creating user that already exists fails
        """
        create_user(**self.payload)
        response = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Tests that password is more > 5 char
        """
        response = self.client.post(CREATE_USER_URL, self.payload_invalid_pass)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=self.payload_invalid_pass['email']).exists()
        self.assertFalse(user_exists)  # check that user was not created

    def test_create_token_for_user(self):
        """
        Tests that a token is created for user
        """
        create_user(**self.payload)
        response = self.client.post(TOKEN_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credentials(self):
        """
        Tests that token is not created when invalid credentials are given
        """
        create_user(**self.payload)
        response = self.client.post(TOKEN_URL, self.payload_invalid_pass)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Tests that token is not created if user doesn't exist
        """
        response = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Tests that token is not created when email/password is missing
        """
        response = self.client.post(TOKEN_URL, self.payload_empty_pass)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_unauthorized(self):
        """
        Tests that authentication is required
        """
        request = self.client.get(ME_URL)

        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)


class TestPrivateUserAPI(TestCase):
    """
    Tests API requests that require authentication
    """

    def setUp(self):
        """
        Prepares variables for each test
        """
        self.user = create_user(email='valid@email.com',
                                password='validpass123',
                                name='Valid User')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Tests retrieving profile for logged in user
        """
        response = self.client.get(ME_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'name': self.user.name,
                                         'email': self.user.email})

    def test_post_me_not_allowed(self):
        """
        Tests that POST is not allowed for logged in user
        """
        response = self.client.post(ME_URL, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_me_successful(self):
        """
        Tests that UPDATE works for me URL
        """
        payload = {'name': 'New ME',
                   'password': 'newpass123'}
        response = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
