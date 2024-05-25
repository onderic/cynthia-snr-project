from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CaseForm
from .models import Case



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



@user_passes_test(lambda u: u.is_superuser)
@login_required
def student_management(request):
    users = User.objects.filter(user_type='student').order_by('-created_at')
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            student_id = request.POST.get('student_id')
            user_type = request.POST.get('user_type')

            if user_type == 'student':
                password = student_id
            else:
                password = None

            user = User.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                student_id=student_id,
                user_type=user_type,
                password=password
            )
            messages.success(request, 'User created successfully.')

            return redirect('student-managament')
        

        else:
            return render(request, 'admin/students.html', {'users': users})

    except Exception as e:
        print("An error occurred:", e)
        messages.error(request, f'An error occurred: {e}')
        return render(request, 'admin/students.html', {'users': users}) 


@user_passes_test(lambda u: u.is_superuser)
@login_required
def edit_student(request, user_id):
    try:
        user = User.objects.get(pk=user_id)

        if request.method == 'POST':
            user.email = request.POST.get('email')
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.student_id = request.POST.get('student_id')
            user.user_type = request.POST.get('user_type')

            if user.user_type == 'student':
                user.set_password(user.student_id)
            else:
                user.set_unusable_password()

            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('student-managament')

        return render(request, 'admin/edit_student.html', {'user': user})

    except User.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('student-managament')
    except Exception as e:
        print("An error occurred:", e)
        messages.error(request, f'An error occurred: {e}')
        return redirect('student-managament')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        try:
            user.delete()
            messages.success(request, 'User deleted successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    return redirect('student-managament')


@user_passes_test(lambda u: u.is_superuser)
def case_management(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        print(form)
        if form.is_valid():
            case = form.save(commit=False)
            case.student = request.user
            case.save()
            messages.success(request, 'Case reported successfully.')
    else:
        form = CaseForm()
        messages.error(request, "something went wrong")
    students = User.objects.filter(user_type='student').order_by('-created_at')
    cases = Case.objects.all().order_by('-date_reported')
    return render(request, 'admin/case_management.html', {"form": form, "students": students, "cases":cases})
