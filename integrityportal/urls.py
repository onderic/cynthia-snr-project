from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # users

    # admin
    path('admin-case-management',views.case_management, name="admin-case-management" ),
    path('student-managament',views.student_management, name="student-managament" ),
    path('edit-student/<uuid:user_id>/',views.edit_student, name="edit-student" ),
    path('delete/<uuid:user_id>/', views.delete_user, name='delete-user'),
]
