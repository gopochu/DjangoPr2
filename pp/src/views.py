from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from jobs.models import Job
  
def index(request):
    # jobs = Job.objects.all()
    user = request.user
    query = request.GET.get('q')  # Получаем параметр поиска
    if query:
        # Фильтруем вакансии по ключевым словам
        jobs = Job.objects.filter(title__icontains=query) | Job.objects.filter(description__icontains=query)
    else:
        # Если нет поискового запроса, показываем все вакансии
        jobs = Job.objects.all()
    
    if user.is_authenticated:
        # Создаём словарь с информацией о наличии отклика для каждой вакансии
        applications = {job.id: job.applications.filter(user=user).exists() for job in jobs}
    else:
        applications = {}
    is_teacher = request.user.groups.filter(name='teacher').exists()  # Проверка, является ли пользователь учителем
    is_student = request.user.groups.filter(name='student').exists()  # Проверка, является ли пользователь студентом
    return render(request, 'index.html', {'jobs': jobs, 'is_teacher': is_teacher, 'is_student': is_student, 'applications': applications,})
 

# Обработчик для 400 Bad Request
def custom_bad_request(request, exception):
    error_details = {
        "error": "Bad Request",
        "message": "Ваш запрос некорректен. Проверьте параметры и попробуйте снова.",
        "status_code": 400,
        "suggestions": [
            "Убедитесь, что все обязательные параметры переданы.",
            "Проверьте правильность типов данных в параметрах."
        ],
        "details": str(exception)  # Детали ошибки для разработчика
    }
    return render(request, 'error.html', error_details)


# Обработчик для 403 Forbidden
def custom_permission_denied(request, exception):
    error_details = {
        "error": "Permission Denied",
        "message": "У вас нет прав на выполнение этого действия.",
        "status_code": 403,
        "suggestions": [
            "Проверьте, что вы вошли в систему.",
            "Если вы преподаватель, убедитесь, что у вас есть права на выполнение этого действия."
        ],
        "details": str(exception)  # Детали ошибки для разработчика
    }
    return render(request, 'error.html', error_details)


# Обработчик для 404 Not Found
def custom_page_not_found(request, exception):
    error_details = {
        "error": "Page Not Found",
        "message": "Ресурс не найден. Проверьте URL и попробуйте снова.",
        "status_code": 404,
        "suggestions": [
            "Проверьте, правильно ли введен URL.",
            "Если вы переходите по старой ссылке, возможно, ресурс был перемещен или удален."
        ],
        "details": str(exception)  # Детали ошибки для разработчика
    }
    return render(request, 'error.html', error_details)


# Обработчик для 500 Internal Server Error
def custom_server_error(request):
    error_details = {
        "error": "Internal Server Error",
        "message": "Произошла ошибка на сервере. Пожалуйста, попробуйте позже.",
        "status_code": 500,
        "suggestions": [
            "Если ошибка повторяется, обратитесь к администраторам.",
            "Попробуйте обновить страницу позже."
        ]
    }
    return render(request, 'error.html', error_details)

    
