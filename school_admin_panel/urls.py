from django.urls import path
from students.views import admin_views   # ← new import

urlpatterns = [
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
    path("pass-fail-chart/", admin_views.pass_fail_chart_page, name="pass_fail_chart"),
    path("top-5/", admin_views.top5_chart_page, name="top5_chart_page"),
    path("bttm-5/", admin_views.bttm_5_pg, name="bttm_5_pg"),
    path("mark-per/", admin_views.mark_per_studnet, name="mark_per_studnet"),
    path("marks_dept/", admin_views.marks_per_department, name="marks_per_department"),
]
