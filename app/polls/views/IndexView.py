from django.views import generic
from django.utils import timezone

from ..models import Question


class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Returns the last 5 published questions."""
        return self.model.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]