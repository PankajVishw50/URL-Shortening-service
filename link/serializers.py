from rest_framework import serializers

from .models import Url, Visit

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url 
        fields = [
            'pk', 'url', 'unique_identifier',
            'visits', 'allowed_visits', 
            'expiration_datetime', 'disabled', 'user',
        ]

        read_only_fields = [
            'visits', 'disabled',
        ]

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = [
            'pk', 'visit_datetime', 'ip_address',
            'user_agent', 'referrer', 'url',
        ]
