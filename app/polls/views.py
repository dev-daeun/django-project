from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Hello, world. This is poll system index')


def detail(request, question_id):
    return HttpResponse('This is question : %s' % question_id)


def result(request, question_id):
    return HttpResponse('%s result :' % question_id)


def vote(request, question_id):
    return HttpResponse('voting on question %s' % question_id)