from django.urls import path
from . import views

urlpatterns = [
    path('', views.root_redirect),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('home/student/', views.student_home, name='student_home'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),


]
