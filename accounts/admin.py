from django.contrib import admin
from accounts.models import Student, Company

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'user', 'branch', 'cgpa', 'placed')
    list_filter = ('branch', 'placed', 'year')
    search_fields = ('roll_no', 'user__first_name', 'user__last_name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'industry', 'verified', 'created_at')
    list_filter = ('verified', 'created_at')
    search_fields = ('company_name', 'industry')
