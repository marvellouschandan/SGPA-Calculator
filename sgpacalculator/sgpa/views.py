from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    string='My first app of SGPA Calcualtor'
    return HttpResponse(string)
