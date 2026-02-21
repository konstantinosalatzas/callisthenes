from django.db import models
from django.conf import settings
from django.utils import timezone

class Training(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    training_date = models.DateField(blank=True, null=True)
    sets = models.IntegerField(default=0) # total number of training sets

    def calculate_sets(self) -> int:
        """
        Calculate total number of training sets.
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
    comment = models.CharField(max_length=200, blank=True, null=True)

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

    def calculate(self, field: str) -> float:
        """
        Calculate meal protein/carbs/fats/calories from ingredients macronutrients.
        """
        ingredients = Ingredient.objects.filter(meal=self.pk)
        sum = 0.0
        for ingredient in ingredients:
            sum += ingredient.__getattribute__(field)
        return sum

    def update_calculated_fields(self):
        """
        Call calculate().
        """
        for field in ['protein', 'carbs', 'fats', 'kcal']:
            self.__setattr__(field, self.calculate(field))

    def __str__(self):
        return "{}, {} @ {}".format(self.user, self.title, self.meal_date)

class Unit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    unit_of_measurement = models.CharField(max_length=200)
    units = models.FloatField(default=0.1) # number of units
    protein = models.FloatField(default=0.0) # in grams per number of units
    carbs = models.FloatField(default=0.0) # in grams per number of units
    fats = models.FloatField(default=0.0) # in grams per number of units
    kcal = models.FloatField(default=0.0) # calculated from macronutrients per number of units
    cost = models.FloatField(default=0.0) # in euros per number of units

    def calculate_calories(self) -> float:
        """
        Calculate ingredient calories from macronutrients per number of units.
        """
        return (self.protein * 4.0 + self.carbs * 4.0 + self.fats * 9.0)

    def __str__(self):
        return "{} - {}".format(self.user, self.name)

class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)
    protein = models.FloatField(default=0.0) # calculated from protein per number of units
    carbs = models.FloatField(default=0.0) # calculated from carbs per number of units
    fats = models.FloatField(default=0.0) # calculated from fats per number of units
    kcal = models.FloatField(default=0.0) # calculated from calories per number of units
    cost = models.FloatField(default=0.0) # calculated from cost per number of units

    def calculate(self, field: str) -> float:
        """
        Calculate ingredient protein/carbs/fats/calories from macronutrients per number of units.
        """
        unit = self.unit
        return (self.quantity * unit.__getattribute__(field) / unit.units)

    def update_calculated_fields(self):
        """
        Call calculate().
        """
        for field in ['protein', 'carbs', 'fats', 'kcal']:
            self.__setattr__(field, self.calculate(field))

    def __str__(self):
        return "{}, {} @ {} - {}".format(self.meal.user, self.meal.title, self.meal.meal_date,
                                         self.name)
