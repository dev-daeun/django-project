from django.test import TestCase
from django.utils import timezone

from .models import Question

import datetime


class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question_should_return_False(self):
        """
        was_published_recently() returns False for questions whose pub_date is
        in the future.
        :return:
        """
        # Given
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        # When
        was__published_recently = future_question.was_published_recently()

        # Then
        self.assertIs(was__published_recently, False)

    def test_was_published_recently_with_old_question_should_return_False(self):
        """
        was_published_recently() returns False for questions whose pub_date is
        older than 1 day.
        :return:
        """
        # Given
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)

        # When
        was_published_recently = old_question.was_published_recently()

        # Then
        self.assertIs(was_published_recently, False)

    def test_was_published_recently_with_recent_question_should_return_True(self):
        """
        was_published_recently() returns True for questions whose pub_date is
        within the last day.
        :return:
        """
        # Given
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)

        # When
        was_published_recently = recent_question.was_published_recently()

        # Then
        self.assertIs(was_published_recently, True)



