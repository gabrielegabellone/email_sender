from rest_framework import serializers

from subscribers.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    """Serializer class of the subscriber model. Takes care of serializing a subscriber considering id,
    email and username."""
    class Meta:
        model = Subscriber
        fields = ('id', 'email', 'username')
