# views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Student,Subject,Faculty
from .serializers import StudentSerializer,SubjectSerializer,FacultySerializer
from django.http import JsonResponse
import csv
from django.views.decorators.csrf import csrf_exempt

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
        return Response({"message": "Student created successfully"}, status=status.HTTP_201_CREATED)

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Student updated successfully"})

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Student deleted successfully"})

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
