# Generated by Django 5.0.2 on 2024-02-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=models.CharField(choices=[('CSE', 'Computer Science and Engineering'), ('ECE', 'Electronics and Communication Engineering')], max_length=100),
        ),
    ]
