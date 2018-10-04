from django.test import TestCase
from django.shortcuts import reverse

from . import create_question


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

