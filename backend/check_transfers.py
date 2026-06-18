"""
Check if transfers exist in the database
Run with: python manage.py shell < check_transfers.py
"""

from transactions.models import Transfer
from accounts.models import User

print("\n" + "="*60)
print("TRANSFER RECORDS IN DATABASE")
print("="*60)

transfers = Transfer.objects.all()
print(f"\nTotal transfers in database: {transfers.count()}\n")

for transfer in transfers:
    print(f"Transfer #{transfer.id}")
    print(f"  From: {transfer.sender.username}")
    print(f"  To: {transfer.recipient.username}")
    print(f"  Amount: ${transfer.amount}")
    print(f"  Fee: ${transfer.fee_amount}")
    print(f"  Total Deducted: ${transfer.total_deducted}")
    print(f"  Status: {transfer.status}")
    print(f"  Created: {transfer.created_at}")
    print(f"  Completed: {transfer.completed_at}")
    print(f"  Description: {transfer.description or 'N/A'}")
    print()

print("="*60)
print("\nCHECKING USER BALANCES")
print("="*60)

users = User.objects.all()
for user in users:
    sent = Transfer.objects.filter(sender=user).count()
    received = Transfer.objects.filter(recipient=user).count()
    print(f"\nUser: {user.username}")
    print(f"  Balance: ${user.balance}")
    print(f"  Transfers sent: {sent}")
    print(f"  Transfers received: {received}")

print("\n" + "="*60)
