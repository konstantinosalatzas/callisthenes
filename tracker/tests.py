from django.test import TestCase

from .models import Unit

class UnitModelTests(TestCase):
    def test_calculate_calories_with_integer_macronutrient_values(self):
        unit = Unit(protein=20, carbs=1, fats=1)
        self.assertEqual(unit.calculate_calories(), (20 * 4.0 + 1 * 4.0 + 1 * 9.0))

    def test_calculate_calories_with_float_macronutrient_values(self):
        unit = Unit(protein=20.5, carbs=0.5, fats=0.5)
        self.assertEqual(unit.calculate_calories(), (20.5 * 4.0 + 0.5 * 4.0 + 0.5 * 9.0))
