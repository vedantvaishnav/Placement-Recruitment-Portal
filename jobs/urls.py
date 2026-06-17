"""
JOBS URLs
- Job listing, detail
- Job creation, update, delete (by company)
"""
from django.urls import path
from jobs.views import (
    JobListView, JobDetailView, CompanyJobListView,
    JobCreateView, JobUpdateView, JobDeleteView
)

urlpatterns = [
    # Public URLs
    path('', JobListView.as_view(), name='job_list'),
    path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    
    # Company URLs
    path('my-jobs/', CompanyJobListView.as_view(), name='company_jobs'),
    path('create/', JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/edit/', JobUpdateView.as_view(), name='job_edit'),
    path('<int:pk>/delete/', JobDeleteView.as_view(), name='job_delete'),
]
