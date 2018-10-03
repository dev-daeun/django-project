from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

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
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)


def result(request, question_id):
    return HttpResponse('%s result :' % question_id)


def vote(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
    except Http404:
        return render(request, '404.html', {
            'message': 'Question Does not exists.'
        })
    else:
        try:
            # request.POST[value] => html 태그의 id 속성에 들어있는 값을 가져옴.
            selected_choice = get_object_or_404(Choice, id=request.POST['choice'])
        except (KeyError, Http404):
            return render(
                request=request,
                template_name='polls/detail.html',
                context={
                    'question': question,
                    'error_message': "You didn't select a choice.",
                })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse(
                'polls:results',
                args=(question_id,)))
