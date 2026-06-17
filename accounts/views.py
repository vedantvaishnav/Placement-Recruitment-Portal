"""
ACCOUNTS VIEWS
- Student Registration/Login/Dashboard
- Company Registration/Login/Dashboard
- Profile management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from accounts.models import Student, Company
from accounts.forms import (
    StudentRegistrationForm, StudentLoginForm, CompanyRegistrationForm,
    CompanyLoginForm, StudentProfileForm, CompanyProfileForm
)
from jobs.models import Job
from applications.models import Application


class StudentRegistrationView(View):
    """
    View for student registration
    - Accepts POST request with student data
    - Creates User and Student profile
    """
    def get(self, request):
        form = StudentRegistrationForm()
        return render(request, 'accounts/student_register.html', {'form': form})

    def post(self, request):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = form.save(commit=False)
                    user.first_name = form.cleaned_data.get('first_name')
                    user.last_name = form.cleaned_data.get('last_name')
                    user.save()

                    # Create Student profile
                    student = Student.objects.create(
                        user=user,
                        roll_no=form.cleaned_data.get('roll_no'),
                        phone=form.cleaned_data.get('phone'),
                        branch=form.cleaned_data.get('branch'),
                        year=form.cleaned_data.get('year'),
                        skills='',
                    )
                    messages.success(request, "Registration successful! Please login.")
                    return redirect('student_login')
            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")
        return render(request, 'accounts/student_register.html', {'form': form})


class StudentLoginView(View):
    """
    View for student login
    - Authenticates student credentials
    - Creates session
    """
    def get(self, request):
        form = StudentLoginForm()
        return render(request, 'accounts/student_login.html', {'form': form})

    def post(self, request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user has student profile
                if hasattr(user, 'student'):
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    return redirect('student_dashboard')
                else:
                    messages.error(request, "You are not registered as a student.")
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'accounts/student_login.html', {'form': form})


class CompanyRegistrationView(View):
    """
    View for company registration
    - Accepts POST request with company data
    - Creates User and Company profile
    """
    def get(self, request):
        form = CompanyRegistrationForm()
        return render(request, 'accounts/company_register.html', {'form': form})

    def post(self, request):
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create User
                    user = form.save(commit=False)
                    user.first_name = form.cleaned_data.get('company_name')
                    user.save()

                    # Create Company profile
                    company = Company.objects.create(
                        user=user,
                        company_name=form.cleaned_data.get('company_name'),
                        industry=form.cleaned_data.get('industry'),
                        phone=form.cleaned_data.get('phone'),
                        website=form.cleaned_data.get('website', ''),
                        address=form.cleaned_data.get('address'),
                        city=form.cleaned_data.get('city'),
                        state=form.cleaned_data.get('state'),
                    )
                    messages.success(request, "Registration successful! Please wait for admin verification.")
                    return redirect('company_login')
            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")
        return render(request, 'accounts/company_register.html', {'form': form})


class CompanyLoginView(View):
    """
    View for company login
    - Authenticates company credentials
    - Creates session
    """
    def get(self, request):
        form = CompanyLoginForm()
        return render(request, 'accounts/company_login.html', {'form': form})

    def post(self, request):
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user has company profile
                if hasattr(user, 'company'):
                    login(request, user)
                    messages.success(request, f"Welcome, {user.company.company_name}!")
                    return redirect('company_dashboard')
                else:
                    messages.error(request, "You are not registered as a company.")
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'accounts/company_login.html', {'form': form})


class StudentDashboardView(LoginRequiredMixin, TemplateView):
    """
    Student Dashboard
    - Shows profile info
    - Displays applied jobs and their status
    - Shows applications summary
    """
    template_name = 'accounts/student_dashboard.html'
    login_url = 'student_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user.student
        context['student'] = student
        context['applications'] = Application.objects.filter(student=student).select_related('job')
        context['total_applications'] = context['applications'].count()
        context['shortlisted'] = context['applications'].filter(status='SHORTLISTED').count()
        context['selected'] = context['applications'].filter(status='SELECTED').count()
        context['rejected'] = context['applications'].filter(status='REJECTED').count()
        return context


class CompanyDashboardView(LoginRequiredMixin, TemplateView):
    """
    Company Dashboard
    - Shows company profile
    - Displays posted jobs
    - Shows applications received
    """
    template_name = 'accounts/company_dashboard.html'
    login_url = 'company_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.user.company
        context['company'] = company
        context['jobs'] = Job.objects.filter(company=company)
        context['total_jobs'] = context['jobs'].count()
        context['total_applications'] = Application.objects.filter(job__company=company).count()
        context['shortlisted'] = Application.objects.filter(
            job__company=company,
            status='SHORTLISTED'
        ).count()
        return context


class StudentProfileView(LoginRequiredMixin, UpdateView):
    """
    Student Profile Update View
    - Allows student to update profile information
    """
    model = Student
    form_class = StudentProfileForm
    template_name = 'accounts/student_profile.html'
    login_url = 'student_login'
    success_url = reverse_lazy('student_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.student

    def form_valid(self, form):
        student = form.save()
        # Update user information
        user = self.request.user
        user.first_name = self.request.POST.get('first_name', user.first_name)
        user.last_name = self.request.POST.get('last_name', user.last_name)
        user.email = self.request.POST.get('email', user.email)
        user.save()
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class CompanyProfileView(LoginRequiredMixin, UpdateView):
    """
    Company Profile Update View
    - Allows company to update profile information
    """
    model = Company
    form_class = CompanyProfileForm
    template_name = 'accounts/company_profile.html'
    login_url = 'company_login'
    success_url = reverse_lazy('company_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.company

    def form_valid(self, form):
        company = form.save()
        # Update user information
        user = self.request.user
        user.email = self.request.POST.get('email', user.email)
        user.save()
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)


class StudentLogoutView(View):
    """Logout view for students"""
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('student_login')


class CompanyLogoutView(View):
    """Logout view for companies"""
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('company_login')
