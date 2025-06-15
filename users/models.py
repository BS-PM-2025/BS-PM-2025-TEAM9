from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.utils import timezone


class LearningLevel(models.Model):
    class LevelType(models.TextChoices):
        BEGINNER = 'beginner', 'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED = 'advanced', 'Advanced'

    name = models.CharField(max_length=20, choices=LevelType.choices, default=LevelType.BEGINNER) # Beginner / Intermediate / Advanced
    description = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    learning_level = models.ForeignKey(LearningLevel, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# ---------------------------

class StudentEvent(models.Model):
    EVENT_TYPES = [
        ('lesson', 'Lesson'),
        ('homework', 'Homework'),
        ('exam', 'Exam'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # ✅ תיקון חשוב!
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateField()
    date = models.DateField(default=timezone.now)


    def __str__(self):
        return f"{self.title} - {self.event_type} on {self.date}"
    
# class StudentSchedule(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     day = models.CharField(max_length=10, choices=[
#         ('Sunday', 'Sunday'),
#         ('Monday', 'Monday'),
#         ('Tuesday', 'Tuesday'),
#         ('Wednesday', 'Wednesday'),
#         ('Thursday', 'Thursday')
#     ])
#     time = models.TimeField()
#     subject = models.CharField(max_length=100)

#     # 🆕 הוסף את זה:
#     date = models.DateField(null=True, blank=True)  # אפשרי להשאיר ריק בשלב ראשון

class StudentSchedule(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=[
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday')
    ])
    time = models.TimeField()
    subject = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)  



class TeacherMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# ----------------- Course/Assignments Models ------------------ #

# Course Model
class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    learning_level = models.ForeignKey(LearningLevel, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.title

class CourseSection(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class SectionContent(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('file', 'File'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('assignment', 'Assignment'),
        ('link', 'External Link'),
    ]
    
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='contents')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    title = models.CharField(max_length=100)
    text_content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='course_contents/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio_contents/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)
    assignment_instructions = models.TextField(blank=True, null=True)
    assignment_due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.section.title} - {self.title}"

    def save(self, *args, **kwargs):
        # Ensure assignment fields are null for non-assignment content
        if self.content_type != 'assignment':
            self.assignment_instructions = None
            self.assignment_due_date = None
        super().save(*args, **kwargs)

# Student-Course Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def clean(self):
        if self.student.learning_level != self.course.learning_level:
            raise ValidationError("Student's learning level does not match the course level.")

    def __str__(self):
        return f"{self.student} in {self.course}"

class Assignment(models.Model):
    content = models.OneToOneField(SectionContent, on_delete=models.CASCADE, related_name='assignment', null=True, blank=True)
    deadline = models.DateTimeField()
    max_points = models.PositiveIntegerField(default=100)
    allow_late_submissions = models.BooleanField(default=False)
    submission_types = models.CharField(
        max_length=20,
        choices=[('file', 'File'), ('text', 'Text'), ('both', 'File or Text')],
        default='both'
    )
    rubric = models.JSONField(blank=True, null=True)  # For advanced grading
    
    def __str__(self):
        return f"{self.content.title} (Due: {self.deadline})"

    def save(self, *args, **kwargs):
        # Ensure the linked content is actually an assignment
        if self.content.content_type != 'assignment':
            raise ValueError("Cannot create Assignment for non-assignment content")
        super().save(*args, **kwargs)

    @property
    def percent_graded(self):
        total = self.submissions.count()
        if total == 0:
            return 0
        return (self.submissions.filter(status='graded').count() / total) * 100

    @property
    def percent_submitted(self):
        total_enrollments = self.content.section.course.enrollments.count()
        if total_enrollments == 0:
            return 0
        return (self.submissions.count() / total_enrollments) * 100

    @property
    def graded_count(self):
        return self.submissions.filter(status='graded').count()

    @property
    def submitted_count(self):
        return self.submissions.count()
    
    def get_student_submission(self, student):
        """Helper method to get a student's submission"""
        try:
            return self.submissions.get(student=student)
        except Submission.DoesNotExist:
            return None

class Submission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('late', 'Submitted Late'),
        ('graded', 'Graded'),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='users/submissions/%Y/%m/%d/')
    submission_text = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    grade = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    teacher_notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']


    def save(self, *args, **kwargs):
        now = timezone.now()

        # Automatically set status based on conditions
        if self.grade is not None:
            self.status = 'graded'
        elif self.submitted_file or self.submission_text:
            if self.assignment.deadline and now > self.assignment.deadline:
                self.status = 'late'
            else:
                self.status = 'submitted'
        else:
            self.status = 'draft'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student}'s submission for {self.assignment}"

    def is_late(self):
        return self.submitted_at > self.assignment.deadline
    
    @property
    def points_percentage(self):
        """Calculate percentage score if graded"""
        if self.grade is not None and self.assignment.max_points > 0:
            return (self.grade / self.assignment.max_points) * 100
        return None
# users/models.py

class LessonRecord(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='lesson_records/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
# models.py

class TimelineUpload(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='timelines/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.user.username} - {self.title}"

# models.py
class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='course_materials/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField()


from django.db import models
from django.contrib.auth.models import User

class EmailMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_emails', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_emails', on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.sent_at}"


    


class TeacherBio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    

from django.utils import timezone

class Submission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('late', 'Submitted Late'),
        ('graded', 'Graded'),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_file = models.FileField(upload_to='submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    grade = models.PositiveIntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    teacher_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        now = timezone.now()

        # Automatically determine the status
        if self.grade is not None:
            self.status = 'graded'
        elif self.submitted_file:
            if self.assignment.deadline and now > self.assignment.deadline:
                self.status = 'late'
            else:
                self.status = 'submitted'
        else:
            self.status = 'draft'

        super().save(*args, **kwargs)

    @property
    def is_late(self):
        return self.assignment.deadline and self.submitted_at > self.assignment.deadline

    @property
    def points_percentage(self):
        if self.grade is not None and self.assignment.max_points > 0:
            return (self.grade / self.assignment.max_points) * 100
        return None

    def __str__(self):
        return f"{self.student}'s submission for {self.assignment}"