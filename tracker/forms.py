from django import forms

from .models import Training

class TrainingForm(forms.ModelForm):

    class Meta:
        model = Training
        fields = ('title', 'text', 'training_date')
        widgets = {
            'training_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
