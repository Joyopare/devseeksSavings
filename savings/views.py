from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import SavingsGoal, Transaction

@login_required
def savings_overview(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')[:10]
    
    context = {
        'goals': goals,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'savings/overview.html', context)
