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
        self.user = User.objects.create_user('user4', 'user1@test.com', 'pass')
        app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=self.user
            )

    def test_use_serializer_does_not_fail(self):
        response = self.client.get('/custom/use-serializer/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_use_serializer_post_does_not_fail(self):
        data = {"foo":"bar"}
        response = self.client.post('/custom/use-serializer/', json.dumps(data),
                content_type='application/json',
                )
        self.assertEqual(response.status_code, 200)

    def test_use_serializer_post_file_does_not_fail(self):
        fh, tempname = tempfile.mkstemp()
        with open(tempname, 'wb') as write_obj:
            write_obj.write(b"x")
        with open(tempname, 'rb') as read_obj:
            data = read_obj.read()
        data =  json.dumps({'picture' : base64.b64encode(data).decode("utf8")})
        response = self.client.post('/custom/use-serializer/', data,
                content_type='application/json',
                )
        self.assertEqual(response.status_code, 200)
        os.close(fh)
        os.remove(tempname)

    def test_use_serializer_delete_does_not_fail(self):
        response = self.client.delete('/custom/use-serializer/', format='json')
        self.assertEqual(response.status_code, 405)
