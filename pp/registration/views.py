from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            
            # Сохранение пользователя
            user.save()

            # Добавление пользователя в группу "student" или "teacher"
            if role == 'student':
                group = Group.objects.get(name='student')
            else:
                group = Group.objects.get(name='teacher')
            user.groups.add(group)

            login(request, user)
            return redirect('home')  # Перенаправление после регистрации
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
