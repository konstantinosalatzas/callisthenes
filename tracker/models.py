from django.db import models
from django.conf import settings
from django.utils import timezone

class Training(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)
    sets = models.IntegerField(default=0) # calculated from training sets

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def calculate_sets(self) -> int:
        """
        Calculate total number of sets.
        """
        return Set.objects.filter(training=self.pk).count()

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
    meal_date = models.DateField(blank=True, null=True)
    meal_number = models.IntegerField(default=1) # number of meal of the day
    protein = models.FloatField(default=0.0) # calculated from ingredients protein
    carbs = models.FloatField(default=0.0) # calculated from ingredients carbs
    fats = models.FloatField(default=0.0) # calculated from ingredients fats
    kcal = models.FloatField(default=0.0) # calculated from ingredients calories

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def calculate(self, field: str) -> float:
        """
        Calculate meal protein/carbs/fats/calories from ingredients.
        """
        ingredients = Ingredient.objects.filter(meal=self.pk)
        sum = 0.0
        for ingredient in ingredients:
            sum += ingredient.__getattribute__(field)
        return sum

    def __str__(self):
        return "{}, {} @ {}".format(self.user, self.title, self.meal_date)

class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.FloatField(default=0.0)
    unit = models.CharField(max_length=200) # unit of measurement
    protein = models.FloatField(default=0.0) # in grams
    carbs = models.FloatField(default=0.0) # in grams
    fats = models.FloatField(default=0.0) # in grams
    kcal = models.FloatField(default=0.0) # calculated from ingredient macronutrients

    def calculate_calories(self) -> float:
        """
        Calculate ingredient calories (kcal) from macronutrient quantities measured in grams.
        """
        return (self.protein * 4.0 + self.carbs * 4.0 + self.fats * 9.0)

    def __str__(self):
        return "{}, {} @ {} - {}".format(self.meal.user, self.meal.title, self.meal.meal_date,
                                         self.name)

class Unit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=200)
    units = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0) # per number of units
    carbs = models.FloatField(default=0.0) # per number of units
    fats = models.FloatField(default=0.0) # per number of units
    kcal = models.FloatField(default=0.0) # calculated from ingredient per number of units

    def calculate_calories(self) -> float:
        """
        Calculate ingredient calories (kcal) from macronutrient quantities per number of units.
        """
        return (self.protein * 4.0 + self.carbs * 4.0 + self.fats * 9.0)

    def __str__(self):
        return "{} - {}".format(self.user, self.name)
