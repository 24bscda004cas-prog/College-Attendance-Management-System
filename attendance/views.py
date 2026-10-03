from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone

from .models import Student, Faculty, Subject, Attendance


def home(request):
    if request.user.is_authenticated:
        return dashboard(request)

    return render(request, "home.html")


@login_required
def dashboard(request):

    counts = {
        item["status"]: item["total"]
        for item in Attendance.objects
        .values("status")
        .annotate(total=Count("id"))
    }

    total_attendance = sum(counts.values())

    attendance_percentage = (
        round((counts.get("P", 0) / total_attendance) * 100, 2)
        if total_attendance > 0
        else 0
    )

    context = {

        # Basic counts
        "total_students": Student.objects.count(),
        "total_faculty": Faculty.objects.count(),
        "total_subjects": Subject.objects.count(),

        # Attendance counts
        "present": counts.get("P", 0),
        "absent": counts.get("A", 0),
        "od": counts.get("OD", 0),
        "ml": counts.get("ML", 0),

        # Attendance analysis
        "total_attendance": total_attendance,
        "attendance_percentage": attendance_percentage,

        # Dashboard cards
        "rows": [
            ("Total Students", Student.objects.count()),
            ("Faculty", Faculty.objects.count()),
            ("Subjects", Subject.objects.count()),
            ("Present", counts.get("P", 0)),
            ("Absent", counts.get("A", 0)),
            ("OD", counts.get("OD", 0)),
            ("ML", counts.get("ML", 0)),
        ],

        # Students by year
        "year_counts": [
            ("1st Year", Student.objects.filter(year=1).count()),
            ("2nd Year", Student.objects.filter(year=2).count()),
            ("3rd Year", Student.objects.filter(year=3).count()),
        ],
    }

    return render(request, "dashboard.html", context)


@login_required
def student_list(request):

    students = Student.objects.all().order_by(
        "year",
        "department",
        "register_number"
    )

    return render(
        request,
        "students.html",
        {"students": students}
    )


@login_required
def attendance_mark(request):
    """
    Faculty attendance marking page.

    GET:
        Select subject, date and period.

    POST:
        Save Present / Absent / OD / ML for students.
    """

    subjects = Subject.objects.all().order_by(
        "year",
        "code"
    )

    selected_subject = None

    selected_date = (
        request.POST.get("date")
        or request.GET.get("date")
    )

    selected_period = (
        request.POST.get("period")
        or request.GET.get("period", "1")
    )

    if request.method == "POST":

        subject_id = request.POST.get("subject")

        if not subject_id:
            messages.error(
                request,
                "Please select a subject."
            )

            return redirect("attendance_mark")

        try:
            selected_subject = Subject.objects.get(
                id=subject_id
            )

        except Subject.DoesNotExist:

            messages.error(
                request,
                "Subject not found."
            )

            return redirect("attendance_mark")

        students = Student.objects.filter(
            year=selected_subject.year,
            section=selected_subject.section
        ).order_by(
            "department",
            "register_number"
        )

        for student in students:

            status = request.POST.get(
                f"status_{student.id}"
            )

            if status not in [
                "P",
                "A",
                "OD",
                "ML"
            ]:
                continue

            Attendance.objects.update_or_create(

                student=student,

                subject=selected_subject,

                date=selected_date,

                period=selected_period,

                defaults={
                    "status": status,
                    "marked_at": timezone.now(),
                }
            )

        messages.success(
            request,
            "Attendance saved successfully."
        )

        return redirect("attendance_mark")

    students = Student.objects.none()

    if request.GET.get("subject"):

        try:

            selected_subject = Subject.objects.get(
                id=request.GET.get("subject")
            )

            students = Student.objects.filter(
                year=selected_subject.year,
                section=selected_subject.section
            ).order_by(
                "department",
                "register_number"
            )

        except Subject.DoesNotExist:

            selected_subject = None

    return render(
        request,
        "attendance_mark.html",
        {
            "subjects": subjects,
            "students": students,
            "selected_subject": selected_subject,
            "selected_date": selected_date,
            "selected_period": selected_period,
        }
    )


@login_required
def student_attendance(request, student_id=None):
    """
    Shows attendance history for a student.
    """

    if student_id:

        student = Student.objects.get(
            id=student_id
        )

    else:

        student = Student.objects.filter(
            user=request.user
        ).first()

    if not student:

        messages.error(
            request,
            "Student profile not found."
        )

        return redirect("dashboard")

    attendance = Attendance.objects.filter(
        student=student
    ).select_related(
        "subject"
    ).order_by(
        "-date",
        "period"
    )

    counts = {
        item["status"]: item["total"]
        for item in attendance
        .values("status")
        .annotate(total=Count("id"))
    }

    total = attendance.count()

    percentage = 0

    if total > 0:

        percentage = round(
            (counts.get("P", 0) / total) * 100,
            2
        )

    return render(
        request,
        "student_attendance.html",
        {
            "student": student,
            "attendance": attendance,
            "total": total,
            "present": counts.get("P", 0),
            "absent": counts.get("A", 0),
            "od": counts.get("OD", 0),
            "ml": counts.get("ML", 0),
            "percentage": percentage,
        }
    )