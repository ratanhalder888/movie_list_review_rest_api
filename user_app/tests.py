# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


# Create your tests here.
class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        # url = reverse('register')
        response =self.client.post(reverse('register'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example",password="NewPassword@123")

    def test_login(self):
        data = {
            "username": "example",
            "password": "NewPassword@123",
        }
        response = self.client.post(reverse('login'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_logout(self):
        self.token = Token.objects.get(user__username="example")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)