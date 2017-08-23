import json


from  . import models
from  . import serializers

from django.http import HttpResponseForbidden
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class Content(generics.GenericAPIView):
    permission_classes = []
    serializer_class = serializers.ContentsSerializer

    #method has to be overwritten
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        return Response(json.dumps({"status":"success"}))

    #explict forbid, though you could delete this method
    def delete(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def get(self, request, *args, **kwargs):
        return Response(json.dumps({"status":"success"}))

class ContentMultiPart(generics.GenericAPIView):
    permission_classes = []
    parser_classes = (MultiPartParser, FormParser)

    #method has to be overwritten
    def get_queryset(self):
        pass

    def post(self, request, *args, **kwargs):
        print('data is {data}'.format(data = request.data))
        return Response(json.dumps({"status":"success"}))

    #explict forbid, though you could delete this method
    def delete(self, request, *args, **kwargs):
        return HttpResponse(status=405)

    def get(self, request, *args, **kwargs):
        return Response(json.dumps({"status":"success"}))

    def perform_create(self,serializer,format=None):
        pass
