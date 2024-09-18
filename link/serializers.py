from rest_framework import serializers

from .models import Url, Visit

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url 
        fields = [
            'url', 'unique_identifier',
            'visits', 'allowed_visits', 
            'expiration_datetime', 'user',
        ]

        read_only_fields = [
            'visits'
        ]