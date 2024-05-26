from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # users

    # admin
   
    path('student-managament',views.student_management, name="student-managament" ),
    path('edit-student/<uuid:user_id>/',views.edit_student, name="edit-student" ),
    path('delete/<uuid:user_id>/', views.delete_user, name='delete-user'),

    # cases
    path('admin-case-management',views.case_management, name="admin-case-management" ),
    path('edit_case/<int:case_id>/', views.edit_case, name='edit_case'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete_case'),

    # reports
    path('reports/<int:case_id>/', views.reports, name='reports'),

]
