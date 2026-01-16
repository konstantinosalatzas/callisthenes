from django.db import models
from django.conf import settings
from django.utils import timezone

class Training(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return "{}, {} @ {}".format(self.user, self.title, self.training_date)

class Set(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    set_number = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    resistance_weight = models.FloatField(default=0.0)
    comment = models.CharField(max_length=200)

    def __str__(self):
        return "{}, {} @ {} - {} (set {})".format(self.training.user, self.training.title, self.training.training_date,
                                                  self.name, self.set_number)

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    meal_date = models.DateField(blank=True, null=True) # number?

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return "{}, {} @ {}".format(self.user, self.title, self.meal_date)

class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0.0)
    unit = models.CharField(max_length=200) # unit of measurement
    protein = models.FloatField(default=0.0)
    carbs = models.FloatField(default=0.0)
    fats = models.FloatField(default=0.0)
    kcal = models.FloatField(default=0.0)

    def calculate_calories(self):
        return (self.protein * 4.0 + self.carbs * 4.0 + self.fats * 9.0)

    def __str__(self):
        return "{}, {} @ {} - {}".format(self.meal.user, self.meal.title, self.meal.meal_date,
                                         self.name)
