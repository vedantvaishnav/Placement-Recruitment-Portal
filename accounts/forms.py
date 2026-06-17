"""
ACCOUNTS FORMS
- StudentRegistrationForm
- StudentLoginForm
- CompanyRegistrationForm
- CompanyLoginForm
- StudentProfileForm
- CompanyProfileForm
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Student, Company


class StudentRegistrationForm(UserCreationForm):
    """Form for student registration"""
    first_name = forms.CharField(max_length=100, required=True, label='First Name')
    last_name = forms.CharField(max_length=100, required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email Address')
    roll_no = forms.CharField(max_length=20, required=True, label='Roll Number')
    phone = forms.CharField(max_length=20, required=True, label='Phone Number')
    branch = forms.ChoiceField(
        choices=[
            ('CSE', 'Computer Science'),
            ('ECE', 'Electronics'),
            ('ME', 'Mechanical'),
            ('CE', 'Civil'),
            ('EE', 'Electrical'),
        ],
        required=True
    )
    year = forms.IntegerField(
        widget=forms.Select(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')]),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_roll_no(self):
        roll_no = self.cleaned_data.get('roll_no')
        if Student.objects.filter(roll_no=roll_no).exists():
            raise forms.ValidationError("This roll number is already registered.")
        return roll_no

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Password must be at least 8 characters with letters and numbers"
        self.fields['password2'].help_text = "Re-enter your password"


class CompanyRegistrationForm(UserCreationForm):
    """Form for company registration"""
    email = forms.EmailField(required=True, label='Email Address')
    company_name = forms.CharField(max_length=200, required=True, label='Company Name')
    industry = forms.CharField(max_length=100, required=True, label='Industry')
    phone = forms.CharField(max_length=20, required=True, label='Contact Phone')
    website = forms.URLField(required=False, label='Company Website')
    address = forms.CharField(widget=forms.Textarea, required=True, label='Address')
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if Company.objects.filter(company_name=company_name).exists():
            raise forms.ValidationError("This company is already registered.")
        return company_name


class StudentLoginForm(forms.Form):
    """Form for student login"""
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class CompanyLoginForm(forms.Form):
    """Form for company login"""
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class StudentProfileForm(forms.ModelForm):
    """Form for student profile update"""
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = Student
        fields = ('phone', 'cgpa', 'skills', 'resume', 'branch', 'year')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['skills'].help_text = "Enter skills separated by commas"
        self.fields['phone'].widget.attrs['placeholder'] = '+91-XXXXXXXXXX'


class CompanyProfileForm(forms.ModelForm):
    """Form for company profile update"""
    email = forms.EmailField(required=True)

    class Meta:
        model = Company
        fields = ('company_name', 'phone', 'website', 'address', 'city', 'state', 'industry', 'description', 'logo')
