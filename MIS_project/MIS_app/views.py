# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Student,Subject,Faculty,Role
from django.shortcuts import get_object_or_404
from .serializers import StudentSerializer,SubjectSerializer,FacultySerializer,RoleSerializer
from django.http import JsonResponse
import csv
from django.views.decorators.csrf import csrf_exempt



class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Role created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_user_type(request):
    #print(request.GET.get('email'))   Print the entire GET dictionary for debugging
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        role = Role.objects.get(emailid=email)
        user_type = role.user_type # Get the display value of the user type
        return JsonResponse({'user_type': user_type})
    except Role.DoesNotExist as e:
        print(f"User not found for email: {email}. Error: {e}")
        return JsonResponse({'error': 'User not found'}, status=404)

# def get_rollno_from_email(request):
#     if request.method == 'GET':
#         email = request.GET.get('email', None)
#         if email:
#             try:
#                 role = Role.objects.get(emailid=email, user_type=2)
#                 student = Student.objects.get(email=email)
#                 return JsonResponse({'rollno': student.rollno})
#             except Role.DoesNotExist:
#                 return JsonResponse({'error': 'User not found or not a student'}, status=404)
#             except Student.DoesNotExist:
#                 return JsonResponse({'error': 'Student not found for this email'}, status=404)
#         else:
#             return JsonResponse({'error': 'Email parameter is missing'}, status=400)
#     else:
#         return JsonResponse({'error': 'Only GET method is allowed'}, status=405)


@csrf_exempt
def upload_students_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Student.objects.create(
                rollno=row['rollno'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                dob=row['dob'],
                address=row['address'],
                phone=row['phone'],
                gender=row['gender'],
                batch=row['batch'],
                dept=row['dept'],
                year=row['year'],
                course=row['course'],
                doj=row['doj'],
                sem=row['sem']
            )
            # Create Role entry for the student
            Role.objects.create(emailid=row['email'], user_type=2)

        return JsonResponse({'message': 'Data from CSV file uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

class StudentsList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Create Role entry for the student
        Role.objects.create(emailid=request.data['email'], user_type=2)
        return Response({"message": "Student created successfully"}, status=status.HTTP_201_CREATED)

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_url_kwarg = 'lookup'  # Custom lookup URL keyword argument

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_url_kwarg)
        if lookup_value.isdigit():  # Check if the lookup value is a digit (assuming it's a rollno)
            return get_object_or_404(self.queryset, rollno=lookup_value)
        else:  # If it's not a digit, assume it's an email
            return get_object_or_404(self.queryset, email=lookup_value)


# FACULTY SECTION
@csrf_exempt
def upload_faculty_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Faculty.objects.create(
                name=row['name'],
                faculty_id=row['faculty_id'],
                phone_no=row['phone_no'],
                email_id=row['email_id'],
                dept=row['dept'],
                specialisation=row['specialisation'],
                role=row['role']
            )
            # Create Role entry for the faculty
            Role.objects.create(emailid=row['email_id'], user_type=3)

        return JsonResponse({'message': 'Data from CSV file uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

class FacultyList(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Create Role entry for the faculty
        Role.objects.create(emailid=request.data['email_id'], user_type=3)
        return Response({"message": "Faculty created successfully"}, status=status.HTTP_201_CREATED)

class FacultyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Faculty updated successfully"})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Faculty deleted successfully"})



# SUBJECT SECTION STARTS


@csrf_exempt
def upload_subjects_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            Subject.objects.create(
                course_code=row['course_code'],
                subject_name=row['subject_name'],
                semester=row['semester'],
                intended_for=row['intended_for'],
                credit=row['credit'],
                teacher_id=row.get('teacher_id', None)  # Handle null value for teacher_id
            )

        return JsonResponse({'message': 'Data from CSV file uploaded successfully'}, status=200)
    else:
        return JsonResponse({'error': 'No file uploaded'}, status=400)
    
    
class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save serializer data without calling perform_create
        return Response({"message": "Subject created successfully"}, status=status.HTTP_201_CREATED)
    
class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Save serializer data without calling perform_update
        return Response({"message": "Subject updated successfully"})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Subject deleted successfully"})
    


def filter_subjects(request):
    if request.method == 'GET':
        dept = request.GET.get('dept', '')
        semester = request.GET.get('semester', '')
        intended_for = request.GET.get('intended_for', '')

        filtered_subjects = Subject.objects.filter(dept=dept, semester=semester, intended_for=intended_for)

        subjects_list = list(filtered_subjects.values())

        return JsonResponse(subjects_list, safe=False)

    


from .models import Attendance
from .serializers import AttendanceSerializer

@api_view(['POST'])
def mark_attendance(request):
    if request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Attendance marked successfully"}, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_student_attendance(request, student_id):
    if request.method == 'GET':
        attendance_records = Attendance.objects.filter(student_id=student_id)
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_subject_attendance(request, subject_id):
    if request.method == 'GET':
        attendance_records = Attendance.objects.filter(subject_id=subject_id)
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)
