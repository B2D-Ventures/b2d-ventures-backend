# Generated by Django 4.2.15 on 2024-11-04 13:12

import b2d_ventures.app.models.deal
import cloudinary_storage.storage
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0009_user_refresh_token"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deal",
            name="dataroom",
            field=models.FileField(
                blank=True,
                null=True,
                storage=cloudinary_storage.storage.RawMediaCloudinaryStorage(),
                upload_to=b2d_ventures.app.models.deal.dataroom_upload_path,
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=["pdf"]
                    )
                ],
            ),
        ),
    ]