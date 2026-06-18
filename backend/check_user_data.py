"""
Quick script to check if a user has seeded data.
Run with: python manage.py shell < check_user_data.py
"""

import sys
from accounts.models import User
from transactions.models import Transaction
from investments.models import Investment, ProfitHistory

# Get username from command line or use default
username = input("Enter username to check (or press Enter for all users): ").strip()

if username:
    try:
        user = User.objects.get(username=username)
        users = [user]
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found!")
        sys.exit(1)
else:
    users = User.objects.all()
    print(f"Found {users.count()} users\n")

for user in users:
    print(f"\n{'='*60}")
    print(f"User: {user.username} ({user.email})")
    print(f"{'='*60}")

    # Count transactions by type
    deposits = Transaction.objects.filter(user=user, type='deposit').count()
    withdrawals = Transaction.objects.filter(user=user, type='withdrawal').count()

    # Count investments
    investments = Investment.objects.filter(user=user).count()
    active_investments = Investment.objects.filter(user=user, status='active').count()

    # Count profits
    profits = ProfitHistory.objects.filter(user=user).count()

    print(f"Deposits: {deposits}")
    print(f"Withdrawals: {withdrawals}")
    print(f"Investments: {investments} ({active_investments} active)")
    print(f"Profit Records: {profits}")
    print(f"Balance: ${user.balance}")
    print(f"Total Profit: ${user.total_profit}")

    if deposits == 0 and withdrawals == 0 and investments == 0:
        print("\n⚠️  No data found for this user!")
        print(f"   Run: python manage.py seed_user_data {user.username}")
    else:
        print("\n✅ User has transaction data")

print("\n" + "="*60)
