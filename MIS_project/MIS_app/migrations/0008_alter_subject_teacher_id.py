# Generated by Django 5.0.2 on 2024-02-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_app', '0007_alter_student_sem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='teacher_id',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
