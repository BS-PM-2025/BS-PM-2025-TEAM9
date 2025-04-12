from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, StudentSignupForm, TeacherSignupForm, ManagerSignupForm, StudentProfileUpdateForm
from .models import Student, Teacher, Manager, StudentEvent, StudentSchedule, TeacherMessage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateformat import format
from django.http import JsonResponse




@login_required
def get_homework_by_date(request):
    date = request.GET.get('date')  # YYYY-MM-DD
    if date:
        events = StudentEvent.objects.filter(student=request.user, event_type='homework', date=date)
        data = [{'title': e.title, 'description': e.description} for e in events]
        return JsonResponse({'events': data})
    return JsonResponse({'error': 'No date provided'}, status=400)

@login_required
def student_messages(request):
    return render(request, 'users/student_messages.html')


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

def welcome(request):
    return render(request, 'users/welcome.html')



@login_required
def student_home(request):
    return render(request, 'users/student_home.html')

@login_required
def teacher_home(request):
    return render(request, 'users/teacher_home.html')
def root_redirect(request):
    return redirect('login')

def welcome(request):
    return render(request, 'users/welcome.html')


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


def welcome(request):
    return render(request, 'users/welcome.html')


from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Student, Teacher

def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            profile = form.cleaned_data['profile']
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            

            user.save()

            if profile == 'student':
                Student.objects.create(user=user)
                login(request, user)
                return redirect('student_home')
            elif profile == 'teacher':
                Teacher.objects.create(user=user)
                login(request, user)
                return redirect('teacher_home')

    else:
        form = UserForm()

    return render(request, 'users/signup.html', {'form': form})





# def welcome(request):
#     return render(request, 'users/welcome.html')

def welcome(request):
    print("🚀 Welcome page loaded")  # Check terminal output
    return render(request, 'users/welcome.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔍 Check actual role model connected to user
            if hasattr(user, 'student'):
                return redirect('student_home')
            elif hasattr(user, 'teacher'):
                return redirect('teacher_home')
            elif hasattr(user, 'manager'):
                return redirect('manager_home')
            else:
                return redirect('welcome')  # fallback

    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})




@login_required
def view_grades(request):
    return render(request, 'users/view_grades.html')





@login_required
def edit_student_profile(request):
    user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            return render(request, 'users/edit_student_profile.html', {'error': 'Incorrect current password'})

        if new_email:
            user.email = new_email

        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # ✅ כדי שהמשתמש לא יתנתק
            else:
                return render(request, 'users/edit_student_profile.html', {
                    'error': 'Passwords do not match'
                })
        else:
            user.save()

        return redirect('student_home')

    return render(request, 'users/edit_student_profile.html')



@login_required
def student_diary(request):
    events = StudentEvent.objects.filter(student=request.user).order_by('date')
    return render(request, 'users/student_diary.html', {'events': events})






 # ודא שייבאת את המודלים הרלוונטיים

# @login_required
# def student_home(request):
#     student = request.user.student  # מניח שיש קשר OneToOne בין User ל-Student

#     events = StudentEvent.objects.filter(student=student)
#     schedule = StudentSchedule.objects.filter(student__user=request.user).order_by('day', 'time')

#     return render(request, 'users/student_home.html', {
#         'events': events,
#         'schedule': schedule,
#     })




# views.py
# @login_required
# def add_lesson(request):
#     if not hasattr(request.user, 'teacher'):
#         return redirect('home')

#     if request.method == 'POST':
#         form = LessonForm(request.POST)
#         if form.is_valid():
#             lesson = form.save(commit=False)
#             lesson.teacher = request.user.teacher
#             lesson.save()
#             return redirect('teacher_home')
#     else:
#         form = LessonForm()

#     return render(request, 'users/add_lesson.html', {'form': form})


# users/views.py
from .forms import AddLessonForm

@login_required
def teacher_home(request):
    teacher = request.user.teacher
    form = AddLessonForm()

    if request.method == 'POST':
        form = AddLessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = teacher
            lesson.save()
            return redirect('teacher_home')  # מרענן את הדף

    schedule = StudentSchedule.objects.filter(teacher=teacher)

    return render(request, 'users/teacher_home.html', {
        'form': form,
        'schedule': schedule,
    })



@login_required
def send_message(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')
        recipient = User.objects.get(id=student_id)
        TeacherMessage.objects.create(
            sender=request.user,
            recipient=recipient,
            message=message
        )
        return redirect('teacher_home')  # או כל דף אחר שתרצה
    students = Student.objects.all()
    return render(request, 'users/send_message.html', {'students': students})

from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import TeacherProfileUpdateForm  # נטפל בזה עוד רגע

@login_required
def teacher_profile(request):
    teacher = request.user.teacher
    return render(request, 'users/teacher_profile.html', {'teacher': teacher})


from .models import StudentSchedule, Student, Teacher
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_lesson(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        day = request.POST.get('day')
        time = request.POST.get('time')

        try:
            student = Student.objects.get(id=student_id)
            teacher = request.user.teacher
            StudentSchedule.objects.create(
                student=student,
                teacher=teacher,
                subject=subject,
                day=day,
                time=time
            )
            messages.success(request, "Lesson added successfully!")
            return redirect('teacher_home')
        except Student.DoesNotExist:
            messages.error(request, "Student not found.")

    students = Student.objects.all()
    return render(request, 'users/add_lesson.html', {'students': students})

@login_required
def teacher_profile(request):
    user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            return render(request, 'users/teacher_profile.html', {'error': 'Incorrect current password'})

        if new_email:
            user.email = new_email

        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            else:
                return render(request, 'users/teacher_profile.html', {
                    'error': 'Passwords do not match'
                })

        user.save()
        return render(request, 'users/teacher_profile.html', {'success': 'Profile updated successfully'})

    return render(request, 'users/teacher_profile.html')


@login_required
def edit_teacher_profile(request):
    user = request.user

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(current_password):
            return render(request, 'users/edit_teacher_profile.html', {'error': 'Incorrect current password'})

        if new_email:
            user.email = new_email

        if new_password:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
            else:
                return render(request, 'users/edit_teacher_profile.html', {
                    'error': 'Passwords do not match'
                })
        else:
            user.save()

        return redirect('teacher_home')

    return render(request, 'users/edit_teacher_profile.html')





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, StudentSchedule, TeacherMessage
from django.utils import timezone

# @login_required
# def student_home(request):
#     try:
#         student = Student.objects.get(user=request.user)
#     except Student.DoesNotExist:
#         return redirect('login')

#     schedules = StudentSchedule.objects.filter(student=student)
#     today = timezone.now().date()
#     daily_events = StudentSchedule.objects.filter(student=student, date=today)

#     return render(request, 'users/student_home.html', {
#         'schedules': schedules,
#         'daily_events': daily_events,
#     })

# users/views.py


@login_required
def student_home(request):
    student = Student.objects.get(user=request.user)
    schedule = StudentSchedule.objects.filter(student=student)
    context = {
        'schedule': schedule,
        'student': student
    }
    return render(request, 'users/student_home.html', context)


# @login_required
# def student_messages(request):
#     student_user = request.user
#     messages = TeacherMessage.objects.filter(recipient=student_user).order_by('-sent_at')
#     return render(request, 'users/student_messages.html', {'messages': messages})

@login_required
def student_messages(request):
    student_user = request.user
    messages = TeacherMessage.objects.filter(recipient=student_user).order_by('-sent_at')
    return render(request, 'users/student_messages.html', {'messages': messages})

# users/views.py

from .models import Student

def view_students(request):
    students = Student.objects.all()
    return render(request, 'users/view_students.html', {'students': students})

@login_required
def teacher_messages(request):
    student_user = request.user
    messages = TeacherMessage.objects.filter(recipient=student_user).order_by('-sent_at')
    return render(request, 'users/teacher_messages.html', {'messages': messages})
