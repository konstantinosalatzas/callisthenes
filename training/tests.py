import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Training

class TrainingModelTests(TestCase):
    def test_was_posted_recently_with_future_training(self):
        """
        was_posted_recently() returns False for trainings whose training_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_training = Training(training_date=time)
        self.assertIs(future_training.was_posted_recently(), False)

    def test_was_posted_recently_with_old_training(self):
        """
        was_posted_recently() returns False for trainings whose training_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_training = Training(training_date=time)
        self.assertIs(old_training.was_posted_recently(), False)

    def test_was_posted_recently_with_recent_training(self):
        """
        was_posted_recently() returns True for trainings whose training_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_training = Training(training_date=time)
        self.assertIs(recent_training.was_posted_recently(), True)

def create_training(training_title, days):
    """
    Create a training with the given `training_title` and posted the
    given number of `days` offset to now (negative for trainings posted
    in the past, positive for trainings that have yet to be posted).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Training.objects.create(training_title=training_title, training_date=time)

class TrainingIndexViewTests(TestCase):
    def test_no_trainings(self):
        """
        If no trainings exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("training:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No training is available.")
        self.assertQuerySetEqual(response.context["latest_training_list"], [])

    def test_past_training(self):
        """
        Trainings with a training_date in the past are displayed on the
        index page.
        """
        training = create_training(training_title="Past training.", days=-30)
        response = self.client.get(reverse("training:index"))
        self.assertQuerySetEqual(
            response.context["latest_training_list"],
            [training],
        )

    def test_future_training(self):
        """
        Trainings with a training_date in the future aren't displayed on
        the index page.
        """
        create_training(training_title="Future training.", days=30)
        response = self.client.get(reverse("training:index"))
        self.assertContains(response, "No training is available.")
        self.assertQuerySetEqual(response.context["latest_training_list"], [])

    def test_future_training_and_past_training(self):
        """
        Even if both past and future trainings exist, only past trainings
        are displayed.
        """
        training = create_training(training_title="Past training.", days=-30)
        create_training(training_title="Future training.", days=30)
        response = self.client.get(reverse("training:index"))
        self.assertQuerySetEqual(
            response.context["latest_training_list"],
            [training],
        )

    def test_two_past_trainings(self):
        """
        The trainings index page may display multiple trainings.
        """
        training1 = create_training(training_title="Past training 1.", days=-30)
        training2 = create_training(training_title="Past training 2.", days=-5)
        response = self.client.get(reverse("training:index"))
        self.assertQuerySetEqual(
            response.context["latest_training_list"],
            [training2, training1],
        )

class TrainingDetailViewTests(TestCase):
    def test_future_training(self):
        """
        The detail view of a training with a training_date in the future
        returns a 404 not found.
        """
        future_training = create_training(training_title="Future training.", days=5)
        url = reverse("training:detail", args=(future_training.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_training(self):
        """
        The detail view of a training with a training_date in the past
        displays the training's text.
        """
        past_training = create_training(training_title="Past Training.", days=-5)
        url = reverse("training:detail", args=(past_training.id,))
        response = self.client.get(url)
        self.assertContains(response, past_training.training_title)
