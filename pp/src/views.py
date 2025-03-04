from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
  
def index(request):
    return render(request, "index.html")
 
def about(request):
    return HttpResponse("О сайте")
 
def contact(request):
    return HttpResponse("Контакты")