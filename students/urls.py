from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.student_list, name="student_list"),
    path("student_p/", views.student_perform, name="student_perform"),
    path("attendace_s/",views.student_attandance,name="student_attandance"),
    path("manage-students/", views.manage_students, name="manage_students"),
    path("edit-student-info/",views.edit_student_info,name='edit_student_info'),
    path('attendance_edit_student/',views.edit_attendance_info,name="edit_attendance_info"),
    path("edit_perform/",views.edit_performance,name="edit_performance"),
    path("dashboard-data/", views.dashboard_data, name="dashboard-data"),
    path("pass-fail-chart/", views.pass_fail_chart_page, name="pass_fail_chart"),

]
