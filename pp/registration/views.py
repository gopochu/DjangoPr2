from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Замените на страницу, куда перенаправить после регистрации
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
