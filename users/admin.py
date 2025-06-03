from django.contrib import admin
from .models import * 


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Manager)
admin.site.register(StudentSchedule)
admin.site.register(TeacherMessage)
admin.site.register(LearningLevel)


