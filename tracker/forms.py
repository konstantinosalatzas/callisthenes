from django import forms

from .models import Training

class TrainingForm(forms.ModelForm):

    class Meta:
        model = Training
        fields = ('title', 'text', 'training_date', 'sets', 'reps')
        widgets = {
            'training_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={'type': 'number', 'min': '0', 'class': 'form-control'}),
        }
