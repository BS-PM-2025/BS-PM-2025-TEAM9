from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone



class LearningLevel(models.Model):
    name = models.CharField(max_length=50)  # Beginner / Intermediate / Advanced
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