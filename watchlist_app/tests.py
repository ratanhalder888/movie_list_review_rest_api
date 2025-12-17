from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from watchlist_app.api import serializers
from watchlist_app import models


class StreamPlatformTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about='#1 Streaming Platform',
                                                           website='https://netflix.com')

    def test_streamplatform_create(self):
        data = {
            'name' : 'Netflix',
            'about' : '#1 Streaming Platform',
            'website' : 'https://netflix.com',
        }
        # streamplatform is a viewset that why it works when add "streamplatform-list"
        url = reverse('streamplatform-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        url = reverse("streamplatform-detail", args=(self.stream.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WatchListTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="example", password="Password@123")
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                           about='#1 Streaming Platform',
                                                           website='https://netflix.com')
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                         title="Example Movie",
                                                         storyline="Example Story",
                                                         active=True)
    def test_watchlist_create(self):
        data = {
            'platform' : self.stream,
            'title' : 'Example Movie',
            'storyline' : 'Example Story',
            'active' : True,
        }
        response = self.client.post(reverse("movie-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_list(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        url = reverse("movie-detail", args=(self.watchlist.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'Example Movie')
