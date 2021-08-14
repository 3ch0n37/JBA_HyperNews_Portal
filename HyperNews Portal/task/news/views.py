from django.views import View
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
class Home(View):
    def get(self, request):
        return HttpResponse('Coming soon')
