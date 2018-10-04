from django.test import TestCase
from django.shortcuts import reverse

from . import create_question


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

