"""
APPLICATIONS FORMS
- ApplicationForm
- ApplicationStatusForm
"""
from django import forms
from applications.models import Application


class ApplicationForm(forms.ModelForm):
    """Form for job application"""
    
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume_used']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your cover letter here...'
            }),
            'resume_used': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    """Form for updating application status (Admin/Company)"""
    
    class Meta:
        model = Application
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add notes about this application...'
            }),
        }
