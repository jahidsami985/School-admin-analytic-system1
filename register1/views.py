from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from students.models import Student,Teacher,Department

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        role = request.POST.get("role", "").strip()

        if not username or not email or not password or not confirm_password or not role:
            messages.error(request, "Please complete all fields.")
            return render(request, "register1/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register1/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "register1/register.html")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        if role == "student":
            department, _ = Department.objects.get_or_create(name="General")

            Student.objects.create(
                user=user,
                name=username,
                email=email,
                roll_num="TEMP",
                department=department,
            )
        elif role == "teacher":
            Teacher.objects.create(
                user=user,
                name=username,
            )
        elif role == "admin":
            user.is_staff = True
            user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "register1/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("insights")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("insights")

        messages.error(request, "Invalid username or password")

    return render(request, "register1/login.html")




def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def insights_view(request):
    return render(request, "students/insights.html")


@login_required
def dashboard_view(request):
    return render(request, "students/insights.html")

@login_required
def teacher_dashboard(request):
    return render(request, "teacher/dashboard.html")

@login_required
def student_dashboard(request):
    return render(request, "students/dashboard.html")

@login_required
def admin_dashboard(request):
    return render(request, "admin/dashboard.html")





