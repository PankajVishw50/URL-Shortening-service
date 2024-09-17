from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.utils.datastructures import MultiValueDictKeyError
from django.middleware.csrf import get_token

from util.response import response_error, required_fields_str
from util.shortcuts import User
from account.serializers import CustomUserSerializer

# Create your views here.

class CSRFView(APIView):
    
    def get(self, req):

        return Response({
            'csrf': get_token(req),
        }, status.HTTP_200_OK)

class LoginView(APIView):

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

        except (MultiValueDictKeyError, KeyError):
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                required_fields_str(['email', 'password'])
            )
        
        user = authenticate(email=email, password=password)
        if not user:        
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Invalid credentials',
            )
        
        login(request, user)     
        user_serialized = CustomUserSerializer(user)
 
        return Response({
            'data': user_serialized.data
        })
    
class SignUpView(APIView):

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']

        except KeyError:
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                required_fields_str(['email', 'password']),
            )

        if User.objects.filter(email=email).exists():
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Provided email (%s) already exists' % email, 
            )
        
        try:
            user = User.objects.create_user(email, password)
        except ValueError:
            return response_error(
                status.HTTP_400_BAD_REQUEST,
                'Invalid data',
            )

        user_serialized = CustomUserSerializer(user)

        return Response({
            'created': True if user.id else False, 
            'data': user_serialized.data,
        })