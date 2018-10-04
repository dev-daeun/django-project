from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views import generic

from ..models import *


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
