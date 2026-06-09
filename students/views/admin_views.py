from students.models import Student, Performance, Attendance, Course

from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import Avg, Sum, Case, When, FloatField, IntegerField
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
import json
from django.conf import settings
from pathlib import Path

from students.forms import StudentForm, StudentFormSet, AttendanceForm, AttendanceFormSet, PerformanceForm, PerformanceFormSet

@staff_member_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "students/student.html", {"data": students})


def home(request):
    return render(request, "register1/home.html")

@staff_member_required
def student_perform(request):
    student_performance = Performance.objects.all()
    return render(request, "students/performance.html", {"data": student_performance})

@staff_member_required
def student_attandance(request):
    atten_stu = Attendance.objects.all()
    return render(request, "students/attendance.html", {"data": atten_stu})
@staff_member_required

def manage_students(request):
    if request.method == 'POST':
        formset = StudentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = StudentFormSet(queryset=Student.objects.all())

    return render(request, "students/manage_students.html", {"formset": formset})

@staff_member_required
def edit_student_info(request):
    if request.method == "POST":
        formset = StudentFormSet(request.POST, queryset=Student.objects.all())

        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = StudentFormSet(queryset=Student.objects.all())

    return render(request, "students/manage_students.html", {"formset": formset})

@staff_member_required
def edit_attendance_info(request):
    if request.method == "POST":
        formset = AttendanceFormSet(request.POST, queryset=Attendance.objects.all())

        if formset.is_valid():
            formset.save()
            return redirect("manage_students")
    else:
        formset = AttendanceFormSet(queryset=Attendance.objects.all())

    return render(request, "students/edit_att.html", {"formset": formset})

@staff_member_required
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


@login_required

def dashboard_data(request):
    # 1️⃣ Total marks per student
    # marks is stored as CharField in the model; cast to Float for numeric aggregation
    total_marks_qs = Performance.objects.values(
        "student_id",
        "student__name",
        "student__department__id",
        "student__department__name"
    ).annotate(total_marks=Sum(Cast("marks", FloatField())))
    total_marks = list(total_marks_qs)

    # 2️⃣ Top 5 (FIXED: Added missing comma and correct FK lookup)
    top_five_qs = Performance.objects.values(
        "student_id",
        "student__name",
        "student__department__id",
        "student__department__name"
    ).annotate(total_marks=Sum(Cast("marks", FloatField()))).order_by('-total_marks')[:5]
    top_five_stu = list(top_five_qs)

    # 3️⃣ Bottom 5
    bottom_five = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(total_marks=Sum(Cast("marks", FloatField()))).order_by('total_marks')[:5]
    bottom_five_stu = list(bottom_five)

    # 4️⃣ Pass/Fail (<50%)
    fail_rate = Performance.objects.values(
        "student_id",
        "student__name"
    ).annotate(
        total_marks=Sum(Cast("marks", FloatField()))
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
    # Attendance model stores status as 'P'/'A' — use the same values here
    low_attendance_qs = Attendance.objects.values(
        "student_id",
        "student__name"
    ).annotate(
        att=Avg(
            Case(
                When(status='P', then=1),
                When(status='A', then=0),
                output_field=FloatField()
            )
        ) * 100
    ).filter(att__lt=75)

    low_attendance = list(low_attendance_qs)
    data = {
        "total_marks": total_marks,
        "top_five_stu": top_five_stu,
        "bottom_five_stu": bottom_five_stu,
        "fail_rate_status_details": fail_rate_status,
        "low_attendance": low_attendance,
    }

    # Also write a static JSON copy that chart templates consume
    try:
        out_path = Path(settings.BASE_DIR) / 'students' / 'static' / 'students' / 'data' / 'dashboard.json'
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        # Don't break the API if writing fails; log to console for now
        print('Failed to write static dashboard.json:', e)

    return JsonResponse(data)

@login_required
def pass_fail_chart_page(request):
    return render(request, "students/dashoard-data1.html")
@login_required
def top5_chart_page(request):
    return render(request, "students/top-5-studnt-chart.html")
@login_required
def bttm_5_pg(request):
    return render(request,"students/bttom-5-student.html")
@login_required
def mark_per_studnet(request):
    return render(request,"students/chart-total-marks.html")
@login_required
def marks_per_department(request):
    return render(request,"students/marks-basedon-department.html")
