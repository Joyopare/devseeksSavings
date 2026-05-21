from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('set-savings-goal/', views.set_savings_goal, name='set_savings_goal'),
    path('transaction-history/', views.transaction_history, name='transaction_history'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard-data/', views.admin_dashboard_data, name='admin_dashboard_data'),
    path('request-transaction/', views.request_transaction, name='request_transaction'),
    path('transaction-requests/', views.transaction_requests, name='transaction_requests'),
    path('process-request/<int:request_id>/', views.process_request, name='process_request'),
    path('approve-request/<int:request_id>/', views.approve_request, name='approve_request'),
    path('reject-request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('user-management/', views.user_management, name='user_management'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('goal-management/', views.goal_management, name='goal_management'),
    path('add-goal/<int:user_id>/', views.add_goal, name='add_goal'),
    path('edit-goal/<int:goal_id>/', views.edit_goal, name='edit_goal'),
    path('delete-goal/<int:goal_id>/', views.delete_goal, name='delete_goal'),
    path('notifications/', views.admin_notifications, name='admin_notifications'),
    path('send-message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('sent-messages/', views.sent_messages, name='sent_messages'),
    path('user-notifications/', views.user_notifications, name='user_notifications'),
]
