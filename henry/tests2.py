from django.test import TestCase
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Permission, Group
import datetime
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
import pytz


class AppTestCase(TestCase):

    def test_first(self):
        user = User.objects.create_user('user1', 'user1@test.com', 'pass')
        app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
            user=user
        )
        tz = pytz.timezone('US/Pacific')
        pac_dt = tz.localize(datetime.datetime.now())
        access_token = AccessToken.objects.create(
            user=user,
            scope='read',
            expires= pac_dt + datetime.timedelta(seconds = 300),
            token='secret-access-token-key',
            application=app
            )
        client = APIClient()
        client.force_authenticate(user=user, token = access_token)
        response=client.get('/henry/', format='json', HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.status_code, 200)
