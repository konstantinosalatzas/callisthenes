import datetime

from django.db import models
from django.utils import timezone

class Training(models.Model):
    training_title = models.CharField(max_length=200)
    training_date = models.DateTimeField()

    def __str__(self):
        return self.training_title

    def was_created_recently(self):
        return self.training_date >= timezone.now() - datetime.timedelta(days=1)

class Performance(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    performance_text = models.CharField(max_length=200)
    sets = models.IntegerField(default=1)

    def __str__(self):
        return self.performance_text
