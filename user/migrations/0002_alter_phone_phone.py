# Generated by Django 4.2.8 on 2023-12-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phone",
            name="phone",
            field=models.IntegerField(
                default=0, max_length=20, null=True, verbose_name="phone"
            ),
        ),
    ]
