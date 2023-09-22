from django.shortcuts import render, HttpResponse


def home(request):
    return render(request, 'book/home.html')
