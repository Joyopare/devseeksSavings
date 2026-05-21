#!/usr/bin/env python
"""
Setup script to create admin user for Finance Savings App
Run this script after migrations to create an admin user
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_savings.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Create admin user if it doesn't exist"""
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Admin user created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print("\nAccess the admin panel at: http://127.0.0.1:8000/admin/")
    else:
        print(f"Admin user '{username}' already exists.")

if __name__ == '__main__':
    create_admin_user()
