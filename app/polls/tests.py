from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse

from .models import Question

import datetime


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published
    the given number of 'days' offset to now.
    (negative for questions published in the past,
    positive for questions that have yet to be published.)
    :param question_text:
    :param days:
    :return:
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    def test_detail_view_should_return_404_when_question_in_future_is_requested(self):
        # Given
        future_question = create_question(question_text='Future question', days=5)

        # When
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, 404)

    def test_detail_view_should_return_questions_when_question_in_past_is_requested(self):
        # Given
        past_question = create_question(question_text='Past Question.', days=-5)

        # When
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)

        # Then
        self.assertContains(response, past_question.question_text)
        self.assertEqual(response.status_code, 200)


class QuestionIndexViewTests(TestCase):
    def test_index_view_should_return_message_when_no_question_exists(self):
        # Given
        # Question is empty.

        # When
        response = self.client.get(reverse('polls:index'))

        # Then
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, "No polls are available.")
        self.assertEqual(response.status_code, 200)

    def test_index_view_should_return_questions_whose_pub_date_in_the_past(self):
        # Given
        create_question(question_text="Past question.", days=-30)

        # When
        response = self.client.get(reverse('polls:index'))

        # Then
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        self.assertEqual(response.status_code, 200)

    def test_index_view_should_not_return_questions_whose_pub_date_in_the_future(self):
        # Given
        create_question(question_text='Future question.', days=30)

        # When
        response = self.client.get(reverse('polls:index'))

        # Then
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        self.assertContains(response, "No polls are available.")
        self.assertEqual(response.status_code, 200)

    def test_index_view_should_return_only_past_questions_not_future_questions(self):
        # Given
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)

        # When
        response = self.client.get(reverse('polls:index'))

        # Then
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        self.assertEqual(response.status_code, 200)

    def test_index_view_should_return_two_questions_when_two_question_are_created(self):
        # Given
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)

        # When
        response = self.client.get(reverse('polls:index'))

        # Then
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        self.assertEqual(response.status_code, 200)


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

    def test_as_published_recently_with_old_question_should_return_False(self):
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
