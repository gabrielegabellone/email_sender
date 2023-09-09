from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from subscribers.models import Subscriber


@swagger_auto_schema(
    method='POST',
    operation_id='send_emails_to_all',
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'subject': openapi.Schema(type=openapi.TYPE_STRING, description='the subject of the email', default=''),
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='the message to send', default=''),
    }),
    responses={
        '200': openapi.Response(
            description='Success',
            examples={
                'application/json': {
                    'msg': 'Emails successfully sent'
                },
            }
        ),
        '500': openapi.Response(
            description='Internal Server Error',
            examples={
                'application/json': {
                    'msg': 'Error sending email'
                },
            }
        )
    })
@api_view(['POST'])
def send_email_to_all_subscribers(request):
    """Allows the sending of emails to all subscribers."""
    data = request.data
    subscribers = Subscriber.objects.all()
    recipient_list = [subscriber.email for subscriber in subscribers]
    subject = data.get('subject', '')
    email_from = settings.EMAIL_HOST_USER
    message = data.get('message', '')
    email_sent = send_mail(subject, message, email_from, recipient_list)
    if email_sent:
        return Response({'msg': 'Emails successfully sent'}, status=200)
    return Response({'msg': 'Error sending email'}, status=500)


@swagger_auto_schema(
    method='POST',
    operation_id='send_emails_by_subscribers_ids',
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'recipients': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER),
                                     description='the ids of the subscribers who will receive the email',
                                     default=[]),
        'subject': openapi.Schema(type=openapi.TYPE_STRING, description='the subject of the email', default=''),
        'message': openapi.Schema(type=openapi.TYPE_STRING, description='the message to send', default=''),
    }),
    responses={
        '200': openapi.Response(
            description='Success',
            examples={
                'application/json': {
                    'msg': 'Emails successfully sent'
                },
            }
        ),
        '400': openapi.Response(
            description='Bad request',
            examples={
                'application/json': {
                    'msg': 'Recipient list required'
                },
            }
        ),
        '500': openapi.Response(
            description='Internal Server Error',
            examples={
                'application/json': {
                    'msg': 'Error sending email'
                },
            }
        )
    })
@api_view(['POST'])
def send_email_to_specific_subscriber(request):
    """Allows the sending of emails to specific subscribers."""
    data = request.data
    ids_subscribers = data.get('recipients', [])
    if not ids_subscribers:
        return Response({'msg': 'Recipient list required'}, status=400)

    recipient_list = []
    ids_subscribers_not_found = []
    for id_subscriber in ids_subscribers:
        try:
            subscriber = Subscriber.objects.get(pk=id_subscriber)
            recipient_list.append(subscriber.email)
        except ObjectDoesNotExist:
            ids_subscribers_not_found.append(id_subscriber)

    subject = data.get('subject', '')
    email_from = settings.EMAIL_HOST_USER
    message = data.get('message', '')
    email_sent = send_mail(subject, message, email_from, recipient_list)

    if email_sent:
        if ids_subscribers_not_found:
            return Response({'msg': f'Emails partially sent, subscribers not found: {ids_subscribers_not_found}'},
                            status=206)
        return Response({'msg': 'Emails successfully sent'}, status=200)
    return Response({'msg': 'Error sending email'}, status=500)
