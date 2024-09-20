
from rest_framework import status
from django.http import HttpResponse

from util.helpers import get_request
from util.response import response_error

def auth_required(func):

    def wrapper(*args, **kwargs):
        req = get_request(*args)

        if not req:
            return response_error(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                'something went wrong',
            )
        
        if not req.user or not req.user.is_authenticated:
            print('not authentication')
            return response_error(
                status.HTTP_401_UNAUTHORIZED,
                'User not logged in!'
            )
        

        return func(*args, **kwargs)
    
    return wrapper

    
