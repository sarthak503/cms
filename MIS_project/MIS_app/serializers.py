#serializers.py
from rest_framework import serializers
from .models import Student, Subject,Role, Faculty,Attendance

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

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['emailid', 'user_type']



class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Optionally customize the representation if needed
        return representation

    def create(self, validated_data):
        return Attendance.objects.create(**validated_data)

