import os
from django.utils import timezone
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CaseForm
from .models import Case, Office, SuspensionLetter
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.units import cm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO
from .mail import send_suspension_letter_email 


@login_required
def index(request):
    if request.user.is_staff:
        students_count = User.objects.filter(user_type='student').count()
        administrators_count = User.objects.filter(user_type='admin').count()
        cases_count = Case.objects.all().count()
        cases = Case.objects.all().order_by('-date_reported')[:10]

        context = {
            'cases': cases,
            'cases_count': cases_count,
            'students_count': students_count,
            'administrators_count': administrators_count,
        }
        return render(request, 'admin/admin_dashboard.html', context)
    else:
        student = get_object_or_404(User, pk=request.user.pk)
        student_case_count = Case.objects.filter(student_id=student).count()
        cases = Case.objects.filter(student_id=student).order_by('-date_reported')[:5]
        return render(request, 'student/index.html', {'student_case_count': student_case_count,"cases":cases})
    

@user_passes_test(lambda u: u.is_superuser)
@login_required
def generate_suspension_pdf(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    student = case.student_id

    existing_letter = SuspensionLetter.objects.filter(student=student, case=case).first()
    if existing_letter:
        print(f"A suspension letter for this case already exists for {student.first_name}.")

    current_date = timezone.now().strftime('%B %d, %Y')

    # Create a buffer to hold the PDF
    buffer = BytesIO()
    p = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=cm, leftMargin=cm, topMargin=cm, bottomMargin=cm)

    # Define styles for the PDF
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=18, leading=22, spaceAfter=14, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle(name='Subtitle', fontSize=14, leading=18, spaceAfter=10, fontName='Helvetica-Bold')
    body_style = ParagraphStyle(name='Body', fontSize=12, leading=15, spaceAfter=12)

    elements = []

    # Header with Logo and Title
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, 'logo', 'logo.png')
    logo = Image(logo_path, width=60, height=40) 

    header_table = Table([[logo, Paragraph("Suspension Letter", title_style)]])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 1 * cm))

    # Student Details
    elements.append(Paragraph("Student Details", subtitle_style))
    elements.append(Paragraph(f"Name: {student.first_name} {student.last_name}", body_style))
    elements.append(Paragraph(f"ID: {student.student_id}", body_style))
    elements.append(Paragraph(f"Email: {student.email}", body_style))
    elements.append(Paragraph(f"Date: {current_date}", body_style))
    elements.append(Spacer(1, 1 * cm))

    # Suspension Message
    elements.append(Paragraph("Suspension Message", subtitle_style))
    elements.append(Paragraph(f"Dear {student.first_name} {student.last_name},", body_style))
    elements.append(Paragraph(
        "We regret to inform you that due to recent incidents and violations of school policies, "
        "you have been suspended from school for a period of two weeks, effective immediately. "
        "Please contact the school administration for further details and to discuss the terms of your suspension.",
        body_style))
    elements.append(Paragraph(
        "During this period, it is expected that you refrain from attending any school-related activities, "
        "including classes and extracurricular activities. It is important to adhere to the terms outlined "
        "in this suspension letter to ensure a smooth resolution of this matter.",
        body_style))
    elements.append(Paragraph(
        "If there are any questions or concerns regarding this decision, please do not hesitate to contact "
        "the school administration at your earliest convenience.",
        body_style))
    elements.append(Spacer(1, 1 * cm))

    # Resignation Message
    elements.append(Paragraph("Resignation Message", subtitle_style))
    elements.append(Paragraph(
        "If you have any concerns or wish to discuss the suspension, you may reach out to the "
        "principal's office during working hours. We hope to resolve this matter amicably and "
        "look forward to your cooperation.",
        body_style))
    elements.append(Paragraph(
        "Please acknowledge receipt of this letter by signing and returning the attached acknowledgment form. "
        "Your prompt attention to this matter is appreciated.",
        body_style))
    elements.append(Paragraph(
        f"<strong>Sincerely</strong>,<br/>{request.user.first_name} {request.user.last_name}<br/>{request.user.email}",
        body_style))

    # Build the PDF
    p.build(elements)


    # if not existing_letter:
    letter_content = "\n".join([element.text for element in elements if isinstance(element, Paragraph)])
    SuspensionLetter.objects.create(student=student, case=case, content=letter_content)
    pdf_content = buffer.getvalue() 
    send_suspension_letter_email(student.email, pdf_content)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="suspension_letter.pdf"'

    print("PDF generated and response sent.")
    return response



@login_required
def download_student_suspension_pdf(request):
    student = request.user

    current_date = timezone.now().strftime('%B %d, %Y')

    # Create a buffer to hold the PDF
    buffer = BytesIO()
    p = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

    # Define styles for the PDF
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name='Title', fontSize=18, leading=22, spaceAfter=14, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle(name='Subtitle', fontSize=14, leading=18, spaceAfter=10, fontName='Helvetica-Bold')
    body_style = ParagraphStyle(name='Body', fontSize=12, leading=15, spaceAfter=12)

    elements = []

    # Header with Logo and Title
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(current_dir, 'logo', 'logo.png')
    logo = Image(logo_path, width=60, height=40)  # Adjusted size

    header_table = Table([[logo, Paragraph("Suspension Letter", title_style)]])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 1 * cm))

    # Student Details
    elements.append(Paragraph("Student Details", subtitle_style))
    elements.append(Paragraph(f"Name: {student.first_name} {student.last_name}", body_style))
    elements.append(Paragraph(f"ID: {student.student_id}", body_style))
    elements.append(Paragraph(f"Email: {student.email}", body_style))
    elements.append(Paragraph(f"Date: {current_date}", body_style))
    elements.append(Spacer(1, 1 * cm))

    # Suspension Message
    elements.append(Paragraph("Suspension Message", subtitle_style))
    elements.append(Paragraph(f"Dear {student.first_name} {student.last_name},", body_style))
    elements.append(Paragraph(
        "We regret to inform you that due to recent incidents and violations of school policies, "
        "you have been suspended from school for a period of two weeks, effective immediately. "
        "Please contact the school administration for further details and to discuss the terms of your suspension.",
        body_style))
    elements.append(Paragraph(
        "During this period, it is expected that you refrain from attending any school-related activities, "
        "including classes and extracurricular activities. It is important to adhere to the terms outlined "
        "in this suspension letter to ensure a smooth resolution of this matter.",
        body_style))
    elements.append(Paragraph(
        "If there are any questions or concerns regarding this decision, please do not hesitate to contact "
        "the school administration at your earliest convenience.",
        body_style))
    elements.append(Spacer(1, 1 * cm))

    # Resignation Message
    elements.append(Paragraph("Resignation Message", subtitle_style))
    elements.append(Paragraph(
        "If you have any concerns or wish to discuss the suspension, you may reach out to the "
        "principal's office during working hours. We hope to resolve this matter amicably and "
        "look forward to your cooperation.",
        body_style))
    elements.append(Paragraph(
        "Please acknowledge receipt of this letter by signing and returning the attached acknowledgment form. "
        "Your prompt attention to this matter is appreciated.",
        body_style))
    elements.append(Paragraph(
        f"<strong>Sincerely</strong>,<br/>{request.user.first_name} {request.user.last_name}<br/>{request.user.email}",
        body_style))

    # Build the PDF
    p.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="suspension_letter.pdf"'

    print("PDF generated and response sent.")
    return response


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
            return render(request, 'admin/student/students.html', {'users': users})

    except Exception as e:
        print("An error occurred:", e)
        messages.error(request, f'An error occurred: {e}')
        return render(request, 'admin/student/students.html', {'users': users}) 


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

        return render(request, 'admin/student/edit_student.html', {'user': user})

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
        try:
            if form.is_valid():
                case = form.save(commit=False)
                case.student = request.user
                case.save()
                messages.success(request, 'Case reported successfully.')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
    else:
        form = CaseForm()
    
    # Fetch students and cases
    students = User.objects.filter(user_type='student').order_by('-created_at')
    offices = Office.objects.all()
    cases = Case.objects.all().order_by('-date_reported')

    return render(request, 'admin/cases/case_management.html', {"form": form,"offices":offices, "students": students, "cases": cases})


@user_passes_test(lambda u: u.is_superuser)
def edit_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        try:
            case.case_title = request.POST.get('case_title')
            case.description = request.POST.get('description')
            case.hearing_date = request.POST.get('hearing_date')
            case.status = request.POST.get('status')
            case.resolution = request.POST.get('resolution')
            case.decision = request.POST.get('decision')

            office_id = request.POST.get('office')
            if office_id:
                office = Office.objects.get(id=office_id)
                case.office = office

            case.save()
            
            messages.success(request, 'Case updated successfully.')
            return redirect('admin-case-management')
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            return redirect('admin-case-management')
    else:
        form = CaseForm(instance=case)

        offices = Office.objects.all()
    
    return render(request, 'admin/cases/edit_case.html', {"form": form, "case": case, 'offices': offices})


@user_passes_test(lambda u: u.is_superuser)
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    try:
        case.delete()
        messages.success(request, 'Case deleted successfully.')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
    
    return redirect('admin-case-management')

@user_passes_test(lambda u: u.is_superuser)
def reports(request,case_id):
    case = get_object_or_404(Case, id=case_id)
    student = case.student_id 
    return render(request, 'admin/cases/reports.html', {
        'case': case,
        'student': student,
    })


def student_case(request, id):
    student = get_object_or_404(User, id=id)
    cases = Case.objects.filter(student_id=id)
    return render(request, 'student/case.html', {'cases': cases, 'student': student})


def case_detail(request, id):
    case = get_object_or_404(Case, id=id)
    office = case.office 
    
    context = {
        'case': case,
        'office': office,
    }
    return render(request, 'student/case_detail.html', context)


@csrf_exempt
def add_office_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        office_head = request.POST.get('office_head')
        contact_email = request.POST.get('contact_email')
        
        # Create the office
        Office.objects.create(name=name, office_head=office_head, contact_email=contact_email)
        
        return redirect('add_office') 

    offices = Office.objects.all()
    return render(request, 'admin/office.html', {'offices': offices})


@csrf_exempt
def delete_office(request, office_id):
    if request.method == 'POST':
        office = get_object_or_404(Office, id=office_id)
        office.delete()
        messages.success(request, 'Office deleted successfully.')
    
    return redirect('add_office') 


