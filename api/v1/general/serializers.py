from rest_framework import serializers
from general.models import *

    
class ChiefProfileSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ListCountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Countries
        fields=(
            'id',
            'name',
            'country_code',
            'flag',
            'web_code',
            'phone_code',
            'is_active',
            'phone_number_length',
        )