import json

from  . import models
from  . import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseForbidden
from django.http import HttpResponse

class CreateSomeData:

    def make_data(self):
        self.id = 1
        self.title = 'Title'

class UseSerializer(generics.GenericAPIView):
    permission_classes = []
    serializer_class = serializers.TestSerializer

    #method has to be overwritten
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        return Response(json.dumps({"status":"success"}))

    #explict forbid, though you could delete this method
    def delete(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def get(self, request, *args, **kwargs):
        o = CreateSomeData()
        o.make_data()
        serializer = self.get_serializer([o], many=True)
        return Response(serializer.data)
