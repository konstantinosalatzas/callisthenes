from django.urls import path

from . import views

urlpatterns = [
    path('', views.training_list, name='training_list'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('training/new/', views.training_new, name='training_new'),
    path('training/<int:pk>/edit/', views.training_edit, name='training_edit'),
    path('training/<int:pk>/publish/', views.training_publish, name='training_publish'),
    path('training/<int:pk>/remove/', views.training_remove, name='training_remove'),
    path('set/<int:pk>/', views.set_detail, name='set_detail'),
    path('training/<int:pk>/set/new/', views.set_new, name='set_new'),
    path('set/<int:pk>/edit/', views.set_edit, name='set_edit'),
    path('set/<int:pk>/publish/', views.set_publish, name='set_publish'),
    path('set/<int:pk>/remove/', views.set_remove, name='set_remove'),
]
