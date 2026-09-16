from django.urls import path
from accounts.views import (
    UserLoginView, dashboard, 
    teacher_dashboard,
    teacher_courses,
    teacher_students,
    student_dashboard,
    teacher_attendance,
    teacher_results,
    teacher_profile,

    admin_dashboard,
    admin_students,
    admin_teachers,
    admin_courses,
    admin_departments,


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
    path(
        "dashboard/admin/students/",
        admin_students,
        name="admin_students",
    ),
    path(
        "dashboard/admin/teachers/",
        admin_teachers,
        name="admin_teachers",
    ),
    path(
        "dashboard/admin/courses/",
        admin_courses,
        name="admin_courses",
    ),

    path(
        "dashboard/admin/departments/",
        admin_departments,
        name="admin_departments",
    ),
    

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
    path(
        "dashboard/teacher/attendance/",
        teacher_attendance,
        name="teacher_attendance",
    ),

    path(
        "dashboard/teacher/results/",
        teacher_results,
        name="teacher_results",
    ),
    path(
        "dashboard/teacher/profile/",
        teacher_profile,
        name="teacher_profile",
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