import datetime
import pytz

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.http import HttpResponseForbidden
from django.test import TestCase
from rest_framework.test import APITestCase
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Permission, Group
import json
import tempfile
import base64
import os


class AppTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_use_serializer_does_not_fail(self):
        response = self.client.get('/custom/use-serializer/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_use_serializer_post_does_not_fail(self):
        data = {"foo":"bar"}
        response = self.client.post('/custom/use-serializer/', json.dumps(data),
                content_type='application/json',
                )
        self.assertEqual(response.status_code, 200)

    def test_use_serializer_delete_does_not_fail(self):
        response = self.client.delete('/custom/use-serializer/', format='json')
        self.assertEqual(response.status_code, 405)
