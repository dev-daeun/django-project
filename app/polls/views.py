from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(
        request=request,
        template_name='polls/index.html',
        context={
            'latest_question_list': latest_question_list,
        },
    )


def detail(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
    except Http404:
        return render(
            request=request,
            template_name='404.html',
            context={
                'message': 'Question Does not exists.'
            },
        )
    else:
        return render(
            request=request,
            template_name='polls/detail.html',
            context={
                'question': question,
            },
        )


def result(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
    except Http404:
        return render(
            request=request,
            template_name='404.html',
            context={
                'message': 'Question Does not exists.'
            },
        )
    else:
        return render(
            request=request,
            template_name='polls/results.html',
            context={
                'question': question
            },
        )


def vote(request, question_id):
    try:
        question = get_object_or_404(Question, id=question_id)
    except Http404:
        return render(
            request=request,
            template_name='404.html',
            context={
                'message': 'Question Does not exists.'
            },
        )
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
                },
            )
        else:
            # race condition 발생 가능.
            # 요청1의 쓰레드가 selected_choice.votes += 1 을 실행한다고 가정할 때,
            # 그 사이 요청2의 쓰레드가 selected_choice.votes += 1 과 selected_choice.save()를 실행하면
            # 디비에서 votes는 1이 더해진 것으로 갱신된다.
            # 그러나 요청1의 selected_choice.votes += 1 의 votes는 아직 votes가 증가하지 않은 상태이고,
            # 나중에야 selected_choice.save()를 호출하면 votes는 votes+1+1 이 아니라 votes+1 상태가 된다.
            # 이를 방지하기 위해 F() 객체를 쓴다.
            # F()객체에 모델의 필드가 할당되면 그 모델의 필드는 모델 인스턴스가 save()를 호출할 때까지 대기 상태에 머무른다.
            # => 요청1 에서 save()를 호출할 때까지 요청2에서는 대기한다는 뜻.

            selected_choice.votes += F('votes') + 1
            selected_choice.save()

            # E
            return HttpResponseRedirect(reverse(
                'polls:results',
                args=(question_id,),
            ))
