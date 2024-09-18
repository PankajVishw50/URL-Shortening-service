from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.conf import settings


from .serializers import UrlSerializer
from .models import Url, Visit
from util.response import response_error


# Create your views here.
class UrlsView(APIView):

    def get(self, request):
        return Response('not implemented')
    
    
    def post(self, request):

        # Get random string which is not in database
        unique_identifier = None 

        for x in range(10):
            _ui = get_random_string(settings.URL_UNIQUE_IDENTIFIERS_LENGTH)

            if not Url.objects.filter(unique_identifier=_ui).exists():
                unique_identifier = _ui 
                break 
        
        if not unique_identifier:
            return response_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        url_serialized = UrlSerializer(data={
            **request.data,
            'user': request.user.pk,
            'unique_identifier': unique_identifier,
        })

        if not url_serialized.is_valid():
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Invalid input data',
                {'errors': url_serialized.errors},
            )
        
        url_serialized.save()
        return Response({
            'created': True if url_serialized.instance.pk else False,
            'data': url_serialized.data,
        })