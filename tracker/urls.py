from django.urls import path

from . import views

urlpatterns = [
    path('', views.training_list, name='training_list'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('training/new/', views.training_new, name='training_new'),
    path('training/<int:pk>/edit/', views.training_edit, name='training_edit'),
    path('training/<int:pk>/publish/', views.training_publish, name='training_publish'),
    path('training/<int:pk>/remove/', views.training_remove, name='training_remove'),
]
