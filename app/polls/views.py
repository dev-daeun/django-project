from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from .models import *


class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Returns the last 5 published questions."""
        return self.model.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    # 템플릿에서 참조하는 객체 이름
    context_object_name = 'question'
    # path에서 지정한 uri 이름
    pk_url_kwarg = 'question_id'

    def get_object(self, queryset=None):
        requested_question = get_object_or_404(self.model, id=self.kwargs['question_id'])
        if requested_question.pub_date > timezone.now():
            raise Http404
        else:
            return requested_question


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'
    success_url = 'polls/results'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs['question_id'])


class VoteView(generic.edit.CreateView):
    model = Choice
    success_url = 'polls:results'

    def post(self, request, *args, **kwargs):
        try:
            selected_choice = get_object_or_404(self.model, id=request.POST['choice'])
        except KeyError:
            raise Http404
        else:
            selected_choice.votes = F('votes') + 1
            selected_choice.save()
            return redirect(self.success_url, question_id=self.kwargs['question_id'])
