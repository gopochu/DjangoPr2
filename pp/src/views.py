from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from jobs.models import Job
  
# def index(request):
#     jobs = Job.objects.all()

#     # Проверяем, является ли пользователь преподавателем
#     is_teacher = request.user.groups.filter(name='teacher').exists()

#     # Передаем информацию о возможности удаления вакансий в шаблон
#     return render(request, 'index.html', {'jobs': jobs, 'is_teacher': is_teacher})
def index(request):
    # jobs = Job.objects.all()
    query = request.GET.get('q')  # Получаем параметр поиска
    if query:
        # Фильтруем вакансии по ключевым словам
        jobs = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query)
    else:
        # Если нет поискового запроса, показываем все вакансии
        jobs = Job.objects.all()
    is_teacher = request.user.groups.filter(name='teacher').exists()  # Проверка, является ли пользователь учителем
    return render(request, 'index.html', {'jobs': jobs, 'is_teacher': is_teacher})
 
def about(request):
    return HttpResponse("О сайте")
 
def contact(request):
    return HttpResponse("Контакты")

# Обработчик для 400 Bad Request
def custom_bad_request(request, exception):
    return JsonResponse({
        "error": "Bad Request",
        "message": "Ваш запрос некорректен. Проверьте параметры и попробуйте снова.",
        "status_code": 400,
    }, status=400)

# Обработчик для 403 Forbidden
def custom_permission_denied(request, exception):
    return JsonResponse({
        "error": "Permission Denied",
        "message": "У вас нет прав на выполнение этого действия.",
        "status_code": 403,
    }, status=403)

# Обработчик для 404 Not Found
def custom_page_not_found(request, exception):
    return JsonResponse({
        "error": "Page Not Found",
        "message": "Ресурс не найден. Проверьте URL и попробуйте снова.",
        "status_code": 404,
    }, status=404)

# Обработчик для 500 Internal Server Error
def custom_server_error(request):
    return JsonResponse({
        "error": "Internal Server Error",
        "message": "Произошла ошибка на сервере. Пожалуйста, попробуйте позже.",
        "status_code": 500,
    }, status=500)
    
