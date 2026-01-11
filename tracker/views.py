from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Training, Set, Meal, Ingredient
from .forms import TrainingForm, SetForm, MealForm

def index(request):
    return render(request, 'tracker/index.html')

@login_required
def training_list(request):
    trainings = []
    if request.user.is_authenticated:
        trainings = Training.objects.filter(user=request.user, published_date__lte=timezone.now()).order_by('-training_date')
    return render(request, 'tracker/training_list.html', {'trainings': trainings})

@login_required
def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk, user=request.user)
    sets = Set.objects.filter(training=pk).order_by('name', 'set_number')
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
    training = get_object_or_404(Training, pk=pk, user=request.user)
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
    training = get_object_or_404(Training, pk=pk, user=request.user)
    if request.method=='POST':
        training.publish()
    return redirect('training_detail', pk=pk)

@login_required
def training_remove(request, pk):
    training = get_object_or_404(Training, pk=pk, user=request.user)
    #if request.method=='POST':
    training.delete()
    return redirect('training_list')

@login_required
def set_detail(request, pk):
    set = get_object_or_404(Set, pk=pk)
    get_object_or_404(Training, pk=set.training.pk, user=request.user)
    return render(request, 'tracker/set_detail.html', {'set': set})

@login_required
def set_new(request, pk):
    get_object_or_404(Training, pk=pk, user=request.user)
    if request.method == "POST":
        form = SetForm(request.POST)
        if form.is_valid():
            set = form.save(commit=False)
            set.training = get_object_or_404(Training, pk=pk)
            set.save()
            return redirect('set_detail', pk=set.pk)
    else:
        form = SetForm()
    return render(request, 'tracker/set_edit.html', {'form': form})

@login_required
def set_edit(request, pk):
    set = get_object_or_404(Set, pk=pk)
    get_object_or_404(Training, pk=set.training.pk, user=request.user)
    if request.method == "POST":
        form = SetForm(request.POST, instance=set)
        if form.is_valid():
            set = form.save(commit=False)
            set.save()
            return redirect('set_detail', pk=set.pk)
    else:
        form = SetForm(instance=set)
    return render(request, 'tracker/set_edit.html', {'form': form})

@login_required
def set_publish(request, pk):
    set = get_object_or_404(Set, pk=pk)
    get_object_or_404(Training, pk=set.training.pk, user=request.user)
    if request.method=='POST':
        set.publish()
    return redirect('set_detail', pk=pk)

@login_required
def set_remove(request, pk):
    set = get_object_or_404(Set, pk=pk)
    get_object_or_404(Training, pk=set.training.pk, user=request.user)
    training_pk = set.training.pk
    #if request.method=='POST':
    set.delete()
    return redirect('training_detail', pk=training_pk)

@login_required
def meal_list(request):
    meals = []
    if request.user.is_authenticated:
        meals = Meal.objects.filter(user=request.user, published_date__lte=timezone.now()).order_by('-meal_date')
    return render(request, 'tracker/meal_list.html', {'meals': meals})

@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    ingredients = Ingredient.objects.filter(meal=pk).order_by('name')
    return render(request, 'tracker/meal_detail.html', {'meal': meal,
                                                        'ingredients': ingredients})

@login_required
def meal_new(request):
    if request.method == "POST":
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.published_date = timezone.now()
            meal.save()
            return redirect('meal_detail', pk=meal.pk)
    else:
        form = MealForm()
    return render(request, 'tracker/meal_edit.html', {'form': form})

@login_required
def meal_edit(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.published_date = timezone.now()
            meal.save()
            return redirect('meal_detail', pk=meal.pk)
    else:
        form = MealForm(instance=meal)
    return render(request, 'tracker/meal_edit.html', {'form': form})

@login_required
def meal_publish(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method=='POST':
        meal.publish()
    return redirect('meal_detail', pk=pk)
