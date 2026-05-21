from django.contrib import admin
from .models import UserProfile, Transaction, SavingsGoal

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'description', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['user__username', 'description']

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal_amount', 'deadline', 'is_completed', 'created_at']
    list_filter = ['is_completed', 'created_at']
    search_fields = ['user__username']
