from django.http import JsonResponse
from django.db.models import Avg, Sum, Case, When, FloatField, IntegerField
from students.models import Teacher, Student, Performance, Attendance, Course
from django.shortcuts import render


# -----------------------------------------
# 1️⃣ TEACHER LIST (optional)
# -----------------------------------------
def teacher_list(request):
    teachers = Teacher.objects.values(
        "course_id",
        "name",
        "email",
        "course__name",
        "course__code",
    )
    return JsonResponse(list(teachers), safe=False)


# -----------------------------------------
# 2️⃣ TEACHER DASHBOARD (JSON for charts)
# -----------------------------------------
def teacher_dashboard_data(request, teacher_id):
    """
    Dashboard JSON for a specific teacher.
    Shows:
        - Average marks for this teacher's course
        - Top 5 students
        - Bottom 5 students
        - Attendance summary
    """

    # Check teacher exists
    try:
        teacher = Teacher.objects.select_related("course").get(course_id=teacher_id)
    except Teacher.DoesNotExist:
        return JsonResponse({"error": "Teacher not found"}, status=404)

    course_id = teacher.course_id

    # 1️⃣ Average marks in this teacher’s course
    avg_score = Performance.objects.filter(course_id=course_id).aggregate(
        avg=Avg("marks", output_field=FloatField())
    )["avg"]

    # 2️⃣ Top 5 students for this teacher
    top_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum("marks", output_field=FloatField()))
        .order_by("-total")[:5]
    )

    # 3️⃣ Bottom 5 students
    bottom_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum("marks", output_field=FloatField()))
        .order_by("total")[:5]
    )

    # 4️⃣ Attendance percentage for this teacher’s course
    attendance = Attendance.objects.filter(course_id=course_id)

    attendance_summary = attendance.values("student_id", "student__name").annotate(
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
            "id": teacher.course_id,
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


# -----------------------------------------
# 3️⃣ TEMPLATE PAGE (for Chart.js)
# -----------------------------------------
def teacher_dashboard_page(request, teacher_id):
    return render(request, "teacher/teacher_dashboard.html", {"teacher_id": teacher_id})
