# jobs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import JobForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job, Application
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages

# Проверка, что пользователь является преподавателем
def is_teacher(user):
    return user.groups.filter(name='teacher').exists()

# Представление для создания вакансии
# @user_passes_test(is_teacher)
def create_job(request):
    if not request.user.groups.filter(name="teacher").exists():
        # messages.error(request, "Вы не можете создавать вакансии, так как не являетесь преподавателем.")
        # return redirect('home')
        raise PermissionDenied("Вы не можете создавать вакансии, так как не являетесь преподавателем.")
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.creator = request.user  # Устанавливаем текущего пользователя как создателя вакансии
            job.save()
            return redirect('home')  # Перенаправление после успешного создания вакансии
        else:
            # Возвращаем ошибки валидации
            return JsonResponse({
                "error": "Validation Error",
                "message": "Некоторые параметры были переданы некорректно.",
                "details": form.errors,
            }, status=400)
    else:
        form = JobForm()

    return render(request, 'jobs/create_job.html', {'form': form})
    # raise Exception("This is a test 500 error.")

@user_passes_test(is_teacher)
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Проверяем, что пользователь — преподаватель и является создателем вакансии
    if job.creator == request.user:
        job.delete()  # Удаляем вакансию
        return redirect('home')  # Перенаправляем на главную страницу после удаления
    else:
        return HttpResponseForbidden("Вы не имеете права удалять эту вакансию.")

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Проверяем, что пользователь является студентом
    if not request.user.groups.filter(name='student').exists():
        return HttpResponseForbidden("Только студенты могут откликаться на вакансии.")
    
    # Проверяем, откликнулся ли пользователь уже на эту вакансию
    if Application.objects.filter(user=request.user, job=job).exists():
        # Если отклик уже есть, показываем сообщение об ошибке
        messages.error(request, "Вы уже откликнулись на эту вакансию.")
        return redirect('home')  # Перенаправляем на главную страницу вакансий
    
    # Если отклика нет, создаём новый
    Application.objects.create(user=request.user, job=job)
    messages.success(request, "Вы успешно откликнулись на вакансию!")
    return redirect('home')  # Перенаправляем на главную страницу вакансий

@login_required
def view_responses(request):
    # Проверяем, что пользователь — преподаватель
    if not request.user.groups.filter(name='teacher').exists():
        raise PermissionDenied("У вас нет доступа к этому разделу.")

    # Получаем все вакансии и их отклики
    applications = {}
    jobs = Job.objects.all()

    # Для каждой вакансии получаем её отклики
    for job in jobs:
        applications[job] = job.applications.all()
        
    return render(request, 'jobs/view_responses.html', {'applications': applications})