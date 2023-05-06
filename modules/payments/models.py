from django.db import models

from modules.accounts.models import User


class Payment(models.Model):
    class Status(models.TextChoices):
        INITIATED = ("initiated", "Initiated")
        PROCESSING = ("processing", "Processing")
        SUCCESS = ("success", "Success")
        FAILED = ("failed", "Failed")

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    payment_id = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=50, blank=True, unique=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.INITIATED)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = "payments"

    def __str__(self) -> str:
        return str(self.id)