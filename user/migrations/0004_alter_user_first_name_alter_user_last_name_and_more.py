# Generated by Django 4.1.7 on 2023-09-29 16:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_alter_user_address"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="First_Name",
            field=models.CharField(max_length=30, null=True, verbose_name="First_Name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="Last_Name",
            field=models.CharField(max_length=30, null=True, verbose_name="Last_Name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(
                default="San Francisco",
                max_length=255,
                null=True,
                verbose_name="address",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="created_time",
            field=models.DateTimeField(
                auto_now_add=True, null=True, verbose_name="created_time"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.CharField(
                default=None, max_length=30, null=True, verbose_name="email"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                default=None, max_length=6, null=True, verbose_name="gender"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_active",
            field=models.BooleanField(
                default=True, null=True, verbose_name="is_active"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.IntegerField(default=0, null=True, verbose_name="phone"),
        ),
    ]