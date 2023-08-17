from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response


class EmailAPI(APIView):
    def post(self, request):
        data = request.data
        recipient_list = data.get('recipients')
        if not recipient_list:
            return Response({'msg': 'Recipient list required'}, status=400)
        subject = data.get('subject', '')
        email_from = settings.EMAIL_HOST_USER
        message = data.get('message', '')
        email_sent = send_mail(subject, message, email_from, recipient_list)
        if email_sent:
            return Response({'msg': 'Emails successfully sent'}, status=200)
        return Response({'msg': 'Error sending email'}, status=500)
