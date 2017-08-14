from rest_framework import serializers
from henry.models import DOB
class DobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOB
        fields = ('name', 'dob')
