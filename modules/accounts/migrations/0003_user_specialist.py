# Generated by Django 4.1.7 on 2023-05-08 03:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_slot"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="specialist",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]