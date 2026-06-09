from django.http import JsonResponse
from django.db.models import Avg, Sum, Case, When, FloatField, IntegerField
from django.db.models.functions import Cast
from students.models import Teacher, Student, Performance, Attendance, Course
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404


@login_required
def teacher_dashboard_data(request, teacher_id):
    """
    Dashboard JSON for a specific teacher.
    Accessible ONLY by the teacher who owns it.
    """

    teacher = get_object_or_404(
        Teacher.objects.select_related("course"),
        id=teacher_id
    )

    # 🔐 OWNERSHIP CHECK (MOST IMPORTANT LINE)
    if teacher.user != request.user:
        return HttpResponseForbidden("Access denied")

    course_id = teacher.course_id

    # 1️⃣ Average marks
    # marks stored as CharField; cast to Float for numeric aggregation
    avg_score = Performance.objects.filter(course_id=course_id).aggregate(
        avg=Avg(Cast("marks", FloatField()), output_field=FloatField())
    )["avg"]

    # 2️⃣ Top 5 students
    top_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum(Cast("marks", FloatField())))
        .order_by("-total")[:5]
    )

    # 3️⃣ Bottom 5 students
    bottom_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum(Cast("marks", FloatField())))
        .order_by("total")[:5]
    )

    # 4️⃣ Attendance percentage
    attendance_summary = Attendance.objects.filter(course_id=course_id).values(
        "student_id", "student__name"
    ).annotate(
        attendance_percentage=Avg(
            Case(
                When(status="P", then=1),
                When(status="A", then=0),
                output_field=FloatField(),
            )
        ) * 100
    )

    low_attendance = list(attendance_summary.filter(attendance_percentage__lt=75))

    return JsonResponse({
        "teacher": {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "course": teacher.course.name,
            "course_code": teacher.course.code,
        },
        "avg_score": avg_score,
        "top_students": top_students,
        "bottom_students": bottom_students,
        "low_attendance": low_attendance,
    })
@login_required

def teacher_list(request):
    teachers = Teacher.objects.values(
        "id",
        "name",
        "email",
        "course__name",
        "course__code",
    )
    return JsonResponse(list(teachers), safe=False)


@login_required
def teacher_dashboard_page(request, teacher_id):
    """
    Renders the Teacher Dashboard HTML page.
    Actual data is fetched via teacher_dashboard_data (AJAX).
    """

    teacher = get_object_or_404(Teacher, id=teacher_id)

    # 🔐 Ownership check
    if teacher.user != request.user:
        return HttpResponseForbidden("Access denied")

    return render(
        request,
        "teacher/teacher_dashboard.html",
        {"teacher_id": teacher.id}
    )
