# Generated by Django 4.2.15 on 2024-08-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="type",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("investor", "Investor"),
                    ("startup", "Startup"),
                    ("unassigned", "Unassigned"),
                ],
                default="unassigned",
                max_length=20,
            ),
        ),
    ]