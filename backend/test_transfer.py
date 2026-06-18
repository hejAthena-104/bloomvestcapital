import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from transactions.models import Transfer
from accounts.models import User
from decimal import Decimal

print("\n" + "="*60)
print("TESTING TRANSFER CREATION")
print("="*60)

# Get all users
users = User.objects.all()
print(f"\nTotal users: {users.count()}")

if users.count() < 2:
    print("ERROR: Need at least 2 users to test transfers")
    print("Creating test users...")

    # Create test users if needed
    if not User.objects.filter(username='testuser1').exists():
        user1 = User.objects.create_user(
            username='testuser1',
            email='test1@test.com',
            password='password123',
            balance=Decimal('1000.00')
        )
        print(f"Created user1: {user1.username} with balance ${user1.balance}")
    else:
        user1 = User.objects.get(username='testuser1')
        user1.balance = Decimal('1000.00')
        user1.save()
        print(f"Using existing user1: {user1.username} with balance ${user1.balance}")

    if not User.objects.filter(username='testuser2').exists():
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@test.com',
            password='password123',
            balance=Decimal('500.00')
        )
        print(f"Created user2: {user2.username} with balance ${user2.balance}")
    else:
        user2 = User.objects.get(username='testuser2')
        user2.balance = Decimal('500.00')
        user2.save()
        print(f"Using existing user2: {user2.username} with balance ${user2.balance}")
else:
    user1 = users[0]
    user2 = users[1]
    print(f"Using user1: {user1.username} (balance: ${user1.balance})")
    print(f"Using user2: {user2.username} (balance: ${user2.balance})")

print("\n" + "-"*60)
print("Creating transfer...")
print("-"*60)

amount = Decimal('50.00')

try:
    # Create transfer
    transfer = Transfer.objects.create(
        sender=user1,
        recipient=user2,
        amount=amount,
        description='Test transfer',
        fee_amount=Decimal('0.00'),
        status='pending'
    )

    print(f"[OK] Transfer created: #{transfer.id}")
    print(f"  From: {transfer.sender.username}")
    print(f"  To: {transfer.recipient.username}")
    print(f"  Amount: ${transfer.amount}")
    print(f"  Fee: ${transfer.fee_amount}")
    print(f"  Total: ${transfer.total_deducted}")
    print(f"  Status: {transfer.status}")

    # Try to complete it
    print("\nAttempting to complete transfer...")

    before_sender = user1.balance
    before_recipient = user2.balance

    if transfer.complete():
        # Refresh from database
        user1.refresh_from_db()
        user2.refresh_from_db()
        transfer.refresh_from_db()

        print("[OK] Transfer completed successfully!")
        print(f"\nSender balance: ${before_sender} -> ${user1.balance}")
        print(f"Recipient balance: ${before_recipient} -> ${user2.balance}")
        print(f"Transfer status: {transfer.status}")
    else:
        print("[FAILED] Transfer failed to complete")
        print(f"  Transfer status: {transfer.status}")

except Exception as e:
    print(f"[ERROR] Error creating transfer: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("FINAL STATE")
print("="*60)

transfers = Transfer.objects.all()
print(f"\nTotal transfers in database: {transfers.count()}")
for t in transfers:
    print(f"  #{t.id}: {t.sender.username} -> {t.recipient.username} ${t.amount} [{t.status}]")

print("\n" + "="*60)
