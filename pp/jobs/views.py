# jobs/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import JobForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Job
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
        messages.error(request, "Вы не можете создавать вакансии, так как не являетесь преподавателем.")
        return redirect('home')
        
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
    raise Exception("This is a test 500 error.")

@user_passes_test(is_teacher)
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    # Проверяем, что пользователь — преподаватель и является создателем вакансии
    if job.creator == request.user:
        job.delete()  # Удаляем вакансию
        return redirect('home')  # Перенаправляем на главную страницу после удаления
    else:
        return HttpResponseForbidden("Вы не имеете права удалять эту вакансию.")