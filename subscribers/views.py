from rest_framework import generics

from subscribers.models import Subscriber
from .serializers import SubscriberSerializer


class ListSubscriber(generics.ListCreateAPIView):
    """
    get:
    Return a list of all the existing subscribers.

    post:
    Create a new subscriber.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer


class DetailSubscriber(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Returns a specific subscriber by id.

    put:
    Update a subscriber by id.

    delete:
    Delete a subscriber by id.

    patch:
    Modify a subscriber by id.
    """
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
