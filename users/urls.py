from django.urls import path
from . import views

urlpatterns = [
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('home/student/', views.student_home, name='student_home'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),

]
