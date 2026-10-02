from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),

    path(
        "attendance/mark/",
        views.attendance_mark,
        name="attendance_mark"
    ),

    path(
        "attendance/student/",
        views.student_attendance,
        name="student_attendance"
    ),

    path(
        "attendance/student/<int:student_id>/",
        views.student_attendance,
        name="student_attendance_detail"
    ),
]