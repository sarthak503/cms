from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsList.as_view(), name='student-list'),
    path('students/<str:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('subjects/', views.SubjectList.as_view(), name='subject-list'),
    path('subjects/<str:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),
    path('upload-students-csv/', views.upload_students_csv, name='upload_students_csv'),
    path('upload-subjects-csv/', views.upload_subjects_csv, name='upload_subjects_csv'),
    path('faculty/', views.FacultyList.as_view(), name='faculty-list-create'),
    path('faculty/<str:pk>/', views.FacultyDetail.as_view(), name='faculty-retrieve-update-destroy'),
    path('upload-faculty-csv/', views.upload_faculty_csv, name='upload-faculty-csv'),

]