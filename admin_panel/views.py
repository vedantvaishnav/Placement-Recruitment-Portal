"""
ADMIN PANEL VIEWS
- Dashboard with statistics
- User management
- Company verification
"""
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count
from accounts.models import Student, Company
from jobs.models import Job
from applications.models import Application
from admin_panel.models import AdminStats


class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Admin Dashboard
    - Shows portal statistics
    - Total students, companies, jobs, applications
    - Placement statistics
    """
    template_name = 'admin_panel/dashboard.html'
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        context['total_students'] = Student.objects.count()
        context['total_companies'] = Company.objects.count()
        context['unverified_companies'] = Company.objects.filter(verified=False).count()
        context['total_jobs'] = Job.objects.count()
        context['active_jobs'] = Job.objects.filter(is_active=True).count()
        context['total_applications'] = Application.objects.count()
        context['placed_students'] = Student.objects.filter(placed=True).count()
        context['pending_verifications'] = Company.objects.filter(verified=False).count()
        
        # Application status breakdown
        context['applications_applied'] = Application.objects.filter(status='APPLIED').count()
        context['applications_shortlisted'] = Application.objects.filter(status='SHORTLISTED').count()
        context['applications_selected'] = Application.objects.filter(status='SELECTED').count()
        context['applications_rejected'] = Application.objects.filter(status='REJECTED').count()
        
        # Calculate average salary from selected applications
        selected_apps = Application.objects.filter(status='SELECTED').select_related('job')
        salaries = [app.job.salary_max for app in selected_apps if app.job.salary_max]
        context['average_salary'] = sum(salaries) / len(salaries) if salaries else 0
        
        # Top companies by placements
        context['top_companies'] = Job.objects.values('company__company_name').annotate(
            count=Count('applications__status')
        ).filter(applications__status='SELECTED').order_by('-count')[:5]
        
        return context


class AdminStudentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all students (Admin only)
    - Shows student details
    - Placement status
    """
    model = Student
    template_name = 'admin_panel/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        queryset = Student.objects.all()
        
        # Search by name or roll number
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(roll_no__icontains=search)
            )
        
        # Filter by branch
        branch = self.request.GET.get('branch')
        if branch:
            queryset = queryset.filter(branch=branch)
        
        # Filter by placement status
        placed = self.request.GET.get('placed')
        if placed == 'true':
            queryset = queryset.filter(placed=True)
        elif placed == 'false':
            queryset = queryset.filter(placed=False)
        
        return queryset


class AdminCompanyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all companies (Admin only)
    - Shows company details
    - Verification status
    """
    model = Company
    template_name = 'admin_panel/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        queryset = Company.objects.all()
        
        # Filter by verification status
        verified = self.request.GET.get('verified')
        if verified == 'true':
            queryset = queryset.filter(verified=True)
        elif verified == 'false':
            queryset = queryset.filter(verified=False)
        
        # Search by company name
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(company_name__icontains=search)
        
        return queryset.order_by('-created_at')


class AdminCompanyVerifyView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Verify company (Admin only)
    - Admin can verify/unverify companies
    """
    model = Company
    fields = ['verified']
    template_name = 'admin_panel/verify_company.html'
    login_url = 'admin_login'
    success_url = reverse_lazy('admin_companies')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def form_valid(self, form):
        company = form.save()
        if company.verified:
            messages.success(self.request, f"{company.company_name} has been verified!")
        else:
            messages.info(self.request, f"{company.company_name} verification has been removed.")
        return super().form_valid(form)


class AdminApplicationListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List all applications (Admin only)
    - Shows all applications with status
    - Can track student placements
    """
    model = Application
    template_name = 'admin_panel/application_list.html'
    context_object_name = 'applications'
    paginate_by = 20
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_queryset(self):
        queryset = Application.objects.select_related('student', 'job').all()
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(student__user__first_name__icontains=search) |
                Q(student__roll_no__icontains=search) |
                Q(job__title__icontains=search)
            )
        
        return queryset.order_by('-applied_on')


from django.db.models import Q


class AdminReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Admin Reports
    - Placement statistics
    - Salary statistics
    - Branch-wise breakdown
    """
    template_name = 'admin_panel/reports.html'
    login_url = 'admin_login'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Branch-wise placement
        context['branch_placement'] = Student.objects.values('branch').annotate(
            total=Count('id'),
            placed=Count('id', filter=Q(placed=True))
        )
        
        # Year-wise distribution
        context['year_distribution'] = Student.objects.values('year').annotate(
            count=Count('id')
        )
        
        # Salary range statistics
        selected_jobs = Job.objects.filter(
            applications__status='SELECTED'
        ).values('salary_max').annotate(count=Count('applications__id'))
        context['salary_statistics'] = selected_jobs
        
        # Top recruiting companies
        context['top_companies'] = Company.objects.annotate(
            placed_count=Count('jobs__applications__id', 
                              filter=Q(jobs__applications__status='SELECTED'))
        ).order_by('-placed_count')[:10]
        
        return context
