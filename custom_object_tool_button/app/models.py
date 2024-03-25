from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Notification(models.Model):
    title = models.CharField(max_length=100, default="")
    body = models.CharField(max_length=300, default="")
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title