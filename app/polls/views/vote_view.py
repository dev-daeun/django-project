from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views import generic

from ..models import Choice


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
