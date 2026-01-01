from django.urls import path

from . import views

app_name = "training"

urlpatterns = [
    # ex: /training/
    path("", views.index, name="index"),
    # ex: /training/5/
    path("<int:training_id>/", views.detail, name="detail"),
]
