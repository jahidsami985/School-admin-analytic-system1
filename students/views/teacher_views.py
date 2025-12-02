from django.shortcuts import render

def teacher_dashboard(request):
    return render(request, "students/teacher/dashboard.html")