from django.shortcuts import render
from django.http import HttpResponse

def indexPage(request):
    return HttpResponse("Hello, world. You're at the index.")
