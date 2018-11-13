from rest_framework import serializers
from restapi.models import *

class contentSerializer(serializers.ModelSerializer):
    class Meta:
        model = content
        fields = '__all__'