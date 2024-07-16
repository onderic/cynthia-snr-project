from django.core.mail import EmailMultiAlternatives
import threading

def send_suspension_letter_email(student_email, pdf_content):
    print(f"Preparing to send suspension letter email to {student_email}.")

    # Function to send the email
    def send_email():
        from_name = 'UEAB Discplinary'
        from_email = 'noreply@angoloexpert.com'
        
        email = EmailMultiAlternatives(
            subject='Suspension Letter',
            body='Please find attached your suspension letter.',
            from_email=f"{from_name} <{from_email}>",
            to=[student_email],
        )
    
        email.attach('suspension_letter.pdf', pdf_content, 'application/pdf')
        
        try:
            email.send(fail_silently=False)
            print(f"Suspension letter email sent to {student_email}.")
        except Exception as e:
            print(f"An error occurred while sending email to {student_email}: {e}")

    # Start the email sending in a separate thread
    email_thread = threading.Thread(target=send_email)
    email_thread.start()
