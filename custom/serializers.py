from rest_framework import serializers
from henry.models import DOB

class DobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOB
        fields = ('name', 'dob')

class TestSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
