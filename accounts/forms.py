from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from django.db import transaction
from django.utils import timezone

from academics.models import Department, Course
from students.models import Student
from teacher.models import Teacher


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username", 
        widget= forms.TextInput(
            attrs={
                "placeholder": "Enter your username",
                "autofocus": True
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget= forms.PasswordInput(
            attrs = {
            "placeholder": "Enter your password",
        })
    )

class DepartmentAdminForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = [
            "name",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Computer Science",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Brief description of the department",
                }
            ),
        }


class CourseAdminForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            "name",
            "code",
            "department",
            "teacher",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Web Development",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. WEB201",
                }
            ),
            "department": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "teacher": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["department"].queryset = (
            Department.objects
            .order_by("name")
        )

        self.fields["teacher"].queryset = (
            Teacher.objects
            .select_related("user")
            .order_by(
                "user__last_name",
                "user__first_name",
            )
        )

        self.fields["teacher"].empty_label = "No teacher assigned"


class StudentAdminForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Login username",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "student@example.com",
            }
        ),
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }
        ),
    )

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )

    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        ),
    )

    student_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. STU2026001",
            }
        ),
    )

    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone number",
            }
        ),
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address",
            }
        ),
    )

    admission_date = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "A user with this username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip()

        if Student.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError(
                "A student with this ID already exists."
            )

        return student_id

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match.",
            )

        return cleaned_data


class TeacherAdminForm(forms.Form):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Login username",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "teacher@example.com",
            }
        ),
    )

    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First name",
            }
        ),
    )

    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last name",
            }
        ),
    )

    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )

    confirm_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password",
            }
        ),
    )

    employee_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. EMP2026001",
            }
        ),
    )

    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone number",
            }
        ),
    )

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address",
            }
        ),
    )

    specialization = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. Database Systems",
            }
        ),
    )

    date_joined = forms.DateField(
        initial=timezone.localdate,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    def clean_username(self):
        username = self.cleaned_data["username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(
                "A user with this username already exists."
            )

        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"].strip()

        if Teacher.objects.filter(employee_id=employee_id).exists():
            raise forms.ValidationError(
                "A teacher with this employee ID already exists."
            )

        return employee_id

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match.",
            )

        return cleaned_data

    @transaction.atomic
    def save(self):

        data = self.cleaned_data

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
            role="teacher",
        )

        return Teacher.objects.create(
            user=user,
            employee_id=data["employee_id"],
            phone=data["phone"],
            address=data["address"],
            specialization=data["specialization"],
            date_joined=data["date_joined"],
        )