from django.urls import path

from emails.views import EmailAPI

urlpatterns = [
    path("send/", EmailAPI.as_view()),
]