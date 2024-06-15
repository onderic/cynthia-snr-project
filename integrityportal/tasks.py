
from django.core.mail import EmailMessage


def send_suspension_email(student_email, pdf, student_name):
    subject = 'Suspension Letter'
    message = f'Dear {student_name},\n\nPlease find the suspension letter attached.'
    from_email = 'your_email@example.com' 

    email = EmailMessage(subject, message, from_email, [student_email])
    email.attach('suspension_letter.pdf', pdf, 'application/pdf')

    email.send()