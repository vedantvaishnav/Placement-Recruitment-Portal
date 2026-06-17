"""
APPLICATIONS VIEWS
- Application creation
- Application list (student & company)
- Application tracking
- Skill matching
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from applications.models import Application
from applications.forms import ApplicationForm, ApplicationStatusForm
from jobs.models import Job
from accounts.models import Student


class ApplicationCreateView(LoginRequiredMixin, CreateView):
    """
    Create job application (Student only)
    - Student applies for a job
    - Calculates skill match
    - Prevents duplicate applications
    """
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/application_form.html'
    login_url = 'student_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = get_object_or_404(Job, pk=self.kwargs['job_id'])
        return context

    def form_valid(self, form):
        job = get_object_or_404(Job, pk=self.kwargs['job_id'])
        student = self.request.user.student

        # Check if already applied
        if Application.objects.filter(student=student, job=job).exists():
            messages.error(self.request, "You have already applied for this job!")
            return redirect('job_detail', pk=job.id)

        # Check eligibility
        if student.cgpa < job.min_cgpa:
            messages.error(self.request, f"Your CGPA is below the minimum required ({job.min_cgpa})")
            return redirect('job_detail', pk=job.id)

        if student.branch not in job.get_allowed_branches_list():
            messages.error(self.request, f"Your branch is not eligible for this job")
            return redirect('job_detail', pk=job.id)

        # Create application
        application = form.save(commit=False)
        application.student = student
        application.job = job
        application.save()

        # Calculate skill match
        application.calculate_skill_match()

        # Update job application count
        job.applications_received += 1
        job.save()

        # Update student application count
        student.applied_jobs += 1
        student.save()

        messages.success(self.request, "Application submitted successfully!")
        return redirect('student_dashboard')


class StudentApplicationListView(LoginRequiredMixin, ListView):
    """
    List all applications by a student
    - Shows application status
    - Shows skill match percentage
    """
    model = Application
    template_name = 'applications/student_applications.html'
    context_object_name = 'applications'
    login_url = 'student_login'
    paginate_by = 10

    def get_queryset(self):
        student = self.request.user.student
        return Application.objects.filter(student=student).select_related('job')


class CompanyApplicationListView(LoginRequiredMixin, ListView):
    """
    List all applications received by a company
    - Shows applications for all jobs posted by company
    - Filters by job and status
    """
    model = Application
    template_name = 'applications/company_applications.html'
    context_object_name = 'applications'
    login_url = 'company_login'
    paginate_by = 10

    def get_queryset(self):
        company = self.request.user.company
        queryset = Application.objects.filter(job__company=company).select_related('student', 'job')
        
        # Filter by job if provided
        job_id = self.request.GET.get('job_id')
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-applied_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        context['jobs'] = Job.objects.filter(company=company)
        context['status_choices'] = Application.STATUS_CHOICES
        return context


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    """
    Detail view of an application
    - Shows applicant details, resume, cover letter
    - Shows skill match
    """
    model = Application
    template_name = 'applications/application_detail.html'
    context_object_name = 'application'
    login_url = 'student_login'

    def get_object(self, queryset=None):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        
        # Check access permissions
        user = self.request.user
        if (user.is_staff or 
            (hasattr(user, 'student') and application.student == user.student) or
            (hasattr(user, 'company') and application.job.company == user.company)):
            return application
        
        messages.error(self.request, "You don't have permission to view this application")
        raise PermissionError


class ApplicationStatusUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update application status (Company/Admin only)
    - Update status: Shortlisted, Rejected, Selected, etc.
    - Add notes
    """
    model = Application
    form_class = ApplicationStatusForm
    template_name = 'applications/application_status_form.html'
    login_url = 'company_login'

    def get_object(self, queryset=None):
        application = get_object_or_404(Application, pk=self.kwargs['pk'])
        
        # Check if user is the company or admin
        user = self.request.user
        if user.is_staff or application.job.company == user.company:
            return application
        
        messages.error(self.request, "You don't have permission to update this application")
        raise PermissionError

    def form_valid(self, form):
        messages.success(self.request, "Application status updated!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('company_applications')


class ApplicationTrackingView(LoginRequiredMixin, TemplateView):
    """
    Application tracking dashboard for students
    - Shows all applications with timeline
    - Shows status progression
    """
    template_name = 'applications/application_tracking.html'
    login_url = 'student_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        
        # Get all applications with their details
        applications = Application.objects.filter(student=student).select_related('job')
        
        # Organize by status
        context['applied'] = applications.filter(status='APPLIED')
        context['shortlisted'] = applications.filter(status='SHORTLISTED')
        context['rejected'] = applications.filter(status='REJECTED')
        context['interview'] = applications.filter(status='INTERVIEW')
        context['selected'] = applications.filter(status='SELECTED')
        context['offer_received'] = applications.filter(status='OFFER_RECEIVED')
        context['offer_accepted'] = applications.filter(status='OFFER_ACCEPTED')
        
        context['total'] = applications.count()
        context['applications'] = applications
        
        return context
