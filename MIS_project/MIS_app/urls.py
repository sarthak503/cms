from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentsList.as_view(), name='student-list'),
    path('subjects/', views.SubjectList.as_view(), name='subject-list'),
    path('subjects/<str:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),
    path('upload-students-csv/', views.upload_students_csv, name='upload_students_csv'),
    path('upload-subjects-csv/', views.upload_subjects_csv, name='upload_subjects_csv'),
    path('faculty/', views.FacultyList.as_view(), name='faculty-list-create'),
    path('upload-faculty-csv/', views.upload_faculty_csv, name='upload-faculty-csv'),
    path('filter/', views.filter_subjects, name='filter_subjects'),
    path('roles/', views.RoleList.as_view(), name='role-list'),
    path('get-user-type/', views.get_user_type, name='get-user-type'),
    path('students/<str:lookup>/', views.StudentDetail.as_view(), name='student_detail'),
    path('faculty/<str:lookup>/', views.FacultyDetail.as_view(), name='faculty_detail'),
    path('filter-students/', views.filter_students, name='filter_students'),
    path('bulk-attendance-upload/', views.BulkAttendanceUpload.as_view(), name='bulk-attendance-upload'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('attendance/', views.AttendanceListView.as_view(), name='attendance-list'),






]

    