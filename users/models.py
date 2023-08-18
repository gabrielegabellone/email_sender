from django.db import models


class User(models.Model):
    class Meta:
        db_table = 'users'

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username
