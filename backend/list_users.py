import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from transactions.models import Transfer

print("\n" + "="*60)
print("ALL USERS IN THE SYSTEM")
print("="*60)

users = User.objects.all().order_by('-date_joined')

for user in users:
    print(f"\nUsername: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Full name: {user.get_full_name() or 'N/A'}")
    print(f"  Balance: ${user.balance}")
    print(f"  Is staff: {user.is_staff}")
    print(f"  Is superuser: {user.is_superuser}")
    print(f"  Date joined: {user.date_joined}")

    # Count transfers
    sent = Transfer.objects.filter(sender=user).count()
    received = Transfer.objects.filter(recipient=user).count()
    print(f"  Transfers: {sent} sent, {received} received")

print("\n" + "="*60)
print(f"Total users: {users.count()}")
print("="*60 + "\n")
