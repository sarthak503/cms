# Generated by Django 5.0.2 on 2024-02-25 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_app', '0003_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='id',
        ),
        migrations.AlterField(
            model_name='subject',
            name='course_code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
