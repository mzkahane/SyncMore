# Generated by Django 4.1.7 on 2023-10-26 03:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0007_alter_document_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="supervisor",
            name="name",
            field=models.CharField(default="Zac", max_length=30, verbose_name="name"),
        ),
    ]