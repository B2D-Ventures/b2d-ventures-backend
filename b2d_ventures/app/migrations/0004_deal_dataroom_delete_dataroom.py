# Generated by Django 4.2.15 on 2024-08-31 03:47

import b2d_ventures.app.models.deal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0003_rename_type_user_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="deal",
            name="dataroom",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to=b2d_ventures.app.models.deal.dataroom_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    )
                ],
            ),
        ),
        migrations.DeleteModel(
            name="DataRoom",
        ),
    ]