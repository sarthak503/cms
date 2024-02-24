from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsList.as_view(), name='student-list'),
    path('students/<str:pk>/', views.StudentDetail.as_view(), name='student-detail'),
]