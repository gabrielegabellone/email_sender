from django.urls import path

from emails.views import send_email_to_all_subscribers, send_email_to_specific_subscriber

urlpatterns = [
    path("send_to_all/", send_email_to_all_subscribers),
    path("send/", send_email_to_specific_subscriber)
]
