from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from jobs.models import Job
  
# def index(request):
#     jobs = Job.objects.all()

#     # Проверяем, является ли пользователь преподавателем
#     is_teacher = request.user.groups.filter(name='teacher').exists()

#     # Передаем информацию о возможности удаления вакансий в шаблон
#     return render(request, 'index.html', {'jobs': jobs, 'is_teacher': is_teacher})
def index(request):
    jobs = Job.objects.all()
    is_teacher = request.user.groups.filter(name='teacher').exists()  # Проверка, является ли пользователь учителем
    return render(request, 'index.html', {'jobs': jobs, 'is_teacher': is_teacher})
 
def about(request):
    return HttpResponse("О сайте")
 
def contact(request):
    return HttpResponse("Контакты")