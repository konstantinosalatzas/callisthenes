from django import forms

from .models import Training, Set

class TrainingForm(forms.ModelForm):

    class Meta:
        model = Training
        fields = ('title', 'text', 'training_date', 'sets')
        widgets = {
            'training_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'type': 'number', 'min': '1', 'class': 'form-control'}),
        }

class SetForm(forms.ModelForm):

    class Meta:
        model = Set
        fields = ('set_number', 'reps')
