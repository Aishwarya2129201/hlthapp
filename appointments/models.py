from django.db import models
from users.models import User


class Appointment(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = ("confirmed", "Confirmed")
        CANCELLED = ("cancelled", "Cancelled")
        RESCHEDULED = ("rescheduled", "Re-Scheduled")

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_appointments"
    )
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_appointments"
    )
    scheduled_on = models.DateTimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appointments"

    def __str__(self) -> str:
        return str(self.id)
