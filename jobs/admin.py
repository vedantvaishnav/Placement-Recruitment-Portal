from django.contrib import admin
from jobs.models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'posted_on', 'is_active')
    list_filter = ('is_active', 'job_type', 'posted_on')
    search_fields = ('title', 'company__company_name')
