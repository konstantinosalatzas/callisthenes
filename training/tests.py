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
