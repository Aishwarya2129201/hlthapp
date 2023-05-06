from django.db import models
from modules.accounts.models import User
from modules.payments.models import Payment


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
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "appointments"

    def __str__(self) -> str:
        return str(self.id)
