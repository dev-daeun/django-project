from django.shortcuts import get_object_or_404
from django.views import generic

from ..models import Question


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'question'
    pk_url_kwarg = 'question_id'
    success_url = 'polls/results'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, id=self.kwargs['question_id'])