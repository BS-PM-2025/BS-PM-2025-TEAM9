from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserForm, StudentSignupForm, TeacherSignupForm, ManagerSignupForm
from .models import Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def student_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentSignupForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            login(request, user)
            return redirect('student_home')  # You'll create this page later
    else:
        user_form = UserForm()
        student_form = StudentSignupForm()
    return render(request, 'users/student_signup.html', {
        'user_form': user_form,
        'profile_form': student_form
    })

def teacher_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherSignupForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            login(request, user)
            return redirect('teacher_home')  # You'll create this page later
    else:
        user_form = UserForm()
        teacher_form = TeacherSignupForm()
    return render(request, 'users/teacher_signup.html', {
        'user_form': user_form,
        'profile_form': teacher_form
    })
from django.contrib.auth.decorators import login_required

@login_required
def student_home(request):
    return render(request, 'users/student_home.html')

@login_required
def teacher_home(request):
    return render(request, 'users/teacher_home.html')
def root_redirect(request):
    return redirect('login')


@login_required
def redirect_after_login(request):
    user = request.user
    if hasattr(user, 'student'):
        return redirect('student_home')
    elif hasattr(user, 'teacher'):
        return redirect('teacher_home')
    elif hasattr(user, 'manager'):
        return redirect('manager_home')
    else:
        return redirect('login')

def manager_signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        manager_form = ManagerSignupForm(request.POST)
        if user_form.is_valid() and manager_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            manager = manager_form.save(commit=False)
            manager.user = user
            manager.save()
            login(request, user)
            return redirect('manager_home')
    else:
        user_form = UserForm()
        manager_form = ManagerSignupForm()
    return render(request, 'users/manager_signup.html', {
        'user_form': user_form,
        'profile_form': manager_form
    })
@login_required
def manager_home(request):
    return render(request, 'users/manager_home.html')
