from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)


def detail(request, question_id):
    return HttpResponse('This is question : %s' % question_id)


def result(request, question_id):
    return HttpResponse('%s result :' % question_id)


def vote(request, question_id):
    return HttpResponse('voting on question %s' % question_id)