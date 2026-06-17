"""
ADMIN PANEL URLs
- Dashboard, student list, company list, applications
- Reports and statistics
"""
from django.urls import path
from admin_panel.views import (
    AdminDashboardView, AdminStudentListView, AdminCompanyListView,
    AdminCompanyVerifyView, AdminApplicationListView, AdminReportsView
)

urlpatterns = [
    path('dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('students/', AdminStudentListView.as_view(), name='admin_students'),
    path('companies/', AdminCompanyListView.as_view(), name='admin_companies'),
    path('company/<int:pk>/verify/', AdminCompanyVerifyView.as_view(), name='verify_company'),
    path('applications/', AdminApplicationListView.as_view(), name='admin_applications'),
    path('reports/', AdminReportsView.as_view(), name='admin_reports'),
]
