from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsList.as_view(), name='student-list'),
    path('students/<str:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('subjects/', views.SubjectList.as_view(), name='subject-list'),
    path('subjects/<str:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),
    path('upload-students-csv/', views.upload_students_csv, name='upload_students_csv'),

]