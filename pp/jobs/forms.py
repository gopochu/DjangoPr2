# jobs/forms.py
from django import forms
from .models import Job
from .models import Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary']

    def save(self, commit=True):
        job = super().save(commit=False)
        if commit:
            job.save()
        return job
    
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = []