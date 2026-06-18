"""
Script to create initial payment methods for deposits and withdrawals.
Run this with: python manage.py shell < create_payment_methods.py
"""

from investments.models import PaymentMethod

# Create USDT payment method
usdt, created = PaymentMethod.objects.get_or_create(
    name='USDT',
    defaults={
        'type': 'both',  # Can be used for deposits and withdrawals
        'min_amount': 10.00,
        'max_amount': 100000.00,
        'charge_type': 'percentage',
        'charge_amount': 0.00,  # No fees
        'wallet_address': 'TXYZa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5',  # Replace with your actual USDT address
        'is_active': True,
        'description': 'Tether (USDT) - Stablecoin',
    }
)
if created:
    print(f"✓ Created USDT payment method")
else:
    print(f"✓ USDT payment method already exists")

# Create Bitcoin payment method
bitcoin, created = PaymentMethod.objects.get_or_create(
    name='Bitcoin',
    defaults={
        'type': 'both',
        'min_amount': 10.00,
        'max_amount': 100000.00,
        'charge_type': 'percentage',
        'charge_amount': 0.00,
        'wallet_address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Replace with your actual Bitcoin address
        'is_active': True,
        'description': 'Bitcoin (BTC)',
    }
)
if created:
    print(f"✓ Created Bitcoin payment method")
else:
    print(f"✓ Bitcoin payment method already exists")

# Create Ethereum payment method
ethereum, created = PaymentMethod.objects.get_or_create(
    name='Ethereum',
    defaults={
        'type': 'both',
        'min_amount': 10.00,
        'max_amount': 100000.00,
        'charge_type': 'percentage',
        'charge_amount': 0.00,
        'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',  # Replace with your actual Ethereum address
        'is_active': True,
        'description': 'Ethereum (ETH)',
    }
)
if created:
    print(f"✓ Created Ethereum payment method")
else:
    print(f"✓ Ethereum payment method already exists")

print("\n✓ All payment methods are set up!")
print("\nYou can now:")
print("1. Test deposits and withdrawals")
print("2. Modify payment methods in the admin panel at /admin/investments/paymentmethod/")
print("3. Update wallet addresses and fees as needed")
