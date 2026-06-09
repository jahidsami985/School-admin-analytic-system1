from django.shortcuts import render

def student_dashboard(request):
    return render(request, "students/student/dashboard.html")