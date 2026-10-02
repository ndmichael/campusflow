import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from academics.models import (
    Department,
    Course,
    Enrollment,
    Attendance,
    Result,
)
from accounts.models import User
from students.models import Student
from teacher.models import Teacher


class Command(BaseCommand):
    help = "Reset and create realistic APTECHSys demo data."

    STUDENT_COUNT = 220
    TEACHER_COUNT = 15
    ADMIN_COUNT = 2
    ATTENDANCE_DAYS = 60

    def handle(self, *args, **options):

        with transaction.atomic():

            rng = random.Random(20260918)

            # =========================================================
            # REALISTIC NIGERIAN NAMES
            # =========================================================

            first_names = [
                "David", "Amina", "Chinedu", "Blessing", "Zainab",
                "Emeka", "Mary", "Daniel", "Samuel", "Grace",
                "Ibrahim", "Favour", "Michael", "Esther", "Joshua",
                "Adaeze", "Yusuf", "Victoria", "Oluwaseun", "Chioma",
                "Benjamin", "Halima", "Ifeanyi", "Joy", "Abdulrahman",
                "Deborah", "Nnamdi", "Ruth", "Musa", "Sophia",
                "Obinna", "Janet", "Usman", "Peace", "Kelvin",
                "Ngozi", "Ahmed", "Caroline", "Tochukwu", "Mercy",
                "Sani", "Faith", "Chisom", "Hauwa", "Godwin",
                "Patience", "Ikenna", "Elizabeth", "Olamide", "Rebecca",
                "Uche", "Mariam", "Ifeoma", "Peter", "Sadiq",
                "Amaka", "Joseph", "Hadiza", "Kingsley", "Sarah",
                "Ogochukwu", "Isaac", "Nafisat", "Victor", "Caroline",
                "Somtochukwu", "Anthony", "Fatima", "Kelvin", "Stephanie",
            ]

            surnames = [
                "Okafor", "Bello", "Okoro", "Adebayo", "Musa",
                "Eze", "Ibrahim", "Nwosu", "Yusuf", "Adeyemi",
                "Obi", "Mohammed", "Udo", "Olawale", "Ezeh",
                "Abdullahi", "Okechukwu", "Balogun", "Chukwu", "Suleiman",
                "Onyeka", "Usman", "Akinyemi", "Nwachukwu", "Lawal",
                "Ogunleye", "Ibe", "Danladi", "Ojo", "Okeke",
                "Ugwu", "Garba", "Afolabi", "Chukwuemeka", "Adamu",
                "Onu", "Yakubu", "Agu", "Oni", "Aliyu",
                "Umeh", "Abubakar", "Ezenwa", "Bassey", "Ogunbiyi",
                "Ikechukwu", "Ahmed", "Opara", "Bamidele", "Uche",
                "Nnamani", "Sani", "Fashola", "Nwankwo", "Olatunji",
                "Ezeani", "Danjuma", "Oyekan", "Anyanwu", "Iroha",
            ]

            teacher_names = [
                ("Michael", "Okoro", "Software Engineering"),
                ("Grace", "Okafor", "Web Development"),
                ("Daniel", "Adeyemi", "Database Systems"),
                ("Esther", "Nwosu", "Software Engineering"),
                ("Ibrahim", "Bello", "Networking"),
                ("Chioma", "Eze", "Web Development"),
                ("Samuel", "Adebayo", "Software Engineering"),
                ("Amina", "Yusuf", "Database Systems"),
                ("Peter", "Umeh", "Networking"),
                ("Victoria", "Obi", "Web Development"),
                ("Chinedu", "Nwachukwu", "Software Engineering"),
                ("Fatima", "Abdullahi", "Networking"),
                ("Joseph", "Opara", "Database Systems"),
                ("Deborah", "Ojo", "Information Systems"),
                ("Oluwaseun", "Afolabi", "Information Systems"),
            ]

            # =========================================================
            # DEMO USERNAMES
            # =========================================================

            student_usernames = [
                "student_demo"
            ] + [
                f"student_{index:03d}"
                for index in range(2, self.STUDENT_COUNT + 1)
            ]

            teacher_usernames = [
                "teacher_demo"
            ] + [
                f"teacher_{index:03d}"
                for index in range(2, self.TEACHER_COUNT + 1)
            ]

            admin_usernames = [
                "admin_demo",
                "admin_secondary",
            ]

            demo_usernames = (
                student_usernames
                + teacher_usernames
                + admin_usernames
            )

            # =========================================================
            # DEPARTMENTS
            # =========================================================

            department_data = [
                (
                    "Software Engineering",
                    "Software development, programming and engineering practices.",
                ),
                (
                    "Web Development",
                    "Frontend and backend web application development.",
                ),
                (
                    "Database Systems",
                    "Database design, administration and data management.",
                ),
                (
                    "Networking",
                    "Computer networks, infrastructure and communication systems.",
                ),
                (
                    "Information Systems",
                    "Business information systems and technology operations.",
                ),
                (
                    "Cybersecurity",
                    "Security principles, threats, protection and secure systems.",
                ),
            ]

            departments = {}

            for name, description in department_data:
                department, _ = Department.objects.update_or_create(
                    name=name,
                    defaults={
                        "description": description,
                    },
                )

                departments[name] = department

            # =========================================================
            # COURSE DEFINITIONS
            # =========================================================

            course_data = [
                ("PY101", "Python Programming I", "Software Engineering"),
                ("PY201", "Python Programming II", "Software Engineering"),
                ("JAVA101", "Java Programming I", "Software Engineering"),
                ("JAVA201", "Java Programming II", "Software Engineering"),
                ("SE201", "Software Engineering Principles", "Software Engineering"),

                ("WEB101", "HTML and CSS Fundamentals", "Web Development"),
                ("WEB201", "JavaScript Programming", "Web Development"),
                ("WEB202", "Frontend Development", "Web Development"),
                ("WEB301", "Backend Web Development", "Web Development"),
                ("WEB302", "Full-Stack Application Development", "Web Development"),

                ("DB101", "Database Fundamentals", "Database Systems"),
                ("DB201", "SQL and Relational Databases", "Database Systems"),
                ("DB202", "Database Design", "Database Systems"),
                ("DB301", "Database Administration", "Database Systems"),
                ("DB302", "Advanced Data Management", "Database Systems"),

                ("NET101", "Networking Fundamentals", "Networking"),
                ("NET201", "Routing and Switching", "Networking"),
                ("NET202", "Network Infrastructure", "Networking"),
                ("NET301", "Network Administration", "Networking"),
                ("NET302", "Wireless and Internet Technologies", "Networking"),

                ("IS101", "Information Systems Fundamentals", "Information Systems"),
                ("IS201", "Systems Analysis and Design", "Information Systems"),
                ("IS202", "IT Project Management", "Information Systems"),
                ("IS301", "Enterprise Systems", "Information Systems"),
                ("IS302", "Business Process Management", "Information Systems"),

                ("SEC101", "Cybersecurity Fundamentals", "Cybersecurity"),
                ("SEC201", "Network Security", "Cybersecurity"),
                ("SEC202", "Application Security", "Cybersecurity"),
                ("SEC301", "Security Operations", "Cybersecurity"),
                ("SEC302", "Ethical Hacking Fundamentals", "Cybersecurity"),
            ]

            course_codes = [item[0] for item in course_data]

            # =========================================================
            # CLEAN PREVIOUS DEMO RELATIONSHIP DATA
            # =========================================================

            demo_students_qs = Student.objects.filter(
                user__username__in=student_usernames
            )

            Enrollment.objects.filter(
                Q(student__in=demo_students_qs)
                | Q(course__code__in=course_codes)
            ).delete()

            Attendance.objects.filter(
                Q(student__in=demo_students_qs)
                | Q(course__code__in=course_codes)
            ).delete()

            Result.objects.filter(
                Q(student__in=demo_students_qs)
                | Q(course__code__in=course_codes)
            ).delete()

            # =========================================================
            # ADMINS
            # =========================================================

            admin_data = [
                (
                    "admin_demo",
                    "System",
                    "Administrator",
                    "admin@aptechsys.com",
                ),
                (
                    "admin_secondary",
                    "Sarah",
                    "Management",
                    "admin2@aptechsys.com",
                ),
            ]

            admins = []

            for username, first_name, last_name, email in admin_data:

                user, _ = User.objects.get_or_create(
                    username=username
                )

                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.role = "admin"
                user.is_active = True
                user.is_staff = True
                user.set_password("Admin@123")
                user.save()

                admins.append(user)

            # =========================================================
            # TEACHERS
            # =========================================================

            teachers = {}

            for index in range(self.TEACHER_COUNT):

                username = teacher_usernames[index]

                first_name, last_name, specialization = (
                    teacher_names[index]
                )

                if index == 0:
                    employee_id = "TCH001"
                    email = "teacher@aptechsys.com"
                else:
                    employee_id = f"TCH{index + 1:03d}"
                    email = (
                        f"{first_name.lower()}."
                        f"{last_name.lower()}@aptechsys.com"
                    )

                user, _ = User.objects.get_or_create(
                    username=username
                )

                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.role = "teacher"
                user.is_active = True
                user.set_password("Teacher@123")
                user.save()

                teacher, _ = Teacher.objects.update_or_create(
                    user=user,
                    defaults={
                        "employee_id": employee_id,
                        "phone": f"0803{index + 1:07d}",
                        "address": "Abuja, Nigeria",
                        "specialization": specialization,
                        "date_joined": date(2024, 9, 1)
                        + timedelta(days=index * 18),
                    },
                )

                teachers[username] = teacher

            # =========================================================
            # COURSES
            # =========================================================

            courses = {}

            teacher_list = list(teachers.values())

            for index, (
                code,
                name,
                department_name,
            ) in enumerate(course_data):

                teacher = teacher_list[index % len(teacher_list)]

                course, _ = Course.objects.update_or_create(
                    code=code,
                    defaults={
                        "name": name,
                        "department": departments[department_name],
                        "teacher": teacher,
                    },
                )

                courses[code] = course

            # =========================================================
            # STUDENTS
            # =========================================================

            students = {}

            for index in range(self.STUDENT_COUNT):

                first_name = first_names[index % len(first_names)]
                surname = surnames[(index * 13) % len(surnames)]

                # Make the first demo account an easy-to-recognise name.
                if index == 0:
                    first_name = "David"
                    surname = "Okafor"

                username = student_usernames[index]

                if index == 0:
                    email = "student@aptechsys.com"
                else:
                    email = (
                        f"{first_name.lower()}."
                        f"{surname.lower()}"
                        f"{index + 1}@aptechsys.com"
                    )

                user, _ = User.objects.get_or_create(
                    username=username
                )

                user.first_name = first_name
                user.last_name = surname
                user.email = email
                user.role = "student"
                user.is_active = True
                user.set_password("Student@123")
                user.save()

                # Produce varied but realistic student dates.
                birth_year = 1999 + (index % 8)
                birth_month = 1 + (index % 12)
                birth_day = 5 + (index % 20)

                admission_date = (
                    date(2025, 9, 15)
                    + timedelta(days=(index % 90))
                )

                student, _ = Student.objects.update_or_create(
                    user=user,
                    defaults={
                        "student_id": f"STU{index + 1:03d}",
                        "date_of_birth": date(
                            birth_year,
                            birth_month,
                            birth_day,
                        ),
                        "phone": f"0802{index + 1:07d}",
                        "address": "Abuja, Nigeria",
                        "admission_date": admission_date,
                    },
                )

                students[username] = student

            # =========================================================
            # ENROLLMENTS
            # =========================================================

            enrollment_objects = []
            student_courses = {}

            course_list = list(courses.values())

            for index in range(self.STUDENT_COUNT):

                username = student_usernames[index]
                student = students[username]

                # Each student takes 5, 6 or 7 courses.
                course_count = 5 + (index % 3)

                selected_courses = rng.sample(
                    course_list,
                    course_count,
                )

                student_courses[username] = selected_courses

                for course in selected_courses:

                    enrollment_objects.append(
                        Enrollment(
                            student=student,
                            course=course,
                        )
                    )

            Enrollment.objects.bulk_create(
                enrollment_objects,
                batch_size=1000,
            )

            # =========================================================
            # ATTENDANCE DATES
            # =========================================================

            attendance_dates = []

            current_date = timezone.localdate()

            while len(attendance_dates) < self.ATTENDANCE_DAYS:

                if current_date.weekday() < 5:
                    attendance_dates.append(current_date)

                current_date -= timedelta(days=1)

            attendance_dates.reverse()

            # =========================================================
            # ATTENDANCE
            # =========================================================

            attendance_objects = []

            for index in range(self.STUDENT_COUNT):

                username = student_usernames[index]
                student = students[username]

                # Student reliability varies between roughly
                # 62% and 96%, giving dashboards useful variation.
                reliability = (
                    0.62
                    + ((index * 17) % 35) / 100
                )

                for course_index, course in enumerate(
                    student_courses[username]
                ):

                    course_adjustment = (
                        ((course_index * 3) % 5) - 2
                    ) / 100

                    student_reliability = max(
                        0.55,
                        min(
                            0.97,
                            reliability + course_adjustment,
                        ),
                    )

                    for attendance_date in attendance_dates:

                        roll = rng.random()

                        if roll < student_reliability:
                            status = "present"
                        elif roll < student_reliability + 0.07:
                            status = "late"
                        else:
                            status = "absent"

                        attendance_objects.append(
                            Attendance(
                                student=student,
                                course=course,
                                date=attendance_date,
                                status=status,
                            )
                        )

            Attendance.objects.bulk_create(
                attendance_objects,
                batch_size=5000,
            )

            # =========================================================
            # RESULTS
            # =========================================================

            result_objects = []

            for index in range(self.STUDENT_COUNT):

                username = student_usernames[index]
                student = students[username]

                reliability = (
                    0.62
                    + ((index * 17) % 35) / 100
                )

                for course_index, course in enumerate(
                    student_courses[username]
                ):

                    # Small course difficulty variation.
                    difficulty = (
                        ((course_index * 7) % 9) - 4
                    )

                    score = (
                        25
                        + (reliability * 55)
                        + rng.randint(-12, 12)
                        + difficulty
                    )

                    score = round(
                        max(35, min(98, score)),
                        2,
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

                    result_objects.append(
                        Result(
                            student=student,
                            course=course,
                            score=score,
                            grade=grade,
                        )
                    )

            Result.objects.bulk_create(
                result_objects,
                batch_size=1000,
            )

            # =========================================================
            # SUMMARY
            # =========================================================

            enrollment_count = Enrollment.objects.count()
            attendance_count = Attendance.objects.count()
            result_count = Result.objects.count()

            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    "APTECHSys demo data seeded successfully."
                )
            )

            self.stdout.write("")
            self.stdout.write("Demo login credentials:")
            self.stdout.write(
                "  Student : student_demo / Student@123"
            )
            self.stdout.write(
                "  Teacher : teacher_demo / Teacher@123"
            )
            self.stdout.write(
                "  Admin   : admin_demo / Admin@123"
            )

            self.stdout.write("")
            self.stdout.write(
                f"Students     : {Student.objects.count()}"
            )
            self.stdout.write(
                f"Teachers     : {Teacher.objects.count()}"
            )
            self.stdout.write(
                f"Admins       : {User.objects.filter(role='admin').count()}"
            )
            self.stdout.write(
                f"Departments  : {Department.objects.count()}"
            )
            self.stdout.write(
                f"Courses      : {Course.objects.count()}"
            )
            self.stdout.write(
                f"Enrollments  : {enrollment_count}"
            )
            self.stdout.write(
                f"Attendance   : {attendance_count}"
            )
            self.stdout.write(
                f"Results      : {result_count}"
            )

            self.stdout.write("")