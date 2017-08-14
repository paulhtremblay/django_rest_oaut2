from django.test import TestCase
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Permission, Group
import datetime

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
        access_token = AccessToken.objects.create(
            user=user,
            scope='read write',
            expires=datetime.datetime.now() +
            datetime.timedelta(seconds=300),
            token='secret-access-token-key',
            application=app
            )
