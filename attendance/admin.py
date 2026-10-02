from django.contrib import admin
from .models import Student,Faculty,Subject,Attendance
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=("register_number","full_name","year","section","department")
    list_filter=("year","section"); search_fields=("register_number","full_name")
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display=("employee_id","full_name","department")
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display=("code","name","year","section","faculty")
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display=("student","subject","date","period","status","marked_by")
    list_filter=("status","date","subject")
