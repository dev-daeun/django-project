from django.shortcuts import redirect


def index(request):

    # url 네임스페이싱을 따라야 함.
    return redirect('polls:index')
