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
