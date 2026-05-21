from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile

class Command(BaseCommand):
    help = 'Create UserProfile records for all users and show balance totals'

    def handle(self, *args, **options):
        self.stdout.write('Creating UserProfile records for all users...')
        
        # Create profiles for all users
        users = User.objects.all()
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f'Created profile for {user.username}')
            else:
                self.stdout.write(f'Profile already exists for {user.username}')
        
        # Show current balances
        profiles = UserProfile.objects.all()
        total_balance = 0
        
        self.stdout.write('\nCurrent User Balances:')
        for profile in profiles:
            balance = float(profile.balance)
            total_balance += balance
            self.stdout.write(f'  {profile.user.username}: GH{balance:.2f}')
        
        self.stdout.write(f'\nTotal Balance: GH{total_balance:.2f}')
        self.stdout.write(f'Number of Users: {users.count()}')
        self.stdout.write(f'Number of Profiles: {profiles.count()}')
