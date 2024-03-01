
from rest_framework import serializers
from .models import Student, Subject

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        extra_kwargs = {
            'teacher_id': {'required': False}  # Make teacher_id not required
        }