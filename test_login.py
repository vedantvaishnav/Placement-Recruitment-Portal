#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Company

# Get first company
company_user = User.objects.filter(username__startswith='company_').first()

if company_user:
    print(f"✓ Found test company user")
    print(f"  Username: {company_user.username}")
    print(f"  Has company profile: {hasattr(company_user, 'company')}")
    
    if hasattr(company_user, 'company'):
        company = company_user.company
        print(f"  Company name: {company.company_name}")
        print(f"\nLogin test:")
        print(f"  Username: {company_user.username}")
        print(f"  Password: Company@123")
        
        # Test authentication
        auth_user = authenticate(username=company_user.username, password='Company@123')
        if auth_user is not None:
            print(f"\n✓ Authentication successful!")
        else:
            print(f"\n✗ Authentication failed!")
    else:
        print(f"  ERROR: User has no company profile!")
else:
    print("No company users found in database")
