"""
JOBS VIEWS
- Job listing
- Job detail
- Job creation (by company)
- Skill matching
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from jobs.models import Job
from jobs.forms import JobCreationForm, JobFilterForm
from accounts.models import Company
from applications.models import Application


class JobListView(ListView):
    """
    List all active jobs with filtering and search
    - Accessible to all users
    - Filters by job type, location, salary
    - Shows skill match for logged-in students
    """
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).select_related('company')
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(company__company_name__icontains=search)
            )

        # Job type filter
        job_type = self.request.GET.getlist('job_type')
        if job_type:
            queryset = queryset.filter(job_type__in=job_type)

        # Location filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        # Salary filter
        min_salary = self.request.GET.get('min_salary')
        max_salary = self.request.GET.get('max_salary')
        if min_salary:
            queryset = queryset.filter(salary_min__gte=min_salary)
        if max_salary:
            queryset = queryset.filter(salary_max__lte=max_salary)

        # Sorting
        sort_by = self.request.GET.get('sort_by', 'newest')
        if sort_by == 'newest':
            queryset = queryset.order_by('-posted_on')
        elif sort_by == 'salary_high':
            queryset = queryset.order_by('-salary_max')
        elif sort_by == 'salary_low':
            queryset = queryset.order_by('salary_min')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = JobFilterForm(self.request.GET)
        
        # Add applied status for logged-in students
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student'):
            student = self.request.user.student
            applied_job_ids = Application.objects.filter(
                student=student
            ).values_list('job_id', flat=True)
            context['applied_jobs'] = applied_job_ids
        
        return context


class JobDetailView(DetailView):
    """
    Detailed view of a job posting
    - Shows all job details
    - Shows company information
    - Application button for students
    """
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        
        # Check if student has already applied
        if self.request.user.is_authenticated and hasattr(self.request.user, 'student'):
            student = self.request.user.student
            context['already_applied'] = Application.objects.filter(
                student=student,
                job=job
            ).exists()
            context['can_apply'] = True
            
            # Check eligibility
            if student.cgpa < job.min_cgpa:
                context['can_apply'] = False
                context['reason'] = f"Your CGPA ({student.cgpa}) is below minimum required ({job.min_cgpa})"
            
            if student.branch not in job.get_allowed_branches_list():
                context['can_apply'] = False
                context['reason'] = f"Your branch ({student.branch}) is not allowed for this job"
        
        return context


class CompanyJobListView(LoginRequiredMixin, ListView):
    """
    List of jobs posted by the company
    - Only company can access
    - Shows all job postings and their status
    """
    model = Job
    template_name = 'jobs/company_jobs.html'
    context_object_name = 'jobs'
    login_url = 'company_login'

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company)


class JobCreateView(LoginRequiredMixin, CreateView):
    """
    Create new job posting (Company only)
    - Company can post new jobs
    - Fills in company automatically
    """
    model = Job
    form_class = JobCreationForm
    template_name = 'jobs/job_form.html'
    login_url = 'company_login'
    success_url = reverse_lazy('company_jobs')

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update job posting (Company only)
    - Company can edit their own jobs
    """
    model = Job
    form_class = JobCreationForm
    template_name = 'jobs/job_form.html'
    login_url = 'company_login'
    success_url = reverse_lazy('company_jobs')

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company)

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form)


class JobDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete job posting (Company only)
    - Company can delete their own jobs
    """
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    login_url = 'company_login'
    success_url = reverse_lazy('company_jobs')

    def get_queryset(self):
        return Job.objects.filter(company=self.request.user.company)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Job deleted successfully!")
        return super().delete(request, *args, **kwargs)
