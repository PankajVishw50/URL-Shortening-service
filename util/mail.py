from django.core.mail import send_mail as django_send_mail
from django.conf import settings

def send_mail(
        subject: str, 
        message: str,
        from_email: str|None,
        recipient_list: list,
        fail_silently=False,
        html_message=None,
        ignore_debug=False,
):
    print('Recieved request to send mail to %s' % recipient_list)
    recipient_list = (
        recipient_list
        if not settings.DEBUG or ignore_debug
        else settings.EMAIL_DEBUG_RECEIVERS
    )


    mail = django_send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        html_message=html_message,
    )
    print('Mail sent')
    return mail

