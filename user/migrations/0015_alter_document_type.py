# Generated by Django 4.1.7 on 2023-11-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0014_alter_user_second_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="type",
            field=models.CharField(
                choices=[("type1", "Type 1"), ("type2", "Type 2")],
                default="ID",
                max_length=32,
                null=True,
                verbose_name="type",
            ),
        ),
    ]