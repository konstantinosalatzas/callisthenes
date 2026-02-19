from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Training, Set, Meal, Ingredient, Unit
from .forms import TrainingForm, SetForm, MealForm, IngredientForm, UnitForm
from .heatmap import training_heatmap

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def index(request):
    heatmap = []
    if request.user.is_authenticated:
        heatmap = training_heatmap(request.user)
    return render(request, 'tracker/index.html', {'heatmap': heatmap})

# Training model

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
    return render(request, 'tracker/training_new.html', {'form': form})

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
    return render(request, 'tracker/training_edit.html', {'form': form, 'training': training})

@login_required
def training_remove(request, pk):
    training = get_object_or_404(Training, pk=pk, user=request.user)
    #if request.method=='POST':
    training.delete()
    return redirect('training_list')

# Set model

@login_required
def set_detail(request, pk):
    set = get_object_or_404(Set, pk=pk)
    get_object_or_404(Training, pk=set.training.pk, user=request.user)
    return render(request, 'tracker/set_detail.html', {'set': set})

@login_required
def set_new(request, pk):
    training = get_object_or_404(Training, pk=pk, user=request.user)
    if request.method == "POST":
        form = SetForm(request.POST)
        if form.is_valid():
            set = form.save(commit=False)
            set.training = get_object_or_404(Training, pk=pk)
            set.save()
            training.sets = training.calculate_sets()
            training.save()
            return redirect('set_detail', pk=set.pk)
    else:
        form = SetForm()
    return render(request, 'tracker/set_new.html', {'form': form, 'training': training})

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
    return render(request, 'tracker/set_edit.html', {'form': form, 'set': set})

@login_required
def set_remove(request, pk):
    set = get_object_or_404(Set, pk=pk)
    training = get_object_or_404(Training, pk=set.training.pk, user=request.user)
    training_pk = set.training.pk
    #if request.method=='POST':
    set.delete()
    training.sets = training.calculate_sets()
    training.save()
    return redirect('training_detail', pk=training_pk)

# Meal model

@login_required
def meal_list(request):
    meals = []
    if request.user.is_authenticated:
        meals = Meal.objects.filter(user=request.user, published_date__lte=timezone.now()).order_by('-meal_date', 'meal_number')
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
    return render(request, 'tracker/meal_new.html', {'form': form})

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
    return render(request, 'tracker/meal_edit.html', {'form': form, 'meal': meal})

@login_required
def meal_remove(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    #if request.method=='POST':
    meal.delete()
    return redirect('meal_list')

# Ingredient model

def macronutrient_percentages(ingredient):
    protein = ingredient.protein or 0
    carbs = ingredient.carbs or 0
    fats = ingredient.fats or 0
    total_macros = protein + carbs + fats
    if total_macros:
        p1 = round(protein / total_macros * 100, 1)
        p2 = round(carbs / total_macros * 100, 1)
        p3 = round(fats / total_macros * 100, 1)
    else:
        p1 = p2 = p3 = 0.0
    p1_p2 = round(p1 + p2, 1)
    return (p1, p2, p3, p1_p2, total_macros)

@login_required
def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    get_object_or_404(Meal, pk=ingredient.meal.pk, user=request.user)
    (p1, p2, p3, p1_p2, total_macros) = macronutrient_percentages(ingredient)
    return render(request, 'tracker/ingredient_detail.html', {'ingredient': ingredient,
                                                              'p1': p1, 'p2': p2, 'p3': p3, 'p1_p2': p1_p2, 'total_macros': total_macros,})

@login_required
def ingredient_new(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == "POST":
        form = IngredientForm(request.POST, user=request.user)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.meal = get_object_or_404(Meal, pk=pk)
            ingredient.update_calculated_fields()
            ingredient.save()
            meal.update_calculated_fields()
            meal.save()
            return redirect('ingredient_detail', pk=ingredient.pk)
    else:
        form = IngredientForm(user=request.user)
    return render(request, 'tracker/ingredient_new.html', {'form': form, 'meal': meal})

@login_required
def ingredient_edit(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    get_object_or_404(Meal, pk=ingredient.meal.pk, user=request.user)
    if request.method == "POST":
        form = IngredientForm(request.POST, instance=ingredient, user=request.user)
        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.update_calculated_fields()
            ingredient.save()
            meal = ingredient.meal
            meal.update_calculated_fields()
            meal.save()
            return redirect('ingredient_detail', pk=ingredient.pk)
    else:
        form = IngredientForm(instance=ingredient, user=request.user)
    return render(request, 'tracker/ingredient_edit.html', {'form': form, 'ingredient': ingredient})

@login_required
def ingredient_remove(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    meal = get_object_or_404(Meal, pk=ingredient.meal.pk, user=request.user)
    meal_pk = ingredient.meal.pk
    #if request.method=='POST':
    ingredient.delete()
    meal.update_calculated_fields()
    meal.save()
    return redirect('meal_detail', pk=meal_pk)

# Unit model

@login_required
def unit_list(request):
    units = []
    if request.user.is_authenticated:
        units = Unit.objects.filter(user=request.user, published_date__lte=timezone.now()).order_by('name')
    return render(request, 'tracker/unit_list.html', {'units': units})

@login_required
def unit_detail(request, pk):
    unit = get_object_or_404(Unit, pk=pk, user=request.user)
    return render(request, 'tracker/unit_detail.html', {'unit': unit})

@login_required
def unit_new(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.user = request.user
            unit.published_date = timezone.now()
            unit.kcal = unit.calculate_calories()
            unit.save()
            return redirect('unit_detail', pk=unit.pk)
    else:
        form = UnitForm()
    return render(request, 'tracker/unit_new.html', {'form': form})

@login_required
def unit_edit(request, pk):
    unit = get_object_or_404(Unit, pk=pk, user=request.user)
    if request.method == "POST":
        form = UnitForm(request.POST, instance=unit)
        if form.is_valid():
            unit = form.save(commit=False)
            unit.user = request.user
            unit.published_date = timezone.now()
            unit.kcal = unit.calculate_calories()
            unit.save()
            ingredients = Ingredient.objects.filter(unit=pk)
            for ingredient in ingredients:
                ingredient.update_calculated_fields()
                ingredient.save()
                meal = ingredient.meal
                meal.update_calculated_fields()
                meal.save()
            return redirect('unit_detail', pk=unit.pk)
    else:
        form = UnitForm(instance=unit)
    return render(request, 'tracker/unit_edit.html', {'form': form, 'unit': unit})

@login_required
def unit_remove(request, pk):
    unit = get_object_or_404(Unit, pk=pk, user=request.user)
    #if request.method=='POST':
    ingredients = Ingredient.objects.filter(unit=pk)
    meals = []
    for ingredient in ingredients:
        meals.append(ingredient.meal)
    unit.delete()
    for meal in meals:
        meal.update_calculated_fields()
        meal.save()
    return redirect('unit_list')
