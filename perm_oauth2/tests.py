from django.test import TestCase, TransactionTestCase
from oauth2_provider.models import Application
from oauth2_provider.models import AccessToken
from django.contrib.auth.models import User, Permission, Group
import datetime
from rest_framework.test import APIClient
import pytz
from django.db import connection
from django.contrib.auth.models import Group

class AppTestCase(TestCase):

    def setUp(self):
        app = Application.objects.create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
            redirect_uris='https://www.none.com/oauth2/callback',
            name='dummy',
        )
        self.client_id = app.client_id
        self.client_secret = app.client_secret

    def test_user_with_read_group_can_get_read_token(self):
        Group.objects.update_or_create(name='reader')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group = Group.objects.get(name='reader')
        user.groups = [users_group]
        data = 'scope=read&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 200)

    def test_user_with_no_read_group_cannot_get_read_token(self):
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        data = 'scope=read&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code,  403)


    def test_invalid_user_cannot_get_token(self):
        data = 'scope=read&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code,  403)

    def test_user_with_no_write_group_cannot_get_write_token(self):
        Group.objects.update_or_create(name='reader')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group = Group.objects.get(name='reader')
        user.groups = [users_group]
        data = 'scope=write&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 403)

    def test_user_with_write_group_can_get_write_token(self):
        Group.objects.update_or_create(name='writer')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group = Group.objects.get(name='writer')
        user.groups = [users_group]
        data = 'scope=write&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 200)

    def test_user_with_bad_password_cannot_get_read_token(self):
        Group.objects.update_or_create(name='reader')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group = Group.objects.get(name='reader')
        user.groups = [users_group]
        data = 'scope=read&password=bogus&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_return_refresh_token(self):
        Group.objects.create(name='refresh')
        Group.objects.create(name='reader')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group_refresh = Group.objects.get(name='refresh')
        users_group_read = Group.objects.get(name='reader')
        user.groups = [users_group_refresh, users_group_read]
        data = 'scope=read&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('refresh_token') != None)


    def test_user_with_write_group_cannot_get_refresh_token(self):
        Group.objects.update_or_create(name='writer')
        user = User.objects.create_user('user', 'user1@test.com', 'pass')
        users_group = Group.objects.get(name='writer')
        user.groups = [users_group]
        data = 'scope=write&password=pass&username=user&grant_type=password&client_id={id}&client_secret={sec}'.format(
              id = self.client_id, sec = self.client_secret )
        client = APIClient()
        response = client.post('/o/token/',
                data,
                content_type = 'application/x-www-form-urlencoded'
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json().get('refresh_token') == None)
