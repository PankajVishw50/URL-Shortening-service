from rest_framework.response import Response
from rest_framework import status

def response_error(
        status_code=500, 
        message='Something Went wrong',
        data={}
):
    return Response(
        {
            'error': {
                'status_code': status_code,
                'message': message,
                **data,
            }
        },
        status_code
    )

def required_fields_str(fields: list, prefix: str = 'Required fields'):
    return '%s - %s' % (prefix, ', '.join(fields))