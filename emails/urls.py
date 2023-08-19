from django.urls import path

from emails.views import EmailAllUsers, EmailSpecificUsers

urlpatterns = [
    path("send_to_all/", EmailAllUsers.as_view()),
    path("send/", EmailSpecificUsers.as_view())
]
