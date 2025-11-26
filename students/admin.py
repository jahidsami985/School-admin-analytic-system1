from django.contrib import admin
from .models import Department, Student, Course, Teacher, Performance, Attendance

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(Performance)
admin.site.register(Attendance)

