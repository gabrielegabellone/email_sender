from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from subscribers.models import Subscriber


class EmailAllSubscribers(APIView):
    """View for sending emails to all subscribers."""
    def post(self, request):
        data = request.POST
        subscribers = Subscriber.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]
        subject = data.get('subject', '')
        email_from = settings.EMAIL_HOST_USER
        message = data.get('message', '')
        email_sent = send_mail(subject, message, email_from, recipient_list)
        if email_sent:
            return Response({'msg': 'Emails successfully sent'}, status=200)
        return Response({'msg': 'Error sending email'}, status=500)


class EmailSpecificSubscribers(APIView):
    """View for sending emails to specific subscribers."""
    def post(self, request):
        data = request.POST
        ids_subscribers = data.getlist('recipients', [])
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
                return Response({'msg': f'Emails partially sent, subscribers not found: {ids_subscribers_not_found}'}, status=206)
            return Response({'msg': 'Emails successfully sent'}, status=200)
        return Response({'msg': 'Error sending email'}, status=500)
