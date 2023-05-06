# Generated by Django 4.1.7 on 2023-05-06 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("payments", "0003_alter_payment_transaction_id"),
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="scheduled_on",
        ),
        migrations.AddField(
            model_name="appointment",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="appointment",
            name="end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="appointment",
            name="payment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="payments.payment",
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="start_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]