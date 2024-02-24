from django.db import models

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
    year = models.PositiveSmallIntegerField()
    course_choices = [
        ('BT', 'BTech'),
        ('MT', 'MTech'),
        ('PhD', 'PhD')
    ]
    course = models.CharField(max_length=10, choices=course_choices)
    doj = models.DateField()
    sem = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rollno} - {self.first_name} {self.last_name}"


# class Subject(models.Model):
#     subject_name = models.CharField(max_length=100)
#     course_code = models.CharField(max_length=10)
#     semester = models.PositiveSmallIntegerField()
#     intended_for_choices = [
#         ('BT', 'BTech'),
#         ('MT', 'MTech'),
#         ('PhD', 'PhD')
#     ]
#     intended_for = models.CharField(max_length=10, choices=intended_for_choices)

#     def __str__(self):
#         return self.subject_name