from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Enrollment, Student, Submission, Teacher, Manager,  StudentEvent

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


# ------------------------- Course Forms --------------------------- #

from .models import Course, CourseSection, SectionContent

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'learning_level']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CourseSectionForm(forms.ModelForm):
    class Meta:
        model = CourseSection
        fields = ['title', 'order']

class SectionContentForm(forms.ModelForm):
    class Meta:
        model = SectionContent
        fields = [
            'content_type', 'title', 'text_content', 'file', 
            'video_url', 'audio_file', 'external_link',
            'assignment_instructions', 'assignment_due_date', 'order'
        ]
        widgets = {
            'text_content': forms.Textarea(attrs={'rows': 4}),
            'assignment_instructions': forms.Textarea(attrs={'rows': 4}),
            'assignment_due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make fields required/not required based on content_type
        content_type = self.data.get('content_type') if self.data else self.instance.content_type if self.instance else None
        
        if content_type:
            for field_name in self.fields:
                if field_name not in ['content_type', 'title', 'order']:
                    self.fields[field_name].required = False
            
            if content_type == 'text':
                self.fields['text_content'].required = True
            elif content_type == 'file':
                self.fields['file'].required = True
            elif content_type == 'video':
                self.fields['video_url'].required = True
            elif content_type == 'audio':
                self.fields['audio_file'].required = True
            elif content_type == 'assignment':
                self.fields['assignment_instructions'].required = True
            elif content_type == 'link':
                self.fields['external_link'].required = True

    def clean(self):
        cleaned_data = super().clean()
        content_type = cleaned_data.get('content_type')
        
        if content_type == 'assignment':
            if not cleaned_data.get('assignment_instructions'):
                self.add_error('assignment_instructions', 'Instructions are required for assignments')
            if not cleaned_data.get('assignment_due_date'):
                self.add_error('assignment_due_date', 'Due date is required for assignments')
        else:
            # Clear assignment-related fields if not an assignment
            cleaned_data['assignment_instructions'] = None
            cleaned_data['assignment_due_date'] = None
            
        return cleaned_data

# class SubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['submitted_file', 'submission_text']
#         widgets = {
#             'submission_text': forms.Textarea(attrs={'rows': 10}),
#         }
#         labels = {
#             'submitted_file': 'Upload your work',
#             'submission_text': 'Or write your submission here'
#         }

#         def clean(self):
#             cleaned_data = super().clean()
#             submitted_file = cleaned_data.get('submitted_file')
#             submission_text = cleaned_data.get('submission_text')
            
#             # Validate at least one submission method is provided
#             if not submitted_file and not submission_text:
#                 raise forms.ValidationError("You must provide either a file or text submission.")
            
#             return cleaned_data

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [] 


# forms.py

# class GradeSubmissionForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['grade', 'feedback', 'teacher_notes']
#         widgets = {
#             'feedback': forms.Textarea(attrs={'rows': 5}),
#             'teacher_notes': forms.Textarea(attrs={'rows': 3}),
#         }
    
#     def clean_grade(self):
#         grade = self.cleaned_data['grade']
#         max_points = self.instance.assignment.max_points
        
#         if grade is not None and grade > max_points:
#             raise forms.ValidationError(f"Grade cannot exceed maximum points ({max_points})")
        
#         return grade
    
    
# class SubmitAssignmentForm(forms.ModelForm):
#     class Meta:
#         model = Submission
#         fields = ['submitted_file', 'submission_text']
#         widgets = {
#             'submission_text': forms.Textarea(attrs={
#                 'rows': 10,
#                 'placeholder': 'Type your submission here...'
#             }),
#         }
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         assignment = kwargs.get('instance').assignment if kwargs.get('instance') else None
        
#         if assignment:
#             if assignment.submission_types == 'file':
#                 self.fields['submission_text'].widget = forms.HiddenInput()
#             elif assignment.submission_types == 'text':
#                 self.fields['submitted_file'].widget = forms.HiddenInput()
    
#     def clean(self):
#         cleaned_data = super().clean()
#         submitted_file = cleaned_data.get('submitted_file')
#         submission_text = cleaned_data.get('submission_text', '').strip()
        
#         if not submitted_file and not submission_text:
#             raise forms.ValidationError("You must provide either a file or text submission.")
        
#         return cleaned_data

        
from .models import LessonRecord

class LessonRecordForm(forms.ModelForm):
    class Meta:
        model = LessonRecord
        fields = ['course', 'title', 'file']

# forms.py


from .models import TimelineUpload  # תוודא שקיים מודל כזה

class TimelineUploadForm(forms.ModelForm):
    class Meta:
        model = TimelineUpload
        fields = ['title', 'file']


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']  # במקום ['submission_text']

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']  # רק שדות שבאמת קיימים

class SubmitAssignmentForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submitted_file']  # ✅ רק שדה שקיים באמת במודל
