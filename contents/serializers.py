from rest_framework import serializers
from . import models

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DOB
        fields = ('name', 'dob')

