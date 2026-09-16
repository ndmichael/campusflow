from django.urls import path
from accounts.views import (
    UserLoginView, dashboard, 
    teacher_dashboard,
    teacher_courses,
    teacher_students,
    student_dashboard,
    admin_dashboard,
    student_courses,
    student_attendance,
    student_results,
    student_profile,
    
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('dashboard/admin/', admin_dashboard, name="admin_dashboard"),
    path('dashboard/teacher/', teacher_dashboard, name="teacher_dashboard"),
    path(
        "dashboard/teacher/courses/",
        teacher_courses,
        name="teacher_courses",
    ),

    path(
        "dashboard/teacher/students/",
        teacher_students,
        name="teacher_students",
    ),
    path('dashboard/student/', student_dashboard, name="student_dashboard"),
    path(
        "dashboard/student/courses/",
        student_courses,
        name="student_courses",
    ),

    path(
        "dashboard/student/attendance/",
        student_attendance,
        name="student_attendance",
    ),
    path(
        "dashboard/student/results/",
        student_results,
        name="student_results"
    ),

    path(
        "dashboard/profile/",
        student_profile,
        name="student_profile"
    ),
    
]