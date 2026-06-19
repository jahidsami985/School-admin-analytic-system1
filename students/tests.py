from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from students.models import Attendance, Course, Department, Performance, Student, Teacher


class TeacherDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="pass12345",
        )
        self.teacher = Teacher.objects.create(user=self.user, name="Teacher One")
        self.client.force_login(self.user)

    def test_teacher_dashboard_page_uses_registered_data_url(self):
        response = self.client.get(
            reverse("teacher_dashboard_page", args=[self.teacher.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("teacher_dashboard_data", args=[self.teacher.id]),
        )
        self.assertContains(response, "cdn.jsdelivr.net/npm/chart.js")

    def test_teacher_dashboard_data_without_course_returns_empty_payload(self):
        response = self.client.get(
            reverse("teacher_dashboard_data", args=[self.teacher.id])
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["avg_score"], 0)
        self.assertEqual(data["top_students"], [])
        self.assertEqual(data["bottom_students"], [])
        self.assertIsNone(data["teacher"]["course"])
        self.assertEqual(data["teacher"]["email"], self.user.email)

    def test_teacher_dashboard_data_with_course_returns_course_metrics(self):
        department = Department.objects.create(name="Science")
        course = Course.objects.create(
            name="Math",
            code="M101",
            department=department,
        )
        self.teacher.course = course
        self.teacher.save()

        top_student = Student.objects.create(
            name="Top Student",
            roll_num="001",
            email="top@example.com",
            department=department,
        )
        low_student = Student.objects.create(
            name="Low Student",
            roll_num="002",
            email="low@example.com",
            department=department,
        )
        Performance.objects.create(
            student=top_student,
            course=course,
            marks="90",
            grade="A",
        )
        Performance.objects.create(
            student=low_student,
            course=course,
            marks="40",
            grade="F",
        )
        Attendance.objects.create(
            student=low_student,
            course=course,
            status=Attendance.ABSENT,
            date=date(2026, 6, 13),
        )

        response = self.client.get(
            reverse("teacher_dashboard_data", args=[self.teacher.id])
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["teacher"]["course"], "Math")
        self.assertEqual(data["teacher"]["course_code"], "M101")
        self.assertEqual(data["avg_score"], 65.0)
        self.assertEqual(data["top_students"][0]["student__name"], "Top Student")
        self.assertEqual(data["bottom_students"][0]["student__name"], "Low Student")
        self.assertEqual(data["low_attendance"][0]["student__name"], "Low Student")

    def test_teacher_dashboard_blocks_other_users(self):
        other_user = User.objects.create_user(
            username="other",
            password="pass12345",
        )
        self.client.force_login(other_user)

        response = self.client.get(
            reverse("teacher_dashboard_data", args=[self.teacher.id])
        )

        self.assertEqual(response.status_code, 403)
