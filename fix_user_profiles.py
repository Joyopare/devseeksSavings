#!/usr/bin/env python
"""
Script to create UserProfile for existing users who don't have one
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finance_savings.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

def create_missing_user_profiles():
    """Create UserProfile for users who don't have one"""
    users_without_profile = User.objects.filter(userprofile__isnull=True)
    
    print(f"Found {users_without_profile.count()} users without UserProfile")
    
    for user in users_without_profile:
        UserProfile.objects.create(user=user)
        print(f"Created UserProfile for user: {user.username}")
    
    print("All missing UserProfiles have been created!")

if __name__ == '__main__':
    create_missing_user_profiles()
