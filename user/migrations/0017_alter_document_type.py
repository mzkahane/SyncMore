# Generated by Django 4.2.5 on 2023-11-17 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_document_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('Other', 'Other'), ('ID', 'ID'), ('Passport', 'Passport'), ('SSN', 'SSN'), ('Birth Certificate', 'Birth Certificate'), ('Housing', 'Housing'), ('Financial', 'Financial'), ('Insurance', 'Insurance')], default='Other', max_length=32, null=True, verbose_name='type'),
        ),
    ]