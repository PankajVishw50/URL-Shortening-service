import re
from django.http import HttpRequest
from rest_framework.request import Request

def derive_name_from_email(email):
    name_part = email.split('@')[0]
    pattern = r'[@\-.,#]'
    
    parts = re.split(pattern, name_part)

    name = ' '.join(word.capitalize() for word in parts[:2])    
    
    return name

def get_request(*args):
    """Used by decorators. some decorators required
    access to request object and those request object are passed
    as positional args at index 0 if view is functional otherwise 
    at index 1 if view is class based and also while using DRF 
    requests object differs from django's default,
    as you can see it can be annoying to find the `Request` Object 
    and it would also not follow DRY standard.
    this function returns the req object from args. 
    
    """

    for arg in args:
        if type(arg) == HttpRequest or type(arg) == Request or issubclass(arg.__class__, HttpRequest):
            return arg

    return None

