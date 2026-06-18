import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from decimal import Decimal

print("\n" + "="*60)
print("CREATING TEST USER FOR TRANSFERS")
print("="*60)

# Check if user2 already exists
if User.objects.filter(username='user2').exists():
    user2 = User.objects.get(username='user2')
    print(f"\nUser 'user2' already exists")
    print(f"  Balance: ${user2.balance}")
else:
    # Create user2
    user2 = User.objects.create_user(
        username='user2',
        email='user2@example.com',
        password='password123',
        first_name='Test',
        last_name='User2',
        balance=Decimal('5000.00')
    )
    print(f"\n[OK] Created user: user2")
    print(f"  Email: user2@example.com")
    print(f"  Password: password123")
    print(f"  Balance: $5000.00")

print("\n" + "="*60)
print("NOW YOU CAN TEST TRANSFERS")
print("="*60)
print("\n1. Login as 'admin' (or any user)")
print("2. Go to /dashboard/transfer-funds/")
print("3. Enter recipient username: user2")
print("4. Enter amount: 100")
print("5. Submit the form")
print("\nThe transfer should show up in history and admin panel!")
print("="*60 + "\n")
