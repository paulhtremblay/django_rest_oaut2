from rest_framework import serializers
class DobSerializer(serializers.ModelSerializer):
    class Meta:
        model = DOB
        fields = ('name', 'dob')
