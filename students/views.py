from .models import Student, Performance, Attendance,Course
from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Avg, Sum, Case, When, FloatField,IntegerField
from django.http import JsonResponse


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




def dashboard_data(request):
    # 1️⃣ Total marks per student
    total_marks_qs = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(total_marks=Sum("marks"))
    total_marks = list(total_marks_qs)

    # 2️⃣ Top 5
    top_five_qs = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(total_marks=Sum("marks")).order_by('-total_marks')[:5]
    top_five_stu = list(top_five_qs)

    # 3️⃣ Bottom 5
    bottom_five = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(total_marks=Sum("marks")).order_by('total_marks')[:5]
    bottom_five_stu = list(bottom_five)

    # 4️⃣ Pass/Fail (<50%)
    fail_rate = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(
        total_marks=Sum("marks")
    ).annotate(
        fail=Case(
            When(total_marks__lt=50, then=1),
            default=0,
            output_field=IntegerField()
        )
    )

    fail_rate_status = [
        {
            "student_id": stu["student_id"],
            "student_name": stu["student__name"],
            "total_marks": stu["total_marks"],
            "status": "fail" if stu["fail"] == 1 else "passed"
        }
        for stu in fail_rate
    ]

    # 5️⃣ Low attendance (<75%)
    low_attendance_qs = Attendance.objects.values(
        "student_id",
        "student__name"
    ).annotate(
        att=Avg(
            Case(
                When(status='Present', then=1),
                When(status='Absent', then=0),
                output_field=FloatField()
            )
        ) * 100
    ).filter(att__lt=75)

    low_attendance = list(low_attendance_qs)

    return JsonResponse({
        "total_marks": total_marks,
        "top_five_stu": top_five_stu,
        "bottom_five_stu": bottom_five_stu,
        "fail_rate_status_details": fail_rate_status,
        "low_attendance": low_attendance,
    })


def pass_fail_chart_page(request):
    return render(request, "students/dashoard-data1.html")
