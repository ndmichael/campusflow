from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from accounts.forms import LoginForm
from academics.models import Attendance, Enrollment, Result, Course, Department
from students.models import Student
from teacher.models import Teacher

from datetime import datetime
from django.contrib import messages
from django.utils import timezone

from django.db.models import Count


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.role == "admin":
        return redirect("admin_dashboard")

    if request.user.role == "teacher":
        return redirect("teacher_dashboard")

    if request.user.role == "student":
        return redirect("student_dashboard")

    raise PermissionDenied


@login_required
def admin_students(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        raise PermissionDenied

    students = (
        Student.objects
        .select_related("user")
        .annotate(course_count=Count("enrollments", distinct=True))
        .order_by(
            "user__last_name",
            "user__first_name",
        )
    )

    context = {
        "title": "Students",
        "students": students,
        "total_students": students.count(),
    }

    return render(
        request,
        "accounts/dashboard/admin/students.html",
        context,
    )

@login_required
def student_dashboard(request):
    if request.user.role != "student":
        raise PermissionDenied

    student = request.user.student_profile

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__department",
            "course__teacher__user",
        )
        .order_by("-enrolled_at")
    )

    attendance_records = (
        Attendance.objects
        .filter(student=student)
        .select_related("course")
        .order_by("-date")
    )

    results = (
        Result.objects
        .filter(student=student)
        .select_related("course")
        .order_by("-id")
    )

    total_courses = enrollments.count()

    total_attendance = attendance_records.count()

    present_count = attendance_records.filter(
        status="present"
    ).count()

    late_count = attendance_records.filter(
        status="late"
    ).count()

    absent_count = attendance_records.filter(
        status="absent"
    ).count()

    attendance_percentage = (
        round(
            ((present_count + late_count) / total_attendance) * 100,
            1,
        )
        if total_attendance
        else 0
    )

    result_count = results.count()

    average_score = (
        round(
            sum(float(result.score) for result in results) / result_count,
            1,
        )
        if result_count
        else 0
    )

    recent_courses = enrollments[:5]
    recent_results = results[:5]
    recent_attendance = attendance_records[:5]

    # Data for performance chart
    performance_chart = [
        {
            "label": result.course.code,
            "score": float(result.score),
        }
        for result in results[:8]
    ]

    performance_chart.reverse()

    # Data for attendance chart
    attendance_chart = {
        "present": present_count,
        "late": late_count,
        "absent": absent_count,
    }

    context = {
        "title": "Student Dashboard",
        "student": student,

        "total_courses": total_courses,

        "total_attendance": total_attendance,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "attendance_percentage": attendance_percentage,

        "result_count": result_count,
        "average_score": average_score,

        "recent_courses": recent_courses,
        "recent_results": recent_results,
        "recent_attendance": recent_attendance,

        "performance_chart": performance_chart,
        "attendance_chart": attendance_chart,
    }

    return render(
        request,
        "accounts/dashboard/student/dashboard.html",
        context,
    )


@login_required
def teacher_dashboard(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    courses = (
        Course.objects
        .filter(teacher=teacher)
        .select_related("department")
    )

    total_courses = courses.count()

    total_students = (
        Enrollment.objects
        .filter(course__teacher=teacher)
        .values("student")
        .distinct()
        .count()
    )

    attendance_records = Attendance.objects.filter(
        course__teacher=teacher
    )

    total_attendance = attendance_records.count()

    present_count = attendance_records.filter(
        status="present"
    ).count()

    absent_count = attendance_records.filter(
        status="absent"
    ).count()

    late_count = attendance_records.filter(
        status="late"
    ).count()

    attendance_percentage = (
        round((present_count / total_attendance) * 100, 1)
        if total_attendance
        else 0
    )

    results = (
        Result.objects
        .filter(course__teacher=teacher)
        .select_related("student", "student__user", "course")
        .order_by("-id")
    )

    result_count = results.count()

    average_score = (
        round(
            sum(float(result.score) for result in results) / result_count,
            1,
        )
        if result_count
        else 0
    )

    recent_courses = courses[:6]
    recent_results = results[:5]

    context = {
        "title": "Teacher Dashboard",
        "teacher": teacher,

        "total_courses": total_courses,
        "total_students": total_students,

        "total_attendance": total_attendance,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "attendance_percentage": attendance_percentage,

        "result_count": result_count,
        "average_score": average_score,

        "recent_courses": recent_courses,
        "recent_results": recent_results,
    }

    return render(
        request,
        "accounts/dashboard/teacher/dashboard.html",
        context,
    )


@login_required
def teacher_courses(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    courses = (
        Course.objects
        .filter(teacher=teacher)
        .select_related("department")
        .prefetch_related("enrollments")
        .order_by("code")
    )

    context = {
        "title": "My Courses",
        "teacher": teacher,
        "courses": courses,
        "total_courses": courses.count(),
    }

    return render(
        request,
        "accounts/dashboard/teacher/courses.html",
        context,
    )


@login_required
def teacher_students(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    enrollments = (
        Enrollment.objects
        .filter(course__teacher=teacher)
        .select_related(
            "student",
            "student__user",
            "course",
        )
        .order_by(
            "student__user__last_name",
            "student__user__first_name",
        )
    )

    students = {}

    for enrollment in enrollments:
        student = enrollment.student
        student_id = student.id

        if student_id not in students:
            students[student_id] = {
                "student": student,
                "courses": [],
            }

        students[student_id]["courses"].append(
            enrollment.course
        )

    students = list(students.values())

    context = {
        "title": "Students",
        "teacher": teacher,
        "students": students,
        "total_students": len(students),
    }

    return render(
        request,
        "accounts/dashboard/teacher/students.html",
        context,
    )


@login_required
def teacher_attendance(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    courses = (
        Course.objects
        .filter(teacher=teacher)
        .select_related("department")
        .order_by("code")
    )

    course_id = request.POST.get("course") or request.GET.get("course")
    selected_date = (
        request.POST.get("date")
        or request.GET.get("date")
        or timezone.localdate().isoformat()
    )

    selected_course = None
    students = []
    attendance_map = {}

    if course_id:
        selected_course = courses.filter(id=course_id).first()

    if selected_course:
        enrollments = (
            Enrollment.objects
            .filter(course=selected_course)
            .select_related("student", "student__user")
            .order_by(
                "student__user__last_name",
                "student__user__first_name",
            )
        )

        attendance_records = Attendance.objects.filter(
            course=selected_course,
            date=selected_date,
        )

        attendance_map = {
            record.student_id: record.status
            for record in attendance_records
        }

        students = [
            {
                "student": enrollment.student,
                "status": attendance_map.get(
                    enrollment.student.id,
                    "present",
                ),
            }
            for enrollment in enrollments
        ]

    if request.method == "POST" and selected_course:

        try:
            attendance_date = datetime.strptime(
                selected_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            messages.error(request, "Invalid attendance date.")
            return redirect(
                f"{request.path}?course={selected_course.id}"
            )

        for item in students:
            student = item["student"]

            status = request.POST.get(
                f"status_{student.id}",
                "present",
            )

            if status not in {
                "present",
                "late",
                "absent",
            }:
                status = "present"

            Attendance.objects.update_or_create(
                student=student,
                course=selected_course,
                date=attendance_date,
                defaults={
                    "status": status,
                },
            )

        messages.success(
            request,
            f"Attendance saved for {selected_course.code}.",
        )

        return redirect(
            f"{request.path}?course={selected_course.id}&date={selected_date}"
        )

    context = {
        "title": "Attendance",
        "teacher": teacher,
        "courses": courses,
        "selected_course": selected_course,
        "selected_date": selected_date,
        "students": students,
    }

    return render(
        request,
        "accounts/dashboard/teacher/attendance.html",
        context,
    )


@login_required
def teacher_results(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    courses = (
        Course.objects
        .filter(teacher=teacher)
        .select_related("department")
        .order_by("code")
    )

    course_id = request.POST.get("course") or request.GET.get("course")

    selected_course = None
    students = []

    if course_id:
        selected_course = courses.filter(id=course_id).first()

    if selected_course:
        enrollments = (
            Enrollment.objects
            .filter(course=selected_course)
            .select_related("student", "student__user")
            .order_by(
                "student__user__last_name",
                "student__user__first_name",
            )
        )

        student_ids = [
            enrollment.student.id
            for enrollment in enrollments
        ]

        results = (
            Result.objects
            .filter(
                course=selected_course,
                student_id__in=student_ids,
            )
            .order_by("-id")
        )

        result_map = {}

        for result in results:
            if result.student_id not in result_map:
                result_map[result.student_id] = result

        students = [
            {
                "student": enrollment.student,
                "result": result_map.get(
                    enrollment.student.id
                ),
            }
            for enrollment in enrollments
        ]

    if request.method == "POST" and selected_course:

        for item in students:
            student = item["student"]

            raw_score = request.POST.get(
                f"score_{student.id}"
            )

            if raw_score in (None, ""):
                continue

            try:
                score = float(raw_score)
            except (TypeError, ValueError):
                messages.error(
                    request,
                    "Scores must be valid numbers.",
                )
                return redirect(
                    f"{request.path}?course={selected_course.id}"
                )

            if score < 0 or score > 100:
                messages.error(
                    request,
                    "Scores must be between 0 and 100.",
                )
                return redirect(
                    f"{request.path}?course={selected_course.id}"
                )

            if score >= 70:
                grade = "A"
            elif score >= 60:
                grade = "B"
            elif score >= 50:
                grade = "C"
            elif score >= 45:
                grade = "D"
            elif score >= 40:
                grade = "E"
            else:
                grade = "F"

            Result.objects.update_or_create(
                student=student,
                course=selected_course,
                defaults={
                    "score": score,
                    "grade": grade,
                },
            )

        messages.success(
            request,
            f"Results saved for {selected_course.code}.",
        )

        return redirect(
            f"{request.path}?course={selected_course.id}"
        )

    context = {
        "title": "Results",
        "teacher": teacher,
        "courses": courses,
        "selected_course": selected_course,
        "students": students,
    }

    return render(
        request,
        "accounts/dashboard/teacher/results.html",
        context,
    )


@login_required
def teacher_profile(request):
    if request.user.role != "teacher":
        raise PermissionDenied

    teacher = request.user.teacher_profile

    courses = (
        Course.objects
        .filter(teacher=teacher)
        .select_related("department")
        .order_by("code")
    )

    context = {
        "title": "My Profile",
        "teacher": teacher,
        "courses": courses,
        "total_courses": courses.count(),
    }

    return render(
        request,
        "accounts/dashboard/teacher/profile.html",
        context,
    )



@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == "admin"):
        raise PermissionDenied

    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_courses = Course.objects.count()
    total_departments = Department.objects.count()
    total_enrollments = Enrollment.objects.count()

    total_attendance = Attendance.objects.count()

    present_count = Attendance.objects.filter(
        status="present"
    ).count()

    late_count = Attendance.objects.filter(
        status="late"
    ).count()

    absent_count = Attendance.objects.filter(
        status="absent"
    ).count()

    attendance_percentage = (
        round((present_count / total_attendance) * 100, 1)
        if total_attendance
        else 0
    )

    total_results = Result.objects.count()

    average_score = (
        round(
            sum(float(result.score) for result in Result.objects.all())
            / total_results,
            1,
        )
        if total_results
        else 0
    )

    recent_students = (
        Student.objects
        .select_related("user")
        .order_by("-id")[:5]
    )

    recent_teachers = (
        Teacher.objects
        .select_related("user")
        .order_by("-id")[:5]
    )

    recent_courses = (
        Course.objects
        .select_related("department", "teacher__user")
        .order_by("-id")[:6]
    )

    departments = (
        Department.objects
        .prefetch_related("courses")
        .order_by("name")
    )

    department_data = []

    for department in departments:
        department_data.append({
            "name": department.name,
            "courses": department.courses.count(),
        })

    context = {
        "title": "Admin Dashboard",

        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_courses": total_courses,
        "total_departments": total_departments,
        "total_enrollments": total_enrollments,

        "total_attendance": total_attendance,
        "present_count": present_count,
        "late_count": late_count,
        "absent_count": absent_count,
        "attendance_percentage": attendance_percentage,

        "total_results": total_results,
        "average_score": average_score,

        "recent_students": recent_students,
        "recent_teachers": recent_teachers,
        "recent_courses": recent_courses,

        "department_data": department_data,
    }

    return render(
        request,
        "accounts/dashboard/admin/dashboard.html",
        context,
    )




#NEXT LOGICAL STEP
@login_required
def student_courses(request):
    if request.user.role != "student":
        raise PermissionDenied

    student = request.user.student_profile

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__department",
            "course__teacher__user",
        )
        .order_by("course__code")
    )

    context = {
        "title": "My Courses",
        "student": student,
        "enrollments": enrollments,
        "total_courses": enrollments.count(),
    }

    return render(
        request,
        "accounts/dashboard/student/courses.html",
        context,
    )


@login_required
def student_attendance(request):
    if request.user.role != "student":
        raise PermissionDenied

    student = request.user.student_profile

    attendance_records = (
        Attendance.objects
        .filter(student=student)
        .select_related("course")
        .order_by("-date", "course__code")
    )

    total = attendance_records.count()
    present = attendance_records.filter(status="present").count()
    late = attendance_records.filter(status="late").count()
    absent = attendance_records.filter(status="absent").count()

    attendance_percentage = (
        round(((present + late) / total) * 100, 1)
        if total
        else 0
    )

    context = {
        "title": "Attendance",
        "student": student,
        "attendance_records": attendance_records,

        "total_attendance": total,
        "present_count": present,
        "late_count": late,
        "absent_count": absent,
        "attendance_percentage": attendance_percentage,
    }

    return render(
        request,
        "accounts/dashboard/student/attendance.html",
        context,
    )

@login_required
def student_results(request):
    if request.user.role != "student":
        raise PermissionDenied

    student = request.user.student_profile

    results = (
        Result.objects
        .filter(student=student)
        .select_related("course", "course__department")
        .order_by("-id")
    )

    total_results = results.count()

    average_score = (
        round(
            sum(float(result.score) for result in results) / total_results,
            1
        )
        if total_results
        else 0
    )

    highest_score = (
        max(float(result.score) for result in results)
        if total_results
        else 0
    )

    passed_count = results.filter(score__gte=40).count()
    failed_count = results.filter(score__lt=40).count()

    context = {
        "title": "Results",
        "student": student,
        "results": results,
        "total_results": total_results,
        "average_score": average_score,
        "highest_score": highest_score,
        "passed_count": passed_count,
        "failed_count": failed_count,
    }

    return render(
        request,
        "accounts/dashboard/student/results.html",
        context
    )


@login_required
def student_profile(request):
    if request.user.role != "student":
        raise PermissionDenied

    student = (
        request.user.student_profile
    )

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related(
            "course",
            "course__department",
            "course__teacher__user",
        )
        .order_by("course__code")
    )

    attendance_records = Attendance.objects.filter(
        student=student
    )

    total_attendance = attendance_records.count()

    present_count = attendance_records.filter(
        status="present"
    ).count()

    late_count = attendance_records.filter(
        status="late"
    ).count()

    attendance_percentage = (
        round(
            ((present_count + late_count) / total_attendance) * 100,
            1
        )
        if total_attendance
        else 0
    )

    context = {
        "title": "My Profile",
        "student": student,
        "enrollments": enrollments,
        "total_courses": enrollments.count(),
        "attendance_percentage": attendance_percentage,
    }

    return render(
        request,
        "accounts/dashboard/student/profile.html",
        context
    )