from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import student_messages, teacher_messages




urlpatterns = [
    path('', views.welcome, name='welcome'),  # ✅ this is the homepage
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.root_redirect),
    path('', views.welcome, name='welcome'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('home/student/', views.student_home, name='student_home'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
    path('signup/manager/', views.manager_signup, name='manager_signup'),
    path('home/manager/', views.manager_home, name='manager_home'),
    path('login/', views.login_view, name='login'),  # 👈 use your view
    path('signup/', views.signup, name='signup'),
    path('', views.welcome, name='welcome'),
    path('grades/', views.view_grades, name='view_grades'),
    path('messages/', views.student_messages, name='messages'), 
    path('student/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('homework-by-date/', views.get_homework_by_date, name='homework_by_date'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher/add_lesson/', views.add_lesson, name='add_lesson'),
    path('teacher/edit/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('student/messages/', student_messages, name='student_messages'),
    path('student/messages/', views.student_messages, name='student_messages'),
    path('student/messages/', student_messages, name='student_messages'),
    path('students/', views.view_students, name='view_students'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),
    path('teacher/messages/', views.teacher_messages, name='teacher_messages'),










]












