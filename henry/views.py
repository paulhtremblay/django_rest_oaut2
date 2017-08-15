from henry.models import DOB
from henry.serializers import DobSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from henry.permissions import CustomPermissions
from henry.permissions import CustomPermissions3
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class DobList(generics.ListCreateAPIView):
    #permission_classes = (CustomPermissions,)
    permission_classes = [TokenHasScope]
    required_scopes = ['read']
    queryset = DOB.objects.all()
    serializer_class = DobSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class DobDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = DOB.objects.all()
    serializer_class = DobSerializer
    permission_classes = (CustomPermissions,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


