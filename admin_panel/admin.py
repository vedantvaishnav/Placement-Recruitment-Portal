from django.contrib import admin
from admin_panel.models import AdminStats

@admin.register(AdminStats)
class AdminStatsAdmin(admin.ModelAdmin):
    list_display = ('total_students', 'total_companies', 'total_jobs', 'students_placed')
