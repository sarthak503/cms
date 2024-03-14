#models.py

from django.db import models
from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


class Student(models.Model):
    rollno = models.CharField(primary_key=True, max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    batch = models.CharField(max_length=10)
    dept_choices = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering'),
        # Add more choices as needed
    ]
    dept = models.CharField(max_length=100, choices=dept_choices)
    year = models.CharField(max_length=2) 
    course_choices = [
        ('BT', 'BTech'),
        ('MT', 'MTech'),
        ('PhD', 'PhD')
    ]
    course = models.CharField(max_length=10, choices=course_choices)
    doj = models.DateField()
    sem = models.CharField(max_length=2) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rollno} - {self.first_name} {self.last_name}"

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    faculty_id = models.CharField(primary_key=True, max_length=20)
    phone_no = models.CharField(max_length=15)
    email_id = models.EmailField(unique=True)
    dept = models.CharField(max_length=100)
    specialisation = models.TextField() 
    role = models.TextField()  

    def __str__(self):
        return self.name
    



class Subject(models.Model):
    course_code = models.CharField(primary_key=True, max_length=10)
    subject_name = models.CharField(max_length=100)
    semester = models.PositiveSmallIntegerField()
    intended_for_choices = [
        ('BT', 'BTech'),
        ('MT', 'MTech'),
        ('PhD', 'PhD')
    ]
    intended_for = models.CharField(max_length=10, choices=intended_for_choices)
    credit = models.PositiveSmallIntegerField()
    teacher_id = models.CharField(max_length=20, null=True)
    dept_choices = [
        ('CSE', 'Computer Science and Engineering'),
        ('ECE', 'Electronics and Communication Engineering')
    ]
    dept = models.CharField(max_length=3, choices=dept_choices, default='CSE')

    def __str__(self):
        return self.subject_name

