# Generated by Django 4.1.7 on 2023-10-26 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0010_remove_user_user_supervisor_user_supervisor"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="supervisor",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="supervisor",
                to="user.supervisor",
            ),
        ),
    ]
