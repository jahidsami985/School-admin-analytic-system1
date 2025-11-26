from .models import Student, Performance, Attendance,Course
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm, StudentFormSet,AttendanceForm,AttendanceFormSet,PerformanceForm,PerformanceFormSet


def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student.html", {"data": students})


def home(request):
    return render(request, "home.html")


def student_perform(request):
    student_performance = Performance.objects.all()
    return render(request, "students/performance.html", {"data": student_performance})


def student_attandance(request):
    atten_stu = Attendance.objects.all()
    return render(request, "students/attendance.html", {"data": atten_stu})


def manage_students(request):
    if request.method == 'POST':
        formset = StudentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = StudentFormSet(queryset=Student.objects.all())

    return render(request, "students/manage_students.html", {"formset": formset})


def edit_student_info(request):
    if request.method == "POST":
        formset = StudentFormSet(request.POST, queryset=Student.objects.all())

        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = StudentFormSet(queryset=Student.objects.all())

    return render(request, "students/manage_students.html", {"formset": formset})


def edit_attendance_info(request):
    if request.method == "POST":
        formset =AttendanceFormSet(request.POST, queryset=Attendance.objects.all())

        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = AttendanceFormSet(queryset=Attendance.objects.all())

    return render(request, "students/edit_att.html", {"formset": formset})
def edit_performance(request):
    queryset = Performance.objects.all()  # optionally filter by course

    if request.method == "POST":
        formset = PerformanceFormSet(request.POST, queryset=queryset)
        if formset.is_valid():
            formset.save()
            return redirect("edit_performance")
        else:
            # Print errors for debugging
            print(formset.errors)
    else:
        formset = PerformanceFormSet(queryset=queryset)

    return render(request, "students/performance_edit.html", {"formset": formset})