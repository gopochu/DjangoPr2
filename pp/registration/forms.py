from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

ROLE_CHOICES = [
    ('student', 'Студент'),
    ('teacher', 'Преподаватель'),
]

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Роль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
