# Generated by Django 4.2.15 on 2024-09-29 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0007_alter_deal_image_background_alter_deal_image_content_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="meeting",
            options={"ordering": ["-start_time"]},
        ),
        migrations.RemoveField(
            model_name="meeting",
            name="date",
        ),
        migrations.RemoveField(
            model_name="meeting",
            name="status",
        ),
        migrations.AddField(
            model_name="meeting",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="end_time",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="investor_event_id",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="start_time",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="meeting",
            name="title",
            field=models.CharField(default="Investor-Startup Meeting", max_length=255),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="investor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meetings",
                to="app.investor",
            ),
        ),
        migrations.AlterField(
            model_name="meeting",
            name="startup",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="meetings",
                to="app.startup",
            ),
        ),
    ]