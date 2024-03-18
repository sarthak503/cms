# Generated by Django 5.0.3 on 2024-03-15 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIS_app', '0012_remove_customuser_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailid', models.EmailField(max_length=254, unique=True)),
                ('user_type', models.PositiveSmallIntegerField(choices=[(1, 'Admin'), (2, 'Student'), (3, 'Faculty')])),
            ],
        ),
    ]