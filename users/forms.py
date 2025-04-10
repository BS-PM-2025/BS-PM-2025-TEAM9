from django import forms
from django.contrib.auth.models import User
from .models import Student, Teacher, Manager  


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentSignupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['bio']

class TeacherSignupForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['expertise']
class ManagerSignupForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['department']
