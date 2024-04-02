# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Student,Subject,Faculty,Role,Attendance
from django.shortcuts import get_object_or_404
from .serializers import StudentSerializer,SubjectSerializer,FacultySerializer,RoleSerializer,AttendanceSerializer
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


@api_view(['GET'])
def get_user_type(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'error': 'Email parameter is missing'}, status=400)

    try:
        role = Role.objects.get(emailid=email)
        user_type = role.user_type
        
        if user_type == 1:  # If user is an admin
            return JsonResponse({'user_type': user_type})
        elif user_type == 2:  # If user is a student
            student = Student.objects.get(email=email)
            serializer = StudentSerializer(student)
            return JsonResponse({'user_type': user_type, 'details': serializer.data})
        elif user_type == 3:  # If user is a faculty
            faculty = Faculty.objects.get(email_id=email)
            serializer = FacultySerializer(faculty)
            return JsonResponse({'user_type': user_type, 'details': serializer.data})
        else:
            return JsonResponse({'error': 'User not found or user type is invalid'}, status=404)
    except Role.DoesNotExist:
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
    lookup_url_kwarg = 'lookup'  # Custom lookup URL keyword argument

    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_url_kwarg)
        
        # Check if the lookup value is an email
        if '@' in lookup_value:
            return get_object_or_404(self.queryset, email_id=lookup_value)
        else:  # Assume it's a faculty ID
            return get_object_or_404(self.queryset, faculty_id=lookup_value)

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
        intended_for = request.GET.get('intended_for', '')

        # Filter based on dept and intended_for regardless of other parameters
        filters = {'dept': dept, 'intended_for': intended_for}

        # Check if semester is provided
        semester = request.GET.get('semester', None)
        if semester:
            filters['semester'] = semester

        # Check if facultyid is provided
        faculty_id = request.GET.get('facultyid', None)
        if faculty_id:
            filters['teacher_id'] = faculty_id
        else:
            # If facultyid is not provided, remove it from the filters
            filters.pop('teacher_id', None)

        filtered_subjects = Subject.objects.filter(**filters)

        subjects_list = list(filtered_subjects.values())

        # If no semester or facultyid is provided, return all subjects based on dept and intended_for
        if not semester and not faculty_id:
            all_filtered_subjects = Subject.objects.filter(dept=dept, intended_for=intended_for)
            all_subjects_list = list(all_filtered_subjects.values())
            return JsonResponse(all_subjects_list, safe=False)

        return JsonResponse(subjects_list, safe=False)
    

def filter_students(request):
    if request.method == 'GET':
        dept = request.GET.get('dept', '')
        sem = request.GET.get('sem', '')
        course = request.GET.get('course', '')

        filters = {}

        if dept:
            filters['dept'] = dept
        if sem:
            filters['sem'] = sem
        if course:
            filters['course'] = course

        filtered_students = Student.objects.filter(**filters)

        students_list = list(filtered_students.values())

        return JsonResponse(students_list, safe=False)
    


class BulkAttendanceUpload(APIView):
    def post(self, request):
        attendance_data = request.data  # Assuming the frontend sends an array of attendance objects
        errors = []
        for data in attendance_data:
            serializer = AttendanceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                errors.append(serializer.errors)
        
        if errors:
            return Response({"errors": errors}, status=400)
        else:
            return Response({"message": "Attendance uploaded successfully"}, status=200)

class AttendanceDetailView(APIView):
    def delete(self, request, pk):
        try:
            attendance = Attendance.objects.get(pk=pk)
            attendance.delete()
            return Response({"message": "Attendance deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Attendance.DoesNotExist:
            return Response({"error": "Attendance not found"}, status=status.HTTP_404_NOT_FOUND)


class AttendanceListView(APIView):
    def get(self, request):
        student_id = request.query_params.get('student_id')
        subject_id = request.query_params.get('subject_id')
        date = request.query_params.get('date')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if student_id and subject_id and date:
            attendance = Attendance.objects.filter(student_id=student_id, subject_id=subject_id, date=date).first()
            serializer = AttendanceSerializer(attendance)
            return Response(serializer.data)

        if student_id and subject_id and start_date and end_date:
            attendance = Attendance.objects.filter(student_id=student_id, subject_id=subject_id, date__range=[start_date, end_date])
            serializer = AttendanceSerializer(attendance, many=True)
            return Response(serializer.data)

from datetime import datetime
        
def attendance_list(request):
    if request.method == 'GET':
        subject_id = request.GET.get('subject_id')
        date_str = request.GET.get('date')

        if subject_id is None or date_str is None:
            return JsonResponse({'error': 'Both subject_id and date are required.'}, status=400)

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        attendance = Attendance.objects.filter(subject_id=subject_id, date=date)
        serializer = AttendanceSerializer(attendance, many=True)

        return JsonResponse({'attendance': serializer.data})

    return JsonResponse({'error': 'Method not allowed.'}, status=405)