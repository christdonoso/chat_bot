from django.db import models

# Create your models here.


class Message(models.Model):
    user_message = models.CharField(max_length=300)
    bot_message = models.TextField()
