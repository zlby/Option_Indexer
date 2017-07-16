from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')


def doc(request):
    return render_to_response('doc.html')
