from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # users

    # admin
    path('admin-case-management',views.case_management, name="admin-case-management" ),
    path('student-managament',views.student_management, name="student-managament" )
]
