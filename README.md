# Django Placement Portal - Complete Documentation

## 📋 Project Overview

A comprehensive Django-based Placement Portal system that connects students with job opportunities. The portal includes student & company registration, job posting, application management, skill matching, resume upload, and admin dashboard with analytics.

---

## 🎯 Features Implemented

### ✅ Student Features
- User registration and login
- Profile creation and management (skills, CGPA, resume upload)
- Browse and search jobs with filters (location, salary, job type)
- Apply for jobs with cover letters
- Track application status
- View skill match percentage
- Application tracking dashboard
- Download resumes

### ✅ Company Features
- Company registration and login
- Company profile management
- Post unlimited job openings
- Manage job postings (create, edit, delete)
- View and manage applications
- Update application status (shortlist, select, reject)
- Track hiring metrics

### ✅ Admin Features
- Comprehensive dashboard with statistics
- Student management
- Company management and verification
- Application tracking and management
- Placement reports and analytics
- Branch-wise placement statistics

### ✅ Skill Matching
- Automatic skill match calculation (0-100%)
- Matches student skills with job requirements
- Helps students find best-fit opportunities

---

## 📁 Project Structure

```
placement_portal/
├── placement_portal/          # Main project settings
│   ├── settings.py           # Django settings (INSTALLED_APPS, DATABASES, etc.)
│   ├── urls.py               # Main URL configuration
│   ├── asgi.py               # ASGI configuration
│   └── wsgi.py               # WSGI configuration
│
├── accounts/                  # Student & Company authentication
│   ├── models.py             # Student and Company models
│   ├── views.py              # Registration, login, dashboard views
│   ├── forms.py              # Registration and profile forms
│   ├── urls.py               # Account URLs
│   ├── admin.py              # Django admin configuration
│   └── apps.py               # App configuration
│
├── jobs/                      # Job posting management
│   ├── models.py             # Job model
│   ├── views.py              # Job listing, detail, creation views
│   ├── forms.py              # Job creation and filter forms
│   ├── urls.py               # Job URLs
│   ├── admin.py              # Admin configuration
│   └── apps.py               # App configuration
│
├── applications/             # Job application system
│   ├── models.py             # Application model with skill matching
│   ├── views.py              # Application views and tracking
│   ├── forms.py              # Application forms
│   ├── urls.py               # Application URLs
│   ├── admin.py              # Admin configuration
│   └── apps.py               # App configuration
│
├── admin_panel/              # Admin dashboard
│   ├── models.py             # AdminStats model
│   ├── views.py              # Admin dashboard and reports
│   ├── urls.py               # Admin URLs
│   ├── admin.py              # Admin configuration
│   └── apps.py               # App configuration
│
├── templates/                # HTML templates
│   ├── base.html             # Base template with navbar and footer
│   ├── home.html             # Home page
│   ├── accounts/             # Account templates
│   │   ├── student_register.html
│   │   ├── student_login.html
│   │   ├── student_dashboard.html
│   │   ├── student_profile.html
│   │   ├── company_register.html
│   │   ├── company_login.html
│   │   ├── company_dashboard.html
│   │   └── company_profile.html
│   ├── jobs/                 # Job templates
│   │   ├── job_list.html
│   │   ├── job_detail.html
│   │   ├── job_form.html
│   │   ├── company_jobs.html
│   │   └── job_confirm_delete.html
│   ├── applications/         # Application templates
│   │   ├── application_form.html
│   │   ├── student_applications.html
│   │   ├── application_tracking.html
│   │   ├── application_detail.html
│   │   ├── company_applications.html
│   │   └── application_status_form.html
│   └── admin_panel/          # Admin templates
│       ├── dashboard.html
│       ├── student_list.html
│       ├── company_list.html
│       ├── verify_company.html
│       ├── application_list.html
│       └── reports.html
│
├── static/                   # Static files
│   └── css/
│       └── style.css         # Main stylesheet
│
├── media/                    # User uploads
│   └── resumes/              # Student resumes
│
├── manage.py                 # Django management script
└── db.sqlite3                # SQLite database
```

---

## 🗂️ Models Explained

### 1. **Student Model** (`accounts/models.py`)
```python
class Student:
    - user: OneToOneField(User)
    - roll_no: CharField (unique)
    - phone: CharField
    - cgpa: FloatField
    - skills: TextField (comma-separated)
    - resume: FileField (PDF/DOC/DOCX)
    - branch: CharField (CSE, ECE, ME, CE, EE)
    - year: IntegerField (1-4)
    - applied_jobs: IntegerField
    - placed: BooleanField
    - placement_offer: CharField
```

### 2. **Company Model** (`accounts/models.py`)
```python
class Company:
    - user: OneToOneField(User)
    - company_name: CharField
    - industry: CharField
    - website: URLField
    - phone: CharField
    - address: TextField
    - city: CharField
    - state: CharField
    - description: TextField
    - logo: ImageField
    - jobs_posted: IntegerField
    - verified: BooleanField
```

### 3. **Job Model** (`jobs/models.py`)
```python
class Job:
    - company: ForeignKey(Company)
    - title: CharField
    - description: TextField
    - required_skills: TextField
    - job_type: CharField (FULL_TIME, PART_TIME, INTERNSHIP, CONTRACT)
    - experience_required: CharField (FRESHER, 0-1, 1-2, 2-5, 5+)
    - location: CharField
    - salary_min/max: IntegerField (LPA)
    - qualification_required: CharField
    - min_cgpa: FloatField
    - allowed_branches: CharField
    - application_deadline: DateTimeField
    - max_applications: IntegerField
    - applications_received: IntegerField
    - is_active: BooleanField
```

### 4. **Application Model** (`applications/models.py`)
```python
class Application:
    - student: ForeignKey(Student)
    - job: ForeignKey(Job)
    - status: CharField (APPLIED, SHORTLISTED, SELECTED, etc.)
    - cover_letter: TextField
    - resume_used: FileField
    - skill_match_percentage: IntegerField (0-100)
    - notes: TextField
    - applied_on: DateTimeField
    - last_updated: DateTimeField
    
    Methods:
    - calculate_skill_match(): Calculates match percentage
```

### 5. **AdminStats Model** (`admin_panel/models.py`)
```python
class AdminStats:
    - total_students: IntegerField
    - total_companies: IntegerField
    - total_jobs: IntegerField
    - total_applications: IntegerField
    - students_placed: IntegerField
    - average_salary: FloatField
```

---

## 🔧 URL Routes

### Accounts URLs (`/auth/`)
| URL | View | Purpose |
|-----|------|---------|
| `/student/register/` | StudentRegistrationView | Student registration |
| `/student/login/` | StudentLoginView | Student login |
| `/student/logout/` | StudentLogoutView | Student logout |
| `/student/dashboard/` | StudentDashboardView | Student dashboard |
| `/student/profile/` | StudentProfileView | Update profile |
| `/company/register/` | CompanyRegistrationView | Company registration |
| `/company/login/` | CompanyLoginView | Company login |
| `/company/logout/` | CompanyLogoutView | Company logout |
| `/company/dashboard/` | CompanyDashboardView | Company dashboard |
| `/company/profile/` | CompanyProfileView | Update profile |

### Jobs URLs (`/jobs/`)
| URL | View | Purpose |
|-----|------|---------|
| `/` | JobListView | Browse all jobs |
| `/<id>/` | JobDetailView | Job details |
| `/my-jobs/` | CompanyJobListView | Company's jobs |
| `/create/` | JobCreateView | Create new job |
| `/<id>/edit/` | JobUpdateView | Edit job |
| `/<id>/delete/` | JobDeleteView | Delete job |

### Applications URLs (`/applications/`)
| URL | View | Purpose |
|-----|------|---------|
| `/my-applications/` | StudentApplicationListView | View applications |
| `/tracking/` | ApplicationTrackingView | Application tracking |
| `/job/<job_id>/apply/` | ApplicationCreateView | Apply for job |
| `/<id>/` | ApplicationDetailView | View application |
| `/company/applications/` | CompanyApplicationListView | Company applications |
| `/<id>/status/` | ApplicationStatusUpdateView | Update status |

### Admin URLs (`/admin-panel/`)
| URL | View | Purpose |
|-----|------|---------|
| `/dashboard/` | AdminDashboardView | Dashboard |
| `/students/` | AdminStudentListView | Student list |
| `/companies/` | AdminCompanyListView | Company list |
| `/company/<id>/verify/` | AdminCompanyVerifyView | Verify company |
| `/applications/` | AdminApplicationListView | All applications |
| `/reports/` | AdminReportsView | Reports |

---

## 🎨 CSS Styling

**Main Stylesheet**: `static/css/style.css`

Features:
- Responsive design (desktop, tablet, mobile)
- Color scheme with CSS variables
- Card-based layout
- Form styling
- Status badges
- Alert messages
- Table styling
- Navigation bar
- Footer
- Utility classes

### Color Scheme
- Primary: `#2c3e50` (Dark Blue)
- Secondary: `#3498db` (Light Blue)
- Success: `#27ae60` (Green)
- Danger: `#e74c3c` (Red)
- Warning: `#f39c12` (Orange)
- Light: `#ecf0f1` (Light Gray)

---

## 🔐 Authentication & Authorization

### Login Types
1. **Student Login** → Access student dashboard, apply jobs
2. **Company Login** → Access company dashboard, post jobs
3. **Admin Login** → Access admin panel (staff users only)

### Access Control
- Student views: Protected with `LoginRequiredMixin`
- Company views: Check `hasattr(user, 'company')`
- Admin views: `UserPassesTestMixin` checks `is_staff` or `is_superuser`

### Login URLs
- `LOGIN_URL = 'student_login'` (default)
- Each view specifies its own `login_url`

---

## 📊 Key Features Explained

### 1. **Skill Matching Algorithm**
```python
# In applications/models.py - Application.calculate_skill_match()
student_skills = set(self.student.get_skills_list())
job_skills = set(self.job.get_required_skills_list())
matching_skills = student_skills.intersection(job_skills)
match_percentage = (len(matching_skills) / len(job_skills)) * 100
```

### 2. **Job Filtering**
- Search by title, company, description
- Filter by job type, location, salary range
- Sort by newest, salary high/low

### 3. **Application Status Flow**
```
APPLIED → SHORTLISTED → INTERVIEW → SELECTED → OFFER_RECEIVED → OFFER_ACCEPTED
                    ↓
                REJECTED
```

### 4. **Dashboard Statistics**
- Real-time application counts
- Placement metrics
- Salary statistics
- Company rankings

---

## 🚀 Getting Started

### 1. **Installation**
```bash
# Navigate to project directory
cd placement_portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django pillow

# Apply migrations
python manage.py makemigrations
python manage.py migrate
```

### 2. **Create Admin User**
```bash
python manage.py createsuperuser
```

### 3. **Run Development Server**
```bash
python manage.py runserver
```

Access at: `http://localhost:8000/`

### 4. **Create Test Data**
- Register students at `/auth/student/register/`
- Register companies at `/auth/company/register/`
- Post jobs at `/jobs/create/` (as company)

---

## 📝 Forms Included

### Student Forms
- `StudentRegistrationForm` - Complete registration
- `StudentLoginForm` - Simple login
- `StudentProfileForm` - Update profile

### Company Forms
- `CompanyRegistrationForm` - Company signup
- `CompanyLoginForm` - Company login
- `CompanyProfileForm` - Update company info

### Job Forms
- `JobCreationForm` - Post/edit jobs
- `JobFilterForm` - Filter jobs

### Application Forms
- `ApplicationForm` - Submit application
- `ApplicationStatusForm` - Update status

---

## 📱 Templates Overview

All templates extend `base.html` which provides:
- Navigation bar with user menu
- Message display
- Footer
- Responsive layout

### Template Structure
```html
{% extends 'base.html' %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <!-- Page specific content -->
{% endblock %}

{% block extra_css %}
    <!-- Optional extra CSS -->
{% endblock %}

{% block extra_js %}
    <!-- Optional extra JavaScript -->
{% endblock %}
```

---

## 🔍 Admin Panel Features

### Dashboard
- Total counts (students, companies, jobs, applications)
- Placement statistics
- Application status breakdown
- Average salary calculation
- Top recruiting companies

### Student Management
- Filter by branch, placement status
- Search by name or roll number
- View all student details

### Company Management
- Company verification system
- Verify/unverify companies
- Company information display

### Reports
- Branch-wise placement statistics
- Year-wise student distribution
- Salary range statistics
- Top recruiting companies

---

## ⚙️ Settings Configuration

### Key Settings
```python
# Installed Apps
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'jobs.apps.JobsConfig',
    'applications.apps.ApplicationsConfig',
    'admin_panel.apps.AdminPanelConfig',
]

# Media Files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static Files
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Templates
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Login URLs
LOGIN_URL = 'student_login'
LOGIN_REDIRECT_URL = 'student_dashboard'
```

---

## 🐛 Common Issues & Solutions

### Issue: Resume upload not working
**Solution**: Ensure `media/` folder exists and has proper permissions

### Issue: Skills not matching
**Solution**: Ensure skills are comma-separated and exact matches

### Issue: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### Issue: "No such table" error
**Solution**: Run `python manage.py migrate`

---

## 📚 File Explanations

### Views
- **Class-Based Views**: Used for better code organization
- **LoginRequiredMixin**: Protects views requiring authentication
- **UserPassesTestMixin**: Admin-only access control

### Models
- **Abstract Models**: Not used, each app has concrete models
- **ForeignKey**: Creates relationships between models
- **OneToOneField**: Extends User model for Student/Company

### Forms
- **ModelForm**: Auto-generates forms from models
- **Form**: Custom forms for login
- **clean_*()**: Validation methods

### URLs
- **path()**: URL routing
- **include()**: Include app-specific URLs
- **reverse_lazy()**: Lazy URL resolution

---

## 🎓 Database Schema

```
User
├── Student
│   ├── Skills (TextField)
│   ├── Resume (FileField)
│   └── Applications (Related)
│
└── Company
    ├── Jobs (Related)
    └── JobApplications (Through Job)

Job
├── Company (ForeignKey)
├── Applications (Related)
└── RequiredSkills (TextField)

Application
├── Student (ForeignKey)
├── Job (ForeignKey)
└── SkillMatch (IntegerField)
```

---

## ✨ Future Enhancements

1. Email notifications on application updates
2. Interview scheduling system
3. Video interview integration
4. Skills recommendation engine
5. Resume parsing with ML
6. Salary negotiation platform
7. Alumni network integration
8. Internship management
9. Placement statistics export (PDF)
10. Mobile app version

---

## 📄 License

This is a complete educational project. Feel free to modify and use as needed.

---

## 👨‍💻 Developer Notes

- **Python**: 3.8+
- **Django**: 6.0.4
- **Database**: SQLite (can be changed in settings)
- **Front-end**: HTML5 + CSS3 (Responsive)
- **File Uploads**: PDF, DOC, DOCX (configurable)

---

## 🤝 Contributing

1. Create feature branches
2. Follow Django best practices
3. Write clear commit messages
4. Test thoroughly before submitting

---

**Built with ❤️ using Django**
