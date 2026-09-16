from django.db import models
from django.conf import settings
from django.utils import timezone


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="student_profile"
        )
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    admission_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
