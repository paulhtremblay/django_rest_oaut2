from django.test import TestCase
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Permission, Group
import datetime
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import pytz


class AppTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user4', 'user1@test.com', 'pass')
        app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=self.user
        )
        self.client_id = app.client_id
        self.client_secret = app.client_secret
        tz = pytz.timezone('US/Pacific')
        pac_dt = tz.localize(datetime.datetime.now())
        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read',
            expires= pac_dt + datetime.timedelta(seconds = 300),
            token='secret-access-token-key',
            application=app
            )
        pac_dt2 = tz.localize(datetime.datetime(year = 2015, month = 1, day = 1))
        self.expired_access_token = AccessToken.objects.create(
            user=self.user,
            scope='read',
            expires= pac_dt2,
            token='secret-access-token-key2',
            application=app
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user, token = self.access_token)

    def test_henry_endpoint_does_not_fail(self):
        response = self.client.get('/henry/', format='json', HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, 200)

    def test_henry_endpoint_with_expired_token_fails(self):
        client = APIClient()
        client.force_authenticate(user=self.user, token = self.expired_access_token)
        response = client.get('/henry/', format='json', HTTP_AUTHORIZATION= self.expired_access_token)
        self.assertEqual(response.status_code, 403)
