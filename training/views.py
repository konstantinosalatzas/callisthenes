from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic

from .models import Training, Performance

class IndexView(generic.ListView):
    template_name = "training/index.html"
    context_object_name = "latest_training_list"

    def get_queryset(self):
        """Return the last five trainings."""
        return Training.objects.order_by("-training_date")[:5]

class DetailView(generic.DetailView):
    model = Training
    template_name = "training/detail.html"

class ResultsView(generic.DetailView):
    model = Training
    template_name = "training/results.html"

def log(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    try:
        selected_performance = training.performance_set.get(pk=request.POST["performance"])
    except (KeyError, Performance.DoesNotExist):
        # Redisplay the training logging form.
        return render(
            request,
            "training/detail.html",
            {
                "training": training,
                "error_message": "You didn't log a performance.",
            },
        )
    else:
        selected_performance.sets = F("sets") + 1
        selected_performance.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("training:results", args=(training.id,)))
