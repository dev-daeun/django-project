from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
    except Http404:
        return render(request, '404.html', {
            'message': 'Question Does not exists.'
        })
    # try:
    #     detail_question = Question.objects.get(
    #         id=question_id
    #     )
    # except Question.DoesNotExist:
    #     context = {
    #         'message': 'Question does not exists.'
    #     }
    #     raise render(request, '404.html', context)
    # else:
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)


def result(request, question_id):
    return HttpResponse('%s result :' % question_id)


def vote(request, question_id):
    return HttpResponse('voting on question %s' % question_id)