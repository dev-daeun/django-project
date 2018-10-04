from django.utils import timezone
from ..models import Question

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

