from django.db import models

from users.models import User


class Schedules(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        db_table = "schedules"

    def __str__(self) -> str:
        return str(self.id)