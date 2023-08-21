from django.urls import path

from .views import ListSubscriber, DetailSubscriber

urlpatterns = [
    path('', ListSubscriber.as_view()),
    path('<int:pk>/', DetailSubscriber.as_view())
]
