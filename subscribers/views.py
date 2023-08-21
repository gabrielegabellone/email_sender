from rest_framework import generics

from subscribers.models import Subscriber
from .serializers import SubscriberSerializer


class ListSubscriber(generics.ListCreateAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class DetailSubscriber(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
