# Generated by Django 4.1.7 on 2023-10-13 18:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_supervisor_phone_note_email_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="document",
            field=models.FileField(
                default=False, upload_to="documents", verbose_name="document"
            ),
        ),
    ]