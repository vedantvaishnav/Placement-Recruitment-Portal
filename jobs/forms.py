"""
JOBS FORMS
- JobCreationForm
- JobFilterForm
"""
from django import forms
from jobs.models import Job


class JobCreationForm(forms.ModelForm):
    """Form for creating/updating job postings"""
    
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'required_skills', 'job_type',
            'experience_required', 'location', 'salary_min', 'salary_max',
            'qualification_required', 'min_cgpa', 'allowed_branches',
            'application_deadline', 'max_applications'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Job Description'}),
            'required_skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, Django, JavaScript'}),
            'job_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_required': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Location'}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Salary (LPA)'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Salary (LPA)'}),
            'qualification_required': forms.Select(attrs={'class': 'form-control'}),
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum CGPA'}),
            'allowed_branches': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CSE, ECE, ME'}),
            'application_deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'max_applications': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class JobFilterForm(forms.Form):
    """Form for filtering jobs"""
    SORT_CHOICES = [
        ('newest', 'Newest First'),
        ('salary_high', 'Highest Salary'),
        ('salary_low', 'Lowest Salary'),
    ]

    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search jobs...'})
    )
    job_type = forms.MultipleChoiceField(
        choices=Job.JOB_TYPE_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    location = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    min_salary = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_salary = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
