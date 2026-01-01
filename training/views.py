from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import Training

def index(request):
    latest_training_list = Training.objects.order_by("-training_date")[:5]
    context = {"latest_training_list": latest_training_list}
    return render(request, "training/index.html", context)

def detail(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    return render(request, "training/detail.html", {"training": training})
