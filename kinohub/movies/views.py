from django.shortcuts import render
from django.http import HttpResponse

from movies.models import Movie

def index(request):
    movies = Movie.objects.order_by('-created_on')[:5]
    output = ', '.join([m.title for m in movies])
    return HttpResponse('Home page, last added movies:' + output)
