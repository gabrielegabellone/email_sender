from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

from subscribers.models import Subscriber


class EmailAllSubscribers(APIView):
    """View for sending emails to all users."""
    def post(self, request):
        data = request.POST
        users = Subscriber.objects.all()
        recipient_list = [user.email for user in users]
        subject = data.get('subject', '')
        email_from = settings.EMAIL_HOST_USER
        message = data.get('message', '')
        email_sent = send_mail(subject, message, email_from, recipient_list)
        if email_sent:
            return Response({'msg': 'Emails successfully sent'}, status=200)
        return Response({'msg': 'Error sending email'}, status=500)


class EmailSpecificSubscribers(APIView):
    """View for sending emails to specific users."""
    def post(self, request):
        data = request.POST
        ids_users = data.getlist('recipients', [])
        if not ids_users:
            return Response({'msg': 'Recipient list required'}, status=400)

        recipient_list = []
        users_not_found = []
        for id_user in ids_users:
            try:
                user = Subscriber.objects.get(pk=id_user)
                recipient_list.append(user.email)
            except ObjectDoesNotExist:
                users_not_found.append(id_user)

        subject = data.get('subject', '')
        email_from = settings.EMAIL_HOST_USER
        message = data.get('message', '')
        email_sent = send_mail(subject, message, email_from, recipient_list)

        if email_sent:
            if users_not_found:
                return Response({'msg': f'Emails partially sent, users not found: {users_not_found}'}, status=206)
            return Response({'msg': 'Emails successfully sent'}, status=200)
        return Response({'msg': 'Error sending email'}, status=500)
