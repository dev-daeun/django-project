from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='poll-index'),
    path('<int:question_id>/', detail, name='detail'),
    path('<int:question_id>/results/', result, name='results'),
    path('<int:question_id>/vote/', vote, name='vote'),
]
