from django.contrib import admin
from .models import Case

# Register your models here.

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ('id', 'student_id', 'case_title', 'hearing_date')
    # Fields to search in the admin list view
    search_fields = ('case_title', 'description', 'student__student_id', 'student__first_name', 'student__last_name')
  
    # Fields to display in the admin form view
    fields = ('student', 'case_title', 'hearing_date', 'description')
   

# You can also register the model without a custom admin class like this:
# admin.site.register(Case)
