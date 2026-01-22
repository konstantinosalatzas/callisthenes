from django.test import TestCase

from .models import Unit

class UnitModelTests(TestCase):
    def test_calculate_calories_with_integer_macronutrient_values(self):
        unit = Unit(protein=20, carbs=1, fats=1)
        self.assertEqual(unit.calculate_calories(), (20 * 4 + 1 * 4 + 1 * 9))
