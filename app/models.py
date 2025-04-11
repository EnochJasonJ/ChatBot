from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AIFeedModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return f"{self.question[:10]} - {self.answer[:10]}"