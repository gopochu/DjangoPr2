from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('create/', views.create_job, name='create_job'),  # URL для создания вакансии
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('responses/', views.view_responses, name='view_responses'),
]
