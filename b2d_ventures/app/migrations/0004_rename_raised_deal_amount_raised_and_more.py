# Generated by Django 4.2.15 on 2024-11-13 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_alter_user_refresh_token"),
    ]

    operations = [
        migrations.RenameField(
            model_name="deal",
            old_name="raised",
            new_name="amount_raised",
        ),
        migrations.RenameField(
            model_name="deal",
            old_name="allocation",
            new_name="target_amount",
        ),
    ]
