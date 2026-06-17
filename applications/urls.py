"""
APPLICATIONS URLs
- Application creation, listing, tracking
- Status updates
"""
from django.urls import path
from applications.views import (
    ApplicationCreateView, StudentApplicationListView, CompanyApplicationListView,
    ApplicationDetailView, ApplicationStatusUpdateView, ApplicationTrackingView
)

urlpatterns = [
    # Student URLs
    path('my-applications/', StudentApplicationListView.as_view(), name='student_applications'),
    path('tracking/', ApplicationTrackingView.as_view(), name='application_tracking'),
    path('job/<int:job_id>/apply/', ApplicationCreateView.as_view(), name='apply_job'),
    
    # Application Detail
    path('<int:pk>/', ApplicationDetailView.as_view(), name='application_detail'),
    
    # Company URLs
    path('company/applications/', CompanyApplicationListView.as_view(), name='company_applications'),
    path('<int:pk>/status/', ApplicationStatusUpdateView.as_view(), name='update_application_status'),
]
