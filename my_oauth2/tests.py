import unittest
import requests
from django.http import HttpResponseForbidden

class TestGetToken(unittest.TestCase):

    def setUp(self):
        self.client_id = r'qgY3mEsFHkewnOeuQ399ssJSBMs1Ws28tsPRTxup'
        self.client_secret = r'1F0fMdut68XAI8rA0zmbHeGGkPNrRxvCauYNgzxIqRpl8SXxv8hNEsUvZ34ajclZixFxE0hMsuTLX3jD3xpONlLNsiyhhqL4jctmJ0wJM6nWg1wKd6SwE1x8HgypBIda'
        self.url = 'http://localhost:8000/o/token/'

    def test_user_with_read_group_can_get_read_token(self):
        data = {
                'grant_type':'password',
                'username': 'user2',
                'password':'bluebird',
                'scope':'read',
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)

    def test_user_with_no_read_group_cannot_get_read_token(self):
        data = {
                'grant_type':'password',
                'username': 'user1',
                'password':'bluebird',
                'scope':'read',
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertEqual(response.status_code, 403)

    def test_invalid_user_cannot_get_token(self):
        data = {
                'grant_type':'password',
                'username': 'user_nobody',
                'password':'bluebird',
                'scope':'read',
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertEqual(response.status_code, 403)

    def test_user_with_no_write_group_cannot_get_write_token(self):
        data = {
                'grant_type':'password',
                'username': 'user2',
                'password':'bluebird',
                'scope':'write',
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertEqual(response.status_code, 403)

    def test_user_with_no_write_group_cannot_get_write_token(self):
        data = {
                'grant_type':'password',
                'username': 'user2',
                'password':'bluebird',
                'scope':'write',
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertEqual(response.status_code, 403)

    def test_user_with_write_group_can_get_write_token(self):
        data = {
                'grant_type':'password',
                'username': 'user3',
                'password':'bluebird',
                'scope':'write',
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)

    def test_user_with_bad_password_cannot_get_read_token(self):
        data = {
                'grant_type':'password',
                'username': 'user2',
                'password':'badPass',
                'scope':'read',
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertEqual(response.status_code, 401)

    def test_refresh_token_return_refresh_token(self):
        data = {
                'grant_type':'password',
                'username': 'user4',
                'password':'bluebird',
                'scope':'write',
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        data = {
                'grant_type':'refresh_token',
                'refresh_token' : response.json()['refresh_token'],
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)
        self.assertTrue(response.json().get('refresh_token') != None)

    def test_user_with_write_group_cannot_get_refresh_token(self):
        data = {
                'grant_type':'password',
                'username': 'user3',
                'password':'bluebird',
                'scope':'write',
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.json().get('refresh_token') == None)

    def test_can_access_with_token(self):
        data = {
                'grant_type':'password',
                'username': 'user2',
                'password':'bluebird',
                'scope':'read',
                'expires_in': 3800,
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)
        headers = {'Authorization': 'bearer {access_token}'.format(access_token = response.json()['access_token'])}
        response = requests.get('http://localhost:8000/henry/', headers=headers)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)

    def test_refresh_token_can_access_resource(self):
        data = {
                'grant_type':'password',
                'username': 'user4',
                'password':'bluebird',
                'scope':'read',
                }
        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        data = {
                'grant_type':'refresh_token',
                'refresh_token' : response.json()['refresh_token'],
                }

        response = requests.post(self.url, auth=(self.client_id, self.client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)
        self.assertTrue(response.json().get('refresh_token') != None)
        headers = {'Authorization': 'bearer {access_token}'.format(access_token = response.json()['access_token'])}
        response = requests.get('http://localhost:8000/henry/', headers=headers)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)

if __name__ == '__main__':
    unittest.main()

