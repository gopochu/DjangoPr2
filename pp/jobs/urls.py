# jobs/urls.py
from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('create/', views.create_job, name='create_job'),  # URL для создания вакансии
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
]
