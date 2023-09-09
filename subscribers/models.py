from django.db import models


class Subscriber(models.Model):
    """Represents the model of a subscriber."""
    class Meta:
        db_table = 'subscribers'

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50)

    def __str__(self):
        """Returns a string representation of a subscriber."""
        return self.username
