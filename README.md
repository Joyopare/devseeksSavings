# Finance Savings Django Application

A comprehensive finance savings management web application built with Django, Bootstrap5, and JavaScript.

## Features

Based on the finance savings flowchart, this application includes:

### User Authentication
- User registration and login
- Secure session management
- Email/phone verification ready

### Dashboard
- View current account balance
- Quick access to all features
- Recent transactions overview
- Savings goals progress tracking

### Core Functionality
1. **View Balance** - Real-time balance display
2. **Deposit Money** - Add funds to account
3. **Withdraw Money** - Remove funds with balance validation
4. **Set Savings Goal** - Define financial goals with deadlines
5. **View Transactions** - Complete transaction history
6. **Logout** - Secure session termination

### Additional Features
- Transaction history with filtering
- Savings goal progress tracking
- Responsive design for all devices
- Real-time form validation
- Animated UI elements
- Keyboard shortcuts

## Technology Stack

- **Backend**: Django 4.2.7
- **Frontend**: Bootstrap5, HTML5, JavaScript
- **Database**: SQLite (development ready)
- **Styling**: Custom CSS with animations
- **Forms**: Django forms with Bootstrap5 integration

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup Instructions

1. **Clone or download the project files**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Unix/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000`

## Usage

### Getting Started
1. Visit the homepage
2. Click "Get Started" to create an account
3. Login with your credentials
4. Access the dashboard to manage your finances

### Dashboard Features
- **Current Balance**: View your available funds
- **Quick Actions**: Deposit, withdraw, set goals
- **Recent Transactions**: Latest 5 transactions
- **Savings Goals**: Progress tracking for active goals

### Transaction Management
- **Deposit**: Add money with optional description
- **Withdraw**: Remove money (balance validation included)
- **History**: View all transactions with totals

### Savings Goals
- Set target amounts and deadlines
- Track progress visually with progress bars
- Get notifications when goals are reached

## Project Structure

```
finance_savings/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── finance_savings/         # Main project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── accounts/               # User accounts app
│   ├── models.py            # User profile, transactions, goals
│   ├── views.py             # Account-related views
│   ├── forms.py             # Django forms
│   └── urls.py              # Account URL patterns
├── savings/                # Savings app
│   ├── views.py            # Savings overview
│   └── urls.py             # Savings URL patterns
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── home.html           # Homepage
│   ├── accounts/           # Account templates
│   └── savings/            # Savings templates
└── static/                 # Static files
    ├── css/
    │   └── custom.css      # Custom styles
    └── js/
        └── main.js         # JavaScript functionality
```

## Database Models

### UserProfile
- Linked to Django User model
- Stores account balance
- Tracks creation and update times

### Transaction
- Records all deposits and withdrawals
- Includes amount, type, description, and timestamp
- Linked to user account

### SavingsGoal
- Target amount and deadline
- Progress tracking
- Completion status

## Security Features

- CSRF protection
- Secure password handling
- Session management
- Form validation
- SQL injection prevention
- XSS protection

## Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## Keyboard Shortcuts

- `Ctrl/Cmd + D`: Go to deposit page
- `Ctrl/Cmd + W`: Go to withdraw page  
- `Ctrl/Cmd + H`: Go to transaction history

## Admin Panel

Access the Django admin panel at `/admin/` with superuser credentials to:
- Manage users
- View transactions
- Monitor savings goals
- Configure application settings

## Development

### Adding New Features
1. Create models in appropriate app
2. Update views and forms
3. Add URL patterns
4. Create templates
5. Update static files if needed

### Customization
- Modify `static/css/custom.css` for styling
- Update `static/js/main.js` for JavaScript functionality
- Edit templates in `templates/` directory

## Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure proper database
3. Set up static file serving
4. Configure domain and SSL
5. Set up proper logging
6. Update `SECRET_KEY`

## License

This project is for educational purposes. Feel free to modify and use as needed.

## Support

For issues or questions, refer to Django documentation or contact the development team.
