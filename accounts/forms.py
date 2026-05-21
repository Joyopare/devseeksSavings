from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Transaction, SavingsGoal
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        }

class UserProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    profile_picture = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Upload a profile picture (JPG, PNG, GIF - Max 5MB)"
    )
    
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'date_of_birth', 'gender', 'address', 'city_or_town', 
                  'id_card_number', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address'}),
            'city_or_town': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City or town'}),
            'id_card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID or passport number'}),
        }

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")
            if age > 120:
                raise ValidationError("Please enter a valid date of birth.")
        return dob

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            # Check file size (5MB limit)
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("Profile picture must be smaller than 5MB.")
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = picture.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError("Only JPG, PNG, and GIF files are allowed.")
        return picture

class SignUpForm(forms.Form):
    # User fields
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm password"
    )
    
    # Profile fields
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1234567890'})
    )
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    gender = forms.ChoiceField(
        choices=[('', 'Select Gender'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Street address'})
    )
    city_or_town = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City or town'})
    )
    id_card_number = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'National ID or passport number'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Upload profile picture (JPG, PNG, GIF - Max 5MB)"
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")
            if age > 120:
                raise ValidationError("Please enter a valid date of birth.")
        return dob

    def clean_id_card_number(self):
        id_card = self.cleaned_data.get('id_card_number')
        if id_card and UserProfile.objects.filter(id_card_number=id_card).exists():
            raise ValidationError("ID card number already registered.")
        return id_card

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:
                raise ValidationError("Profile picture must be smaller than 5MB.")
            
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            file_extension = picture.name.split('.')[-1].lower()
            if file_extension not in valid_extensions:
                raise ValidationError("Only JPG, PNG, and GIF files are allowed.")
        return picture

class DepositForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select user to deposit for (leave blank to deposit for yourself)"
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class WithdrawForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        help_text="Select user to withdraw for (leave blank to withdraw for yourself)"
    )
    def __init__(self, *args, **kwargs):
        self.user_balance = kwargs.pop('user_balance', 0)
        super().__init__(*args, **kwargs)
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
    description = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # For admin withdrawals, balance check is done in the view
        # Skip validation here to avoid checking wrong user's balance
        return amount

class TransactionRequestForm(forms.Form):
    request_type = forms.ChoiceField(
        choices=[('DEPOSIT', 'Deposit'), ('WITHDRAW', 'Withdraw')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter amount (GH₵)'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description (optional)'}),
        required=False
    )

class ProcessRequestForm(forms.Form):
    action = forms.ChoiceField(
        choices=[
            ('APPROVE', 'Approve'),
            ('REJECT', 'Reject'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    admin_notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add admin notes (optional)'}),
        required=False
    )

class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['goal_amount', 'deadline']
        widgets = {
            'goal_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
