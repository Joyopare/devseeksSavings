from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Personal Information
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
        blank=True,
        null=True,
        help_text="Enter your phone number with country code"
    )
    date_of_birth = models.DateField(null=True, blank=True, help_text="Format: YYYY-MM-DD")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    
    # Address Information
    address = models.TextField(max_length=500, blank=True, help_text="Street address")
    city_or_town = models.CharField(max_length=100, blank=True, help_text="City or town name")
    
    # Identification
    id_card_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        help_text="National ID or passport number"
    )
    
    # Profile
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
        help_text="Upload your profile picture"
    )
    
    # Financial Information
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name}'s Profile" if full_name else f"{self.user.username}'s Profile"
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()
    
    @property
    def age(self):
        from datetime import date
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ${self.amount}"

class TransactionRequest(models.Model):
    REQUEST_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('PROCESSED', 'Processed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requests')
    admin_notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.request_type} - ${self.amount}"
    
    class Meta:
        ordering = ['-created_at']

class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    withdrawal_request_created = models.BooleanField(default=False)  # Track if withdrawal request was created

    def __str__(self):
        return f"{self.user.username}'s Goal: GH₵{self.goal_amount}"
    
    @property
    def progress_percentage(self):
        current_balance = self.user.userprofile.balance
        return (current_balance / self.goal_amount) * 100 if self.goal_amount > 0 else 0
    
    @property
    def is_goal_reached(self):
        current_balance = self.user.userprofile.balance
        return current_balance >= self.goal_amount

    class Meta:
        ordering = ['-created_at']

class AdminNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_request = models.ForeignKey('TransactionRequest', on_delete=models.CASCADE, null=True, blank=True)
    related_goal = models.ForeignKey('SavingsGoal', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, default='REQUEST', choices=[
        ('REQUEST', 'Transaction Request'),
        ('GOAL', 'Goal Set'),
        ('SYSTEM', 'System Notification'),
    ])
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
    
    class Meta:
        ordering = ['-created_at']

class UserMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}: {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_request = models.ForeignKey('TransactionRequest', on_delete=models.CASCADE, null=True, blank=True)
    related_goal = models.ForeignKey('SavingsGoal', on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=20, default='REQUEST', choices=[
        ('REQUEST_APPROVED', 'Request Approved'),
        ('REQUEST_REJECTED', 'Request Rejected'),
        ('GOAL_REACHED', 'Goal Reached'),
        ('GOAL_COMPLETED', 'Goal Completed'),
    ])
    
    def __str__(self):
        return f"User Notification for {self.user.username}: {self.title}"
    
    class Meta:
        ordering = ['-created_at']
