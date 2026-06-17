"""
ACCOUNTS URLs
- Student registration, login, dashboard, profile
- Company registration, login, dashboard, profile
"""
from django.urls import path
from accounts.views import (
    StudentRegistrationView, StudentLoginView, StudentDashboardView,
    StudentProfileView, StudentLogoutView,
    CompanyRegistrationView, CompanyLoginView, CompanyDashboardView,
    CompanyProfileView, CompanyLogoutView
)

urlpatterns = [
    # Student URLs
    path('student/register/', StudentRegistrationView.as_view(), name='student_register'),
    path('student/login/', StudentLoginView.as_view(), name='student_login'),
    path('student/logout/', StudentLogoutView.as_view(), name='student_logout'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/profile/', StudentProfileView.as_view(), name='student_profile'),
    
    # Company URLs
    path('company/register/', CompanyRegistrationView.as_view(), name='company_register'),
    path('company/login/', CompanyLoginView.as_view(), name='company_login'),
    path('company/logout/', CompanyLogoutView.as_view(), name='company_logout'),
    path('company/dashboard/', CompanyDashboardView.as_view(), name='company_dashboard'),
    path('company/profile/', CompanyProfileView.as_view(), name='company_profile'),
]
