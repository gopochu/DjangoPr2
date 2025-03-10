from django.urls import path
from .views import register
from .views import login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Страница логина
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
