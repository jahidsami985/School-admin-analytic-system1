"""
URL configuration for school_admin_panel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from students import views


urlpatterns = [
     path('admin/', admin.site.urls),
    
    path("", views.home, name="home"),
    path("students/", views.student_list, name="student_list"),
    path("student_p/", views.student_perform, name="student_perform"),
    path("attendance_s/", views.student_attandance, name="student_attandance"),
    path("manage-students/", views.manage_students, name="manage_students"),
    path("edit-student-info/",views.edit_student_info,name='edit_student_info'),
    path('attendance_edit_student/',views.edit_attendance_info,name="edit_attendance_info"),
    path("edit_perform/",views.edit_performance,name="edit_performance"),
    path("dashboard-data/", views.dashboard_data, name="dashboard-data"),
    path("pass-fail-chart/", views.pass_fail_chart_page, name="pass_fail_chart"),
    path("top-5/",views.top5_chart_page,name="top5_chart_page"),
    path("bttm-5/",views.bttm_5_pg,name="bttm_5_pg"),
    path("mark-per/",views.mark_per_studnet,name="mark_per_studnet")

]



