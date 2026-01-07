from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Training
from .forms import TrainingForm

def training_list(request):
    trainings = Training.objects.filter(published_date__lte=timezone.now()).order_by('-training_date')
    return render(request, 'tracker/training_list.html', {'trainings': trainings})

def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    return render(request, 'tracker/training_detail.html', {'training': training})

@login_required
def training_new(request):
    if request.method == "POST":
        form = TrainingForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.published_date = timezone.now()
            training.save()
            return redirect('training_detail', pk=training.pk)
    else:
        form = TrainingForm()
    return render(request, 'tracker/training_edit.html', {'form': form})

@login_required
def training_edit(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method == "POST":
        form = TrainingForm(request.POST, instance=training)
        if form.is_valid():
            training = form.save(commit=False)
            training.user = request.user
            training.published_date = timezone.now()
            training.save()
            return redirect('training_detail', pk=training.pk)
    else:
        form = TrainingForm(instance=training)
    return render(request, 'tracker/training_edit.html', {'form': form})

@login_required
def training_publish(request, pk):
    training = get_object_or_404(Training, pk=pk)
    if request.method=='POST':
        training.publish()
    return redirect('training_detail', pk=pk)

@login_required
def training_remove(request, pk):
    training = get_object_or_404(Training, pk=pk)
    #if request.method=='POST':
    training.delete()
    return redirect('training_list')
