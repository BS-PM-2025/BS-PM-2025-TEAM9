from django.contrib import admin
from .models import Student, Teacher, Manager
from .models import StudentSchedule
from .models import TeacherMessage

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Manager)
admin.site.register(StudentSchedule)
admin.site.register(TeacherMessage)


