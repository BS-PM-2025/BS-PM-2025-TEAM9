from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # דפי קורסים ומערכי שיעור - Teacher
    path('courses/', views.teacher_courses, name='teacher_courses'),
    path('courses/create/', views.create_course, name='create_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/add-section/', views.add_section, name='add_section'),
    path('sections/<int:section_id>/add-content/', views.add_content, name='add_content'),
    path('contents/<int:content_id>/edit/', views.edit_content, name='edit_content'),
    path('contents/<int:content_id>/delete/', views.delete_content, name='delete_content'),
    path('teacher/upload-timeline/', views.upload_timeline, name='upload_timeline'),
    path('teacher/upload-recording/', views.upload_recording, name='upload_recording'),
    path('lesson-records/', views.view_lesson_records, name='view_lesson_records'),
     path('assignment/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
     path('assignment/<int:assignment_id>/submition/', views.assignment_submissions, name='assignment_submissions'),
     path('assignment/<int:assignment_id>/submition/', views.download_submissions, name='download_submissions'),
    path('submission/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('course/<int:course_id>/grades/', views.view_grades, name='view_grades'),




    # Assignments
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/submit', views.submit_assignment, name='submit_assignment'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('submissions/<int:submission_id>/', views.view_submission, name='view_submission'),

    # סטודנט - קורסים
    path('student/courses/', views.course_list, name='course_list'),
    path('student/course/<int:course_id>/', views.student_course_detail, name='student_course_detail'),
    path('student/course-content/<int:course_id>/', views.student_course_content, name='student_course_content'),
    path('student/courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),

    # חומרי לימוד והקלטות
    path('course-materials/', views.student_all_course_materials, name='student_course_materials'),
    path('student/materials/', views.student_all_course_materials, name='student_all_course_materials'),
    path('teacher/upload-material/', views.upload_material, name='upload_material'),

    # דפים כלליים
    path('', views.welcome, name='welcome'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),

    # התחברות/יציאה
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # הרשמה
    path('signup/', views.signup, name='signup'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('signup/manager/', views.manager_signup, name='manager_signup'),

    # דפי בית
    path('home/student/', views.student_home, name='student_home'),
    path('home/teacher/', views.teacher_home, name='teacher_home'),
    path('home/manager/', views.manager_home, name='manager_home'),

    # ניהול פרופיל
    path('student/edit/', views.edit_student_profile, name='edit_student_profile'),
    path('teacher/profile/', views.teacher_profile, name='teacher_profile'),
    path('teacher/edit/', views.edit_teacher_profile, name='edit_teacher_profile'),
    #מנהל מעדכן משתמשים
    path('manager/users/', views.manage_users, name='manage_users'),
    path('manager/users/<int:user_id>/update_level/', views.update_user_level, name='update_user_level'),
    path('manager/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),


    # הודעות
    path('student/messages/', views.student_messages, name='student_messages'),
    path('teacher/messages/', views.teacher_messages, name='teacher_messages'),

    # ניהול לוח זמנים / שיעורים
    path('homework-by-date/', views.get_homework_by_date, name='homework_by_date'),
    path('teacher/add_lesson/', views.add_lesson, name='add_lesson'),

    # ניהול תלמידים
    path('students/', views.view_students, name='view_students'),

    # לוחות / ציונים
    path('grades/', views.all_my_submissions, name='view_grades'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    # ⚠️ אדמין
    path('admin/', admin.site.urls),
]
