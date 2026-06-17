from django.contrib import admin
from applications.models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_on')
    list_filter = ('status', 'applied_on')
    search_fields = ('student__user__first_name', 'job__title')
