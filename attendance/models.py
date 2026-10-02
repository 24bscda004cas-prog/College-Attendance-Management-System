from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):

    YEAR_CHOICES = [
        (1, "1st Year"),
        (2, "2nd Year"),
        (3, "3rd Year"),
    ]

    DEPARTMENT_CHOICES = [
        ("AI", "Artificial Intelligence"),
        ("CS", "Computer Science"),
        ("DA", "Data Analytics"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    register_number = models.CharField(
        max_length=30,
        unique=True
    )

    full_name = models.CharField(
        max_length=120
    )

    department = models.CharField(
        max_length=2,
        choices=DEPARTMENT_CHOICES,
        default="CS"
    )

    year = models.PositiveSmallIntegerField(
        choices=YEAR_CHOICES
    )

    section = models.CharField(
        max_length=10,
        default="A"
    )

    email = models.EmailField(
        blank=True
    )

    def __str__(self):
        return f"{self.register_number} - {self.full_name}"


class Faculty(models.Model):

    DEPARTMENT_CHOICES = [
        ("AI", "Artificial Intelligence"),
        ("CS", "Computer Science"),
        ("DA", "Data Analytics"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    employee_id = models.CharField(
        max_length=30,
        unique=True
    )

    full_name = models.CharField(
        max_length=120
    )

    department = models.CharField(
        max_length=2,
        choices=DEPARTMENT_CHOICES,
        default="CS"
    )

    email = models.EmailField(
        blank=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class Subject(models.Model):

    code = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=120
    )

    year = models.PositiveSmallIntegerField(
        choices=Student.YEAR_CHOICES
    )

    section = models.CharField(
        max_length=10,
        default="A"
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.code} - {self.name}"


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("P", "Present"),
        ("A", "Absent"),
        ("OD", "On Duty"),
        ("ML", "Medical Leave"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    period = models.PositiveSmallIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES
    )

    marked_by = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    marked_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject",
                    "date",
                    "period"
                ],
                name="unique_attendance"
            )
        ]

        ordering = [
            "-date",
            "period"
        ]

    def __str__(self):
        return (
            f"{self.student} | "
            f"{self.subject} | "
            f"{self.date} | "
            f"{self.status}"
        )