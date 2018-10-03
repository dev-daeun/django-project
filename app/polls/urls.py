from django.contrib import admin
from django.urls import path

from .views import *

# urls.py에 app_name을 정의하면 template에서 app_name을 url의 네임스페이스로 쓸 수 있다.
# polls/templates/polls/index.html 참고
app_name = 'polls'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:question_id>/', DetailView.as_view(), name='detail'),
    path('<int:question_id>/results/', ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', VoteView.as_view(), name='vote'),
]
