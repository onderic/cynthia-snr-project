from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # users
    path('student-case/<uuid:id>/',views.student_case, name="student-case" ),
    path('case/<int:id>/', views.case_detail, name='case_detail'),

    # admin
   
    path('student-managament',views.student_management, name="student-managament" ),
    path('edit-student/<uuid:user_id>/',views.edit_student, name="edit-student" ),
    path('delete/<uuid:user_id>/', views.delete_user, name='delete-user'),

    path('add_office', views.add_office_view, name='add_office'),
    path('delete/<int:office_id>/', views.delete_office, name='delete_office'),

    
 

    # cases
    path('admin-case-management',views.case_management, name="admin-case-management" ),
    path('edit_case/<int:case_id>/', views.edit_case, name='edit_case'),
    path('delete_case/<int:case_id>/', views.delete_case, name='delete_case'),

    path('generate-suspension-pdf/<int:case_id>/', views.generate_suspension_pdf, name='generate_suspension_pdf'),

    path('download-suspension-pdf/', views.download_student_suspension_pdf, name='download_student_suspension_pdf'),

    # reports
    path('reports/<int:case_id>/', views.reports, name='reports'),

]
