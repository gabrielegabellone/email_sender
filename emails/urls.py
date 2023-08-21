from django.urls import path

from emails.views import EmailAllSubscribers, EmailSpecificSubscribers

urlpatterns = [
    path("send_to_all/", EmailAllSubscribers.as_view()),
    path("send/", EmailSpecificSubscribers.as_view())
]
