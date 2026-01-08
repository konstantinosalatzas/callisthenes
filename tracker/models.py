from django.db import models
from django.conf import settings
from django.utils import timezone

class Training(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # name
    text = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)
    sets = models.IntegerField(default=1) # TODO: create method

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Set(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    set_number = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    resistance_weight = models.FloatField(default=0.0)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return "{}, set no.{}".format(self.training.title, self.set_number)
