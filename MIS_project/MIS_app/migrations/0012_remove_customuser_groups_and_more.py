# Generated by Django 5.0.2 on 2024-03-14 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_app', '0011_customuser_admin_faculty_user_student_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='student',
            name='user',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='user',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]