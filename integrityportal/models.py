from django.db import models
from accounts.models import User

class Case(models.Model):
    CASE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]

    student_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    case_title = models.CharField(max_length=255)
    description = models.TextField()
    hearing_date = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='open')
    resolution = models.TextField(blank=True, null=True)
    date_resolved = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.case_title
