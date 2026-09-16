from django.db import models
from django.conf import settings
from django.utils import timezone


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name="teacher_profile"
        )
    employee_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"
