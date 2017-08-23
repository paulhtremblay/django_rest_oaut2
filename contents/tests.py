import os
import datetime
import pytz
import json
import tempfile
import base64

from rest_framework.test import APIClient
from rest_framework.test import APITestCase



class AppTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_base64_does_not_fail(self):
        fh, tempname = tempfile.mkstemp()
        with open(tempname, 'wb') as write_obj:
            write_obj.write(b"x")
        with open(tempname, 'rb') as read_obj:
            data = read_obj.read()
        data =  json.dumps({'picture' : base64.b64encode(data).decode("utf8")})
        response = self.client.post('/contents/base-64/', data,
                content_type='application/json',
                )
        os.close(fh)
        os.remove(tempname)
        self.assertEqual(response.status_code, 200)

    def test_x_www_form_urlencoded_does_not_fail(self):
        data = 'field1=value1'
        content_type = 'application/x-www-form-urlencoded'
        response = self.client.post('/contents/base-64/', data,
                content_type=content_type,
                )
        self.assertEqual(response.status_code, 200)

    def test_multipart_form_data_does_not_fail(self):
        fh, tempname = tempfile.mkstemp()
        with open(tempname, 'wb') as write_obj:
            write_obj.write(b"x")
        read_obj = open(tempname, 'rb')
        data = {'title': "title", 'file':read_obj}
        content_type = 'multipart/form-data'
        response = self.client.post('/contents/multipart/', data,
            format = 'multipart'
                )
        read_obj.close()
        os.close(fh)
        os.remove(tempname)
        self.assertEqual(response.status_code, 200)

    def test_x_www_form_urlencoded_fails(self):
        data = {'foo':'boo'}
        content_type = 'application/json'
        response = self.client.post('/contents/multipart/', data,
                content_type=content_type,
                )
        self.assertEqual(response.status_code, 415)
