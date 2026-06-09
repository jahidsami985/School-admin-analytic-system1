import json
from django.core.management.base import BaseCommand
from django.conf import settings
from students.models import Performance, Attendance
from django.db.models import Sum, Avg, Case, When, FloatField, IntegerField
from django.db.models.functions import Cast
from django.db.models import F
from django.db import transaction


class Command(BaseCommand):
    help = 'Export dashboard data to students/static/students/data/dashboard.json'

    def handle(self, *args, **options):
        out_path = settings.BASE_DIR / 'students' / 'static' / 'students' / 'data' / 'dashboard.json'

        # Build the same structure as views.dashboard_data
        total_marks_qs = Performance.objects.values(
            "student_id",
            "student__name",
            "student__department__id",
            "student__department__name"
        ).annotate(total_marks=Sum(Cast('marks', FloatField())))

        top_five_qs = Performance.objects.values(
            "student_id",
            "student__name",
            "student__department__id",
            "student__department__name"
        ).annotate(total_marks=Sum(Cast('marks', FloatField()))).order_by('-total_marks')[:5]

        bottom_five_qs = Performance.objects.values(
            "student_id",
            "student__name"
        ).annotate(total_marks=Sum(Cast('marks', FloatField()))).order_by('total_marks')[:5]

        fail_rate = Performance.objects.values(
            "student_id",
            "student__name"
        ).annotate(
            total_marks=Sum(Cast('marks', FloatField()))
        )

        fail_rate_status = [
            {
                "student_id": stu["student_id"],
                "student_name": stu["student__name"],
                "total_marks": stu["total_marks"],
                "status": "fail" if stu["total_marks"] and stu["total_marks"] < 50 else "passed"
            }
            for stu in fail_rate
        ]

        low_attendance_qs = Attendance.objects.values(
            "student_id",
            "student__name"
        ).annotate(
            att=Avg(
                Case(
                    When(status='P', then=1),
                    When(status='A', then=0),
                    output_field=FloatField()
                )
            ) * 100
        ).filter(att__lt=75)

        data = {
            "total_marks": list(total_marks_qs),
            "top_five_stu": list(top_five_qs),
            "bottom_five_stu": list(bottom_five_qs),
            "fail_rate_status_details": fail_rate_status,
            "low_attendance": list(low_attendance_qs),
        }

        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Wrote dashboard JSON to {out_path}'))
