from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Training, Set
from .forms import TrainingForm, SetForm

def training_list(request):
    trainings = Training.objects.filter(published_date__lte=timezone.now()).order_by('-training_date')
    return render(request, 'tracker/training_list.html', {'trainings': trainings})

def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    sets = Set.objects.filter(training=pk).order_by('set_number')
    return render(request, 'tracker/training_detail.html', {'training': training,
                                                            'sets': sets})

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

def set_detail(request, pk):
    set = get_object_or_404(Set, pk=pk)
    return render(request, 'tracker/set_detail.html', {'set': set})

@login_required
def set_new(request):
    if request.method == "POST":
        form = SetForm(request.POST)
        if form.is_valid():
            set = form.save(commit=False)
            set.save()
            return redirect('set_detail', pk=set.pk)
    else:
        form = SetForm()
    return render(request, 'tracker/set_edit.html', {'form': form})

@login_required
def set_edit(request, pk):
    set = get_object_or_404(Set, pk=pk)
    if request.method == "POST":
        form = SetForm(request.POST, instance=set)
        if form.is_valid():
            set = form.save(commit=False)
            set.user = request.user
            set.save()
            return redirect('set_detail', pk=set.pk)
    else:
        form = SetForm(instance=set)
    return render(request, 'tracker/set_edit.html', {'form': form})

@login_required
def set_publish(request, pk):
    set = get_object_or_404(Set, pk=pk)
    if request.method=='POST':
        set.publish()
    return redirect('set_detail', pk=pk)

@login_required
def set_remove(request, pk):
    set = get_object_or_404(Set, pk=pk)
    #if request.method=='POST':
    set.delete()
    return redirect('training_list') # TODO: go to training detail
