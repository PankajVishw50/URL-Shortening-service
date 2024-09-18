from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.crypto import get_random_string
from django.conf import settings
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import datetime, pytz


from .serializers import UrlSerializer, VisitSerializer
from .models import Url, Visit
from util.response import response_error
from util.helpers import page_range

# Create your views here.
class UrlsView(APIView):

    def get(self, request):

        try:
            req_page = int(self.request.query_params['page']) if self.request.query_params.get('page') else None
            req_size = int(self.request.query_params['size']) if self.request.query_params.get('size') else None 

            if (req_page and req_page <= 0) or (req_size and (req_size <= 0 or req_size > 50)):
                raise Exception('invalid data')
        except:
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Invalid data'
            )


        page = req_page or 1
        size = req_size or 10

        [start, end] = page_range(page, size)
        all_urls = Url.objects.filter(user=request.user).order_by('-id')
        urls = all_urls[start:end]

        urls_serialized = UrlSerializer(instance=urls, many=True)

        return Response(
            {
                'next': all_urls.count() > urls.count(),
                'total': all_urls.count(),
                'page_info': {
                    'page': page,
                    'size': size,
                    'fetched_rows': urls.count(),
                },
                'data': urls_serialized.data,
            }
        )
    
    
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
    

class UrlView(APIView):

    def get(self, request, pk):

        try:
            url = Url.objects.get(pk=pk)

        except ObjectDoesNotExist:
            return response_error(
                status.HTTP_404_NOT_FOUND,
                'No url with provided id',
            )
        
        url_serialized = UrlSerializer(url)
        return Response({
            'data': url_serialized.data,
        })
    
    def patch(self, request, pk):

        try:
            url = Url.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return response_error(
                status.HTTP_404_NOT_FOUND,
                'No url with provided id',
            )
        
        url_serialized = UrlSerializer(url, data=request.data, partial=True)
        
        if not url_serialized.is_valid():
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Invalid data',
            )
        
        url_serialized.save()
        return Response({
            'updated': True,
            'data': url_serialized.data,
        })
    
class DisableUrlView(APIView):

    def post(self, request, pk):
        try:
            url = Url.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return response_error(
                status.HTTP_404_NOT_FOUND,
                'No url with provided id',
            )
        
        url.disabled = True 
        url.save()
        url_serialized = UrlSerializer(url)
        return Response({
            'disabled': url.disabled,
            'data': url_serialized.data,
        })

class EnableUrlView(APIView):

    def post(self, request, pk):
        try:
            url = Url.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return response_error(
                status.HTTP_404_NOT_FOUND,
                'No url with provided id',
            )
        
        url.disabled = False 
        url.save()
        url_serialized = UrlSerializer(url)
        return Response({
            'enabled': not url.disabled,
            'data': url_serialized.data,
        })


class RedirectView(APIView):

    def get(self, request, unique_identifier):

        # Get the url which was there 
        try:
            url = Url.objects.get(unique_identifier=unique_identifier)

        except ObjectDoesNotExist:
            return response_error(
                status.HTTP_404_NOT_FOUND,
                'Invalid url',
            )
        
        # Check if url is expired
        now = datetime.datetime.now(pytz.utc)
        if url.expiration_datetime and url.expiration_datetime < now:
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Link expired'
            )
        
        if url.disabled:
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Link is disabled',
            )
        
        # check if visit are available
        if isinstance(url.allowed_visits, int):
            if url.allowed_visits < 1:
                return response_error(
                    status.HTTP_400_BAD_REQUEST,
                    'Restricted',
                )
            
            url.allowed_visits -= 1

        # import ipdb;ipdb.set_trace();
        url.visits += 1
        url.save()

        # Save visitors info
        environ = request.environ

        ip_address = None
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        visitor_data = {
            'user_agent': environ.get('HTTP_USER_AGENT', 'unknown'),
            'ip_address': ip_address,
            'referrer': environ.get('HTTP_REFERER', 'unknown'),
            'url': url.pk,
        }

        visitor_serialized = VisitSerializer(data=visitor_data)
        if visitor_serialized.is_valid():
            visitor_serialized.save()


        return redirect(url.url)