from django.db import models
from accounts.models import User
from django.utils import timezone

class Case(models.Model):
    CASE_STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In Progress'),
    ]

    DECISION_CHOICES = [
            ('no_decision', 'No Decision'),
            ('suspended', 'Suspended'),
            ('probation', 'Probation'),
            ('forgiven', 'Forgiven'),
        ]



    student_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    case_title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    hearing_date = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES, default='open')
    resolution = models.TextField(blank=True, null=True)
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, default='no_decision')
    date_resolved = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == 'closed' and self.date_resolved is None:
            self.date_resolved = timezone.now()
        elif self.status != 'closed':
            self.date_resolved = None
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return self.case_title
