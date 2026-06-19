from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"
    

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=50)
    roll_num = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class Course(models.Model):
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=100)

    department=models.ForeignKey(Department,on_delete=models.CASCADE)
        
    def __str__(self):
            return f"{self.name} ({self.code})"
    
    class Meta:
        ordering=["name"]

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def email(self):
        return self.user.email if self.user else ""
    

class Performance(models.Model):
    marks = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.FloatField(default=0) 

    def __str__(self):
        return f"{self.student.name} - {self.course.name}: {self.grade} ({self.marks})"

    class Meta:
        db_table = "Performance"
        ordering = ['-grade', '-marks']


class Attendance(models.Model):
    PRESENT = "P"
    ABSENT = "A"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
    ]

    date = models.DateField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=ABSENT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name} - {self.date}: {self.get_status_display()}"
    
    class Meta:
        ordering = ['date', 'status']
