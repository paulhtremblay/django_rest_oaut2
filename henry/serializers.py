from rest_framework import serializers
from henry.models import DOB, NotManaged

class DobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOB
        fields = ('name', 'dob')

class NotManagedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotManaged
        fields = ('name', 'dob')
