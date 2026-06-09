from django.contrib import admin
from django.urls import include, path

from students.views import admin_views, teacher_views
from students.views.admin_views import home
from register1.views import (
    login_view,
    register_view,
    logout_view,
    teacher_dashboard,
    student_dashboard,
    admin_dashboard,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # Student CRUD & Lists
    path("students/", admin_views.student_list, name="student_list"),
    path("student_p/", admin_views.student_perform, name="student_perform"),
    path("attendace_s/", admin_views.student_attandance, name="student_attandance"),
    path("manage-students/", admin_views.manage_students, name="manage_students"),
    path("edit-student-info/", admin_views.edit_student_info, name="edit_student_info"),
    path("attendance_edit_student/", admin_views.edit_attendance_info, name="edit_attendance_info"),
    path("edit_perform/", admin_views.edit_performance, name="edit_performance"),

    # Admin Analytics Dashboard URLs
    path("dashboard-data/", admin_views.dashboard_data, name="dashboard-data"),
    path("pass-fail-chart/", admin_views.pass_fail_chart_page, name="pass_fail_chart_page"),
    path("top-5/", admin_views.top5_chart_page, name="top5_chart_page"),
    path("bttm-5/", admin_views.bttm_5_pg, name="bttm_5_pg"),
    path("mark-per/", admin_views.mark_per_studnet, name="mark_per_studnet"),
    path("marks_dept/", admin_views.marks_per_department, name="marks_per_department"),

    #Teach Analytic dashboard
    path("Teacher-Dashboard-charts/<int:teacher_id>/",
    teacher_views.teacher_dashboard_page,
    name="Teacher-Dashboard-charts"),



    path("", include("register1.urls")),
    path("", home, name="home"),

    path("dashboard/teacher/", teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/student/", student_dashboard, name="student_dashboard"),
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),
]




