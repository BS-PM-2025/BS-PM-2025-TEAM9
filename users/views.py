from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CourseForm, CourseSectionForm, SectionContentForm, SubmissionForm, UserForm, StudentSignupForm, TeacherSignupForm, ManagerSignupForm, StudentProfileUpdateForm
from .models import Assignment, Course, CourseMaterial, CourseSection, Enrollment, LearningLevel, SectionContent, Student, Submission, Teacher, Manager, StudentEvent, StudentSchedule, TeacherMessage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.dateformat import format
from django.http import JsonResponse
from .models import Message
from django.db.models import Prefetch 
from .models import LessonRecord, Course
from django.contrib import messages


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

def student_dashboard(request):
    user = request.user

    # הודעות לסטודנט
    messages = Message.objects.filter(receiver=user).order_by('-timestamp')

    # הבאת האובייקט של הסטודנט + רמת הלימוד שלו
    student = get_object_or_404(Student, user=user)
    level = student.learning_level  # זה אובייקט מסוג LearningLevel

    return render(request, 'student_dashboard.html', {
        'messages': messages,
        'student': student,
        'level': level,
    })
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


from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, StudentSchedule, Enrollment, Assignment, Submission, Message, LearningLevel

@login_required
def student_home(request):
    # Get student profile and learning level
    student = Student.objects.get(user=request.user)
    level = student.learning_level
    
    # Get student's schedule
    schedule = StudentSchedule.objects.filter(student=student)
    
    # Get student's enrollments with related course data
    enrollments = Enrollment.objects.filter(student=student).select_related('course', 'course__teacher')
    # Get assignments from enrolled courses
    enrolled_course_ids = enrollments.values_list('course_id', flat=True)
    

    # Get recent assignments (due in next 7 days or recently past due)
    recent_assignments = []
    # courses = Course.objects.filter(learning_level=level)
    
    assignments = Assignment.objects.filter(
        content__section__course_id__in=enrolled_course_ids
    ).select_related(
        'content', 'content__section', 'content__section__course'
    ).order_by('deadline')[:5]  # Limit to 5 most relevant
    
    # Add submission status to each assignment
    for assignment in assignments:
        submission = Submission.objects.filter(
            assignment=assignment,
            student=student
        ).first()
        recent_assignments.append({
            'id': assignment.id,
            'content': assignment.content,
            'deadline': assignment.deadline,
            'is_past_due': assignment.deadline < timezone.now(),
            'submission': submission
        })
    
    # Get recent messages
    recent_messages = Message.objects.filter(
        sender=request.user
    ).order_by('-timestamp')[:3]
    
    context = {
        'schedule': schedule,
        'enrollments': enrollments,
        'student': student,
        'level': level,
        'recent_assignments': recent_assignments,
        'messages': recent_messages
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




# --------------------- Course Views ---------------------------- #
@login_required
def teacher_courses(request):
    try:
        if not request.user.is_authenticated or not hasattr(request.user, 'teacher'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        courses = Course.objects.filter(teacher=request.user.teacher)
        levels = LearningLevel.objects.all()
        
        return render(request, 'users/teacher_courses.html', {
            'courses': courses,
            'levels': levels,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        
@login_required
def create_course(request):
    try:
        if not request.user.is_authenticated or not hasattr(request.user, 'teacher'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.teacher = request.user.teacher
                course.save()
                messages.success(request, 'Course created successfully!')
                return redirect('teacher_courses')
        else:
            form = CourseForm()
        
        return render(request, 'users/create_course.html', {'form': form})
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
      
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if teacher owns the course or student is in this level
    if not request.user.is_authenticated or not hasattr(request.user, 'teacher'):
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if not (
        hasattr(request.user, 'teacher') and request.user.teacher == course.teacher or
        hasattr(request.user, 'student') and 
        request.user.student.learning_level == course.learning_level
    ):
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    sections = course.sections.all().prefetch_related('contents')
    
    return render(request, 'users/course_detail.html', {
        'course': course,
        'sections': sections,
        'is_teacher': request.user.teacher == course.teacher,
    })

@login_required
def add_section(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user.teacher != course.teacher:
        return redirect('home')
    
    if request.method == 'POST':
        form = CourseSectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.course = course
            section.save()
            messages.success(request, 'Section added successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseSectionForm()
    
    return render(request, 'users/add_section.html', {
        'form': form,
        'course': course,
    })
@login_required
def add_content(request, section_id):
    section = get_object_or_404(CourseSection, id=section_id)
    
    if request.user.teacher != section.course.teacher:
        return redirect('home')
    
    if request.method == 'POST':
        form = SectionContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.section = section
            content.save()
            
            if content.content_type == 'assignment':
                # Use get_or_create to prevent duplicates
                Assignment.objects.get_or_create(
                    content=content,
                    defaults={
                        'deadline': content.assignment_due_date,
                        'max_points': 100
                    }
                )
                messages.success(request, 'Assignment content processed successfully!')
            else:
                messages.success(request, 'Content added successfully!')
                
            return redirect('course_detail', course_id=section.course.id)
    else:
        form = SectionContentForm()
    
    return render(request, 'users/add_content.html', {
        'form': form,
        'section': section,
    })
    
@login_required
def edit_content(request, content_id):
    content = get_object_or_404(SectionContent, id=content_id)
    
    if request.user.teacher != content.section.course.teacher:
        return redirect('home')
    
    if request.method == 'POST':
        form = SectionContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Content updated successfully!')
            return redirect('course_detail', course_id=content.section.course.id)
    else:
        form = SectionContentForm(instance=content)
    
    return render(request, 'users/edit_content.html', {
        'form': form,
        'content': content,
    })

@login_required
def delete_content(request, content_id):
    content = get_object_or_404(SectionContent, id=content_id)
    
    if request.user.teacher != content.section.course.teacher:
        return redirect('home')
    
    course_id = content.section.course.id
    content.delete()
    messages.success(request, 'Content deleted successfully!')
    return redirect('course_detail', course_id=course_id)

@login_required
def assignment_list(request):
    # Get all courses the student is enrolled in
    enrollments = Enrollment.objects.filter(student=request.user.student)
    courses = [e.course for e in enrollments]
    
    # Get all assignments from these courses
    assignments = Assignment.objects.filter(content__section__course__in=courses).select_related(
        'content', 'content__section', 'content__section__course'
    ).order_by('deadline')
    
    # Check submission status for each assignment
    assignments_with_status = []
    for assignment in assignments:
        submission = Submission.objects.filter(
            assignment=assignment, 
            student=request.user.student
        ).first()
        
        assignments_with_status.append({
            'assignment': assignment,
            'submission': submission,
            'is_past_due': assignment.deadline < timezone.now()
        })
    
    return render(request, 'users/assignment_list.html', {
        'assignments': assignments_with_status
    })

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student
    
    # Check if student is enrolled in the course
    if not Enrollment.objects.filter(student=student, course=assignment.content.section.course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('assignment_list')
    
    submission = Submission.objects.filter(assignment=assignment, student=student).first()
    form = None
    
    if request.method == 'POST':
        # If submission already exists, show error
        if submission:
            messages.error(request, "You have already submitted this assignment.")
        else:
            form = SubmissionForm(request.POST, request.FILES)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.assignment = assignment
                submission.student = student
                submission.save()
                messages.success(request, "Assignment submitted successfully!")
                return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        if not submission:
            form = SubmissionForm()
    
    return render(request, 'student/assignment_detail.html', {
        'assignment': assignment,
        'submission': submission,
        'form': form,
        'is_past_due': assignment.deadline < timezone.now()
    })

@login_required
def view_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    
    # Check if the student owns this submission
    if submission.student.user != request.user:
        messages.error(request, "You don't have permission to view this submission.")
        return redirect('assignment_list')
    
    return render(request, 'student/view_submission.html', {
        'submission': submission
    })

# views.py
@login_required
def course_content(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    
    # Check if student is enrolled in the course
    if not Enrollment.objects.filter(student=student, course=course).exists():
        messages.error(request, "You are not enrolled in this course.")
        return redirect('student_home')
    
    # Get all sections and their contents
    sections = course.sections.all().prefetch_related('contents')
    
    return render(request, 'users/course_content.html', {
        'course': course,
        'sections': sections
    })


@login_required
def course_list(request):
    student = request.user.student
    # Get courses matching student's learning level that they're not enrolled in
    available_courses = Course.objects.filter(
        learning_level=student.learning_level
    )
    # .exclude(
    #     enrollment__student=student
    # ).select_related('teacher', 'learning_level')
    
    # Get courses the student is already enrolled in
    enrolled_courses = Enrollment.objects.filter(
        student=student
    )
    # Search functionality
  
    context = {
        'available_courses': available_courses,
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'users/course_list.html', context)

@login_required
def student_course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = request.user.student
    
    # Check if student is already enrolled
    is_enrolled = Enrollment.objects.filter(
        student=student, 
        course=course
    ).exists()
    
    # Check if course matches student's learning level
    level_match = course.learning_level == student.learning_level
    
    if request.method == 'POST':
        if not level_match:
            messages.error(request, "This course doesn't match your current learning level.")
            return redirect('course_list')
        
        if is_enrolled:
            messages.warning(request, "You're already enrolled in this course.")
            return redirect('course_detail', course_id=course.id)
        
        # Create enrollment
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, f"Successfully enrolled in {course.title}!")
        return redirect('student_course_content', course_id=course.id)
    
    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'can_enroll': level_match and not is_enrolled
    }
    return render(request, 'users/course_detail.html', context)

@login_required
def unenroll_course(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        student = request.user.student
        
        enrollment = Enrollment.objects.filter(
            student=student,
            course=course
        ).first()
        
        if enrollment:
            enrollment.delete()
            messages.success(request, f"You've been unenrolled from {course.title}.")
        else:
            messages.error(request, "You're not enrolled in this course.")
        
        return redirect('course_list')
    
    return redirect('student_home')

@login_required
def student_course_content(request, course_id):
    student = getattr(request.user, 'student', None)
    if not student:
        return redirect('student_home')

    course = get_object_or_404(Course, id=course_id)

    if not Enrollment.objects.filter(student=student, course=course).exists():
        return redirect('student_home')

    sections = course.sections.prefetch_related(
        Prefetch('contents', queryset=SectionContent.objects.select_related('assignment'))
    )

    # Get all submissions for this course in one query
    submissions = Submission.objects.filter(
        student=student,
        assignment__content__section__course=course
    ).select_related('assignment')

    submission_map = {sub.assignment_id: sub for sub in submissions}

    return render(request, 'users/course_content.html', {
        'course': course,
        'sections': sections,
        'current_time': timezone.now(),
        'submission_map': submission_map,  # Pass the map to template
    })


@login_required
def submit_assignment(request):
    if request.method == 'POST':
        assignment_id = request.POST.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        student = request.user.student
        
        if Submission.objects.filter(assignment=assignment, student=student).exists():
            return JsonResponse({'success': False, 'message': 'You have already submitted this assignment'})
        
        submitted_file = request.FILES.get('submitted_file')
        submission_text = request.POST.get('submission_text', '').strip()
        
        if not (submitted_file or submission_text):
            return JsonResponse({'success': False, 'message': 'You must provide either a file or text submission'})
        
        Submission.objects.create(
            assignment=assignment,
            student=student,
            submitted_file=submitted_file,
            submission_text=submission_text
        )
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Enrollment, LessonRecord, SectionContent

@login_required
def student_all_course_materials(request):
    student = request.user.student
    enrollments = Enrollment.objects.filter(student=student).select_related('course')
    course_ids = enrollments.values_list('course__id', flat=True)

    records = LessonRecord.objects.filter(course__id__in=course_ids)
    contents = SectionContent.objects.filter(section__course__id__in=course_ids)

    return render(request, 'users/student_course_materials.html', {
        'enrollments': enrollments,
        'records': records,
        'contents': contents,
    } )

@login_required
def upload_lesson_record(request):
    from .forms import LessonRecordForm
    teacher = request.user.teacher
    if request.method == 'POST':
        form = LessonRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.teacher = teacher
            record.save()
            messages.success(request, "Lesson record uploaded successfully!")
            return redirect('teacher_home')
    else:
        form = LessonRecordForm()

    return render(request, 'users/upload_lesson_record.html', {'form': form})

@login_required
def view_lesson_records(request):
    teacher = request.user.teacher
    records = LessonRecord.objects.filter(teacher=teacher)
    return render(request, 'users/view_lesson_records.html', {'records': records})


# users/views.py

# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TimelineUploadForm  # אם יש טופס מתאים

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course  # אם יש קשר לקורסים

@login_required
def upload_timeline(request):
    return render(request, 'users/upload_timeline.html')  # צור קובץ HTML מתאים
@login_required
def upload_timeline(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('timeline_file')
        timeline_url = request.POST.get('timeline_url')
        course_id = request.GET.get('course_id')

        if not course_id:
            return HttpResponseBadRequest("Missing course ID")

        course = get_object_or_404(Course, id=course_id)

        # תהליך שמירה
        if uploaded_file:
            LessonRecord.objects.create(
                teacher=request.user.teacher,
                course=course,
                title="Timeline File",
                file=uploaded_file
            )
        elif timeline_url:
            SectionContent.objects.create(
                section=course.sections.first(),  # או לפי בחירה
                content_type='link',
                title="Timeline URL",
                external_link=timeline_url
            )
        else:
            messages.error(request, "Please upload a file or provide a URL.")
            return redirect('upload_timeline')  # אפשר גם לשלוח את ה-course_id

        messages.success(request, "Timeline uploaded successfully!")
        return redirect('course_detail', course_id=course.id)

    return render(request, 'users/upload_timeline.html')



@login_required
def upload_recording(request):
    return render(request, 'users/upload_recording.html')  # צור את הקובץ הזה בתיקיית templates/users

@login_required
def upload_recording(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        course_id = request.POST.get('course_id')
        uploaded_file = request.FILES.get('file')

        if not uploaded_file or not course_id:
            messages.error(request, 'Missing file or course.')
            return redirect('upload_recording')

        course = Course.objects.get(id=course_id)
        teacher = request.user.teacher

        LessonRecord.objects.create(
            teacher=teacher,
            course=course,
            title=title,
            file=uploaded_file
        )

        messages.success(request, 'Recording uploaded successfully!')
        return redirect('teacher_home')

    courses = Course.objects.filter(teacher=request.user.teacher)
    return render(request, 'users/upload_recording.html', {'courses': courses})

from .models import LessonRecord, Course
from .forms import SectionContentForm  # או טופס אחר שתשתמש בו
from django.contrib import messages

@login_required
def upload_material(request):
    if not hasattr(request.user, 'teacher'):
        return redirect('login')

    if request.method == 'POST':
        form = SectionContentForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.section = None  # אם אתה לא מקשר לסקשן ספציפי
            material.save()
            messages.success(request, "Material uploaded successfully!")
            return redirect('teacher_home')
    else:
        form = SectionContentForm()

    return render(request, 'users/upload_material.html', {'form': form})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sections = course.sections.prefetch_related('contents')

    # כל הקבצים בקורס הזה לפי הרמה
    level = course.learning_level
    contents = SectionContent.objects.filter(section__course__learning_level=level)

    return render(request, 'users/course_detail.html', {
        'course': course,
        'sections': sections,
        'level_contents': contents
    })


def view_lesson_records(request):
    return render(request, 'users/view_lesson_records.html')


