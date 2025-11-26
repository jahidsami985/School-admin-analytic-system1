from django import forms
from django.forms import modelformset_factory
from .models import Student, Attendance, Performance


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "roll_num", "email", "department"]

StudentFormSet = modelformset_factory(
    Student,
    form=StudentForm,
    extra=2,
    can_delete=True
)


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['date', 'status']

AttendanceFormSet = modelformset_factory(
    Attendance,
    form=AttendanceForm,
    extra=2,
    can_delete=True
)


class PerformanceForm(forms.ModelForm):
    class Meta:
        model = Performance
        fields = ["student", "course", "marks", "grade"]
        widgets = {
            'student': forms.HiddenInput(),
            'course': forms.HiddenInput(),
        }

PerformanceFormSet = modelformset_factory(
    Performance,
    form=PerformanceForm,
    extra=0,       # only existing performances
    can_delete=False
)