from django import forms

from .models import Training, Set, Meal, Ingredient, Unit

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
        fields = ('title', 'meal_date', 'meal_number')
        widgets = {
            'meal_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'set_number': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'class': 'form-control'}),
        }

class IngredientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        Limit units to user.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['unit'].queryset = Unit.objects.filter(user=user).order_by('name')

    class Meta:
        model = Ingredient
        fields = ('name', 'quantity', 'unit')
        widgets = {
            'quantity': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'step': '0.1', 'class': 'form-control'}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ('name', 'unit_of_measurement', 'units', 'protein', 'carbs', 'fats')
        widgets = {
            'units': forms.NumberInput(attrs={'type': 'number', 'min': '0.1', 'step': '0.1', 'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'step': '0.1', 'class': 'form-control'}),
            'carbs': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'step': '0.1', 'class': 'form-control'}),
            'fats': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'step': '0.1', 'class': 'form-control'}),
        }
