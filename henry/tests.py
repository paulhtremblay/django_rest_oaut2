from django.test import TestCase
from henry.models import DOB
import datetime
#from rest_framework.test import APIRequestFactory
#from rest_framework.test import RequestsClient
#from requests.auth import HTTPBasicAuth
from rest_framework.test import APIClient
import os
from django.contrib.auth.models import User, Permission, Group
from django.test import Client
from rest_framework.test import force_authenticate
#from django.test.client import Client



class DobTestCase(TestCase):
    def setUp(self):
        DOB.objects.create(name='henry2', dob = datetime.datetime(2017, 1, 1))
        self.user1 = User.objects.create_user('user1', 'user1@test.com', 'pass')
        self.user1.save()
        self.group = Group(name='reader')
        self.group.save()
        self.user1.groups.add(self.group)
        self.user1.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_b(self):
        response = self.client.get('/henry/')
        #self.assertEqual(response.status_code, 200)

    def _test_get_token(self):
        url = 'http://localhost:8000/o/token/'
        client_id = r'qgY3mEsFHkewnOeuQ399ssJSBMs1Ws28tsPRTxup'
        client_secret = r'1F0fMdut68XAI8rA0zmbHeGGkPNrRxvCauYNgzxIqRpl8SXxv8hNEsUvZ34ajclZixFxE0hMsuTLX3jD3xpONlLNsiyhhqL4jctmJ0wJM6nWg1wKd6SwE1x8HgypBIda'
        data = {
        'grant_type':'password',
        'username': 'karim',
        'password':'Datos_101',
        'scope':'read'
        }
        response = requests.post(url, auth=(client_id, client_secret), data = data)
        self.assertTrue(response.status_code >= 200 and response.status_code < 300)

    def _test_get_response_with_token(self):
        #t = User.objects.get(username = 'karim')
        #print('t is {t}'.format(t = t))
        #print(t.groups.filter(name = 'reader').exists())
        url = 'http://localhost:8000/o/token/'
        client_id = r'qgY3mEsFHkewnOeuQ399ssJSBMs1Ws28tsPRTxup'
        client_secret = r'1F0fMdut68XAI8rA0zmbHeGGkPNrRxvCauYNgzxIqRpl8SXxv8hNEsUvZ34ajclZixFxE0hMsuTLX3jD3xpONlLNsiyhhqL4jctmJ0wJM6nWg1wKd6SwE1x8HgypBIda'
        data = {
        'grant_type':'password',
        'username': 'karim',
        'password':'Datos_101',
        'scope':'read'
        }

        response = requests.post(url, auth=(client_id, client_secret), data = data)
        access_token = response.json()['access_token']
        headers = {'Authorization': 'bearer {access_token}'.format(access_token = access_token)}
        print(headers)
        response = requests.get('http://localhost:8000/henry/', headers=headers)
        print(response.status_code)

    def _test_get_token2(self):
        client_id = r'qgY3mEsFHkewnOeuQ399ssJSBMs1Ws28tsPRTxup'
        client_secret = r'1F0fMdut68XAI8rA0zmbHeGGkPNrRxvCauYNgzxIqRpl8SXxv8hNEsUvZ34ajclZixFxE0hMsuTLX3jD3xpONlLNsiyhhqL4jctmJ0wJM6nWg1wKd6SwE1x8HgypBIda'
        data = {
        'grant_type':'password',
        'username': 'user1',
        'password':'pass',
        'scope':'read'
        }
        res = self.client.post('/o/token/', auth=(client_id, client_secret), grant_type = 'password', 
                username = 'user1', password = 'pass', scope = 'read', client_id = client_id, 
                client_secret = client_secret)
        print(res.json())
        print(res.reason_phrase)
        return
        view = MyTokenView.as_view()
        factory = APIRequestFactory()
        request = factory.post('/o/token/', auth=(client_id, client_secret), data = data)
        print(dir(request))
        force_authenticate(request, user=user)
        response = view(request)
        print(response)
        return

    def _test_create_superuser(self):
        password = 'mypassword'

        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', password)

        c = APIClient()

        # You'll need to log him in before you can send requests through the client
        #c.login(username=my_admin.username, password=password)
        res = c.post('/o/applications/register/', data = {}, grant_type = 'password',
                username = 'user1', password = 'pass', scope = 'read')
        print(res)
