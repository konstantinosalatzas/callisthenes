from django import forms

from .models import Training, Set, Meal, Ingredient

class TrainingForm(forms.ModelForm):

    class Meta:
        model = Training
        fields = ('title', 'training_date')
        widgets = {
            'training_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ('name', 'set_number', 'reps', 'resistance_weight', 'comment')
        widgets = {
            'set_number': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'class': 'form-control'}),
            'resistance_weight': forms.NumberInput(attrs={'type': 'number', 'step': '0.25', 'class': 'form-control'}),
        }

class MealForm(forms.ModelForm):

    class Meta:
        model = Meal
        fields = ('title', 'meal_date')
        widgets = {
            'meal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class IngredientForm(forms.ModelForm):

    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit')
        widgets = {
            'quantity': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'step': '0.1', 'class': 'form-control'}),
        }
