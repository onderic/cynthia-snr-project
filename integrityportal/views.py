from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            # Admin role
            return render(request, 'admin/admin_dashboard.html')
        else:
            # Regular user role
            return render(request, 'student/index.html')
    else:
       pass


def case_management(request):
    return render(request, 'admin/case_management.html')


def student_management(request):
    return render(request, 'admin/students.html')