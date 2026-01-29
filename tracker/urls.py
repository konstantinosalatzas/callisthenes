from django.urls import path

from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('training', views.training_list, name='training_list'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('training/new/', views.training_new, name='training_new'),
    path('training/<int:pk>/edit/', views.training_edit, name='training_edit'),
    path('training/<int:pk>/remove/', views.training_remove, name='training_remove'),
    path('set/<int:pk>/', views.set_detail, name='set_detail'),
    path('training/<int:pk>/set/new/', views.set_new, name='set_new'),
    path('set/<int:pk>/edit/', views.set_edit, name='set_edit'),
    path('set/<int:pk>/remove/', views.set_remove, name='set_remove'),
    path('meal', views.meal_list, name='meal_list'),
    path('meal/<int:pk>/', views.meal_detail, name='meal_detail'),
    path('meal/new/', views.meal_new, name='meal_new'),
    path('meal/<int:pk>/edit/', views.meal_edit, name='meal_edit'),
    path('meal/<int:pk>/remove/', views.meal_remove, name='meal_remove'),
    path('ingredient/<int:pk>/', views.ingredient_detail, name='ingredient_detail'),
    path('meal/<int:pk>/ingredient/new/', views.ingredient_new, name='ingredient_new'),
    path('ingredient/<int:pk>/edit/', views.ingredient_edit, name='ingredient_edit'),
    path('ingredient/<int:pk>/remove/', views.ingredient_remove, name='ingredient_remove'),
    path('unit', views.unit_list, name='unit_list'),
    path('unit/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('unit/new/', views.unit_new, name='unit_new'),
    path('unit/<int:pk>/edit/', views.unit_edit, name='unit_edit'),
    path('unit/<int:pk>/remove/', views.unit_remove, name='unit_remove'),
]
