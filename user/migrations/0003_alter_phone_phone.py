# Generated by Django 4.2.8 on 2023-12-07 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_alter_phone_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phone",
            name="phone",
            field=models.CharField(
                default="1234567890", max_length=20, null=True, verbose_name="phone"
            ),
        ),
    ]