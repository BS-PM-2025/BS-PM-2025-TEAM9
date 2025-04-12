from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Student, Teacher, Manager,  StudentEvent

from django.core.serializers.json import DjangoJSONEncoder
import json

# users/forms.py
from .models import StudentSchedule

class AddLessonForm(forms.ModelForm):
    class Meta:
        model = StudentSchedule
        fields = ['student', 'subject', 'day', 'time']

def student_home(request):
    student = request.user.student
    events = StudentEvent.objects.filter(student=student)
    events_json = json.dumps([
        {
            'title': e.title,
            'date': e.date.strftime('%Y-%m-%d'),
            'type': e.event_type,
            'color': '#e74c3c' if e.event_type == 'Exam' else '#3498db' if e.event_type == 'Lesson' else '#2ecc71'
        } for e in events
    ], cls=DjangoJSONEncoder)

    return render(request, 'users/student_home.html', {
        'events': events,
        'events_json': events_json
    })

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    profile = forms.ChoiceField(choices=[('student', 'Student'), ('teacher', 'Teacher')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'profile']  # ✅ FIXED


class StudentProfileUpdateForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Current Password')
    email = forms.EmailField(required=False, label='New Email')
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')


class teacherProfileUpdateForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Current Password')
    email = forms.EmailField(required=False, label='New Email')
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False, label='Confirm New Password')



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



class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['expertise']
