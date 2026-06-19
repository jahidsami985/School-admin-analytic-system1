from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Case, FloatField, Sum, When
from django.db.models.functions import Cast
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render

from students.models import Attendance, Performance, Teacher


@login_required
def teacher_dashboard_data(request, teacher_id):
    """
    Dashboard JSON for a specific teacher.
    Accessible only by the teacher who owns it.
    """
    teacher = get_object_or_404(
        Teacher.objects.select_related("user", "course"),
        id=teacher_id,
    )

    if teacher.user_id != request.user.id:
        return HttpResponseForbidden("Access denied")

    teacher_payload = {
        "id": teacher.id,
        "name": teacher.name,
        "email": teacher.email,
        "course": teacher.course.name if teacher.course else None,
        "course_code": teacher.course.code if teacher.course else None,
    }

    if teacher.course_id is None:
        return JsonResponse({
            "teacher": teacher_payload,
            "avg_score": 0,
            "top_students": [],
            "bottom_students": [],
            "low_attendance": [],
        })

    course_id = teacher.course_id

    avg_score = Performance.objects.filter(course_id=course_id).aggregate(
        avg=Avg(Cast("marks", FloatField()), output_field=FloatField())
    )["avg"] or 0

    top_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum(Cast("marks", FloatField())))
        .order_by("-total")[:5]
    )

    bottom_students = list(
        Performance.objects.filter(course_id=course_id)
        .values("student_id", "student__name")
        .annotate(total=Sum(Cast("marks", FloatField())))
        .order_by("total")[:5]
    )

    attendance_summary = Attendance.objects.filter(course_id=course_id).values(
        "student_id",
        "student__name",
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
        "teacher": teacher_payload,
        "avg_score": avg_score,
        "top_students": top_students,
        "bottom_students": bottom_students,
        "low_attendance": low_attendance,
    })


@login_required
def teacher_list(request):
    teachers = [
        {
            "id": teacher.id,
            "name": teacher.name,
            "email": teacher.email,
            "course__name": teacher.course.name if teacher.course else None,
            "course__code": teacher.course.code if teacher.course else None,
        }
        for teacher in Teacher.objects.select_related("user", "course")
    ]
    return JsonResponse(teachers, safe=False)


@login_required
def teacher_dashboard_page(request, teacher_id):
    """
    Renders the Teacher Dashboard HTML page.
    Actual data is fetched via teacher_dashboard_data (AJAX).
    """
    teacher = get_object_or_404(
        Teacher.objects.select_related("user", "course"),
        id=teacher_id,
    )

    if teacher.user_id != request.user.id:
        return HttpResponseForbidden("Access denied")

    return render(
        request,
        "teacher/teacher_dashboard.html",
        {"teacher_id": teacher.id},
    )
