"""
Django management command to seed the database with dummy data.
Usage: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from accounts.models import User
from investments.models import PaymentMethod, InvestmentPlan, Investment, ProfitHistory
from transactions.models import Transaction, Deposit, Withdrawal


class Command(BaseCommand):
    help = 'Seeds the database with dummy data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🌱 Starting database seeding...\n'))

        # Seed Payment Methods
        self.seed_payment_methods()

        # Seed Investment Plans
        self.seed_investment_plans()

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeding completed successfully!\n'))
        self.stdout.write(self.style.WARNING('📝 Note: Run the development server and visit /admin/ to manage this data\n'))

    def seed_payment_methods(self):
        """Create payment methods for deposits and withdrawals"""
        self.stdout.write('Creating payment methods...')

        payment_methods_data = [
            {
                'name': 'USDT',
                'type': 'both',
                'min_amount': Decimal('10.00'),
                'max_amount': Decimal('100000.00'),
                'charge_type': 'percentage',
                'charge_amount': Decimal('0.00'),
                'duration': '1-24 hours',
                'wallet_address': 'TXYZa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5',
                'is_active': True,
                'order': 1,
            },
            {
                'name': 'Bitcoin',
                'type': 'both',
                'min_amount': Decimal('10.00'),
                'max_amount': Decimal('100000.00'),
                'charge_type': 'percentage',
                'charge_amount': Decimal('0.00'),
                'duration': '1-24 hours',
                'wallet_address': 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh',
                'is_active': True,
                'order': 2,
            },
            {
                'name': 'Ethereum',
                'type': 'both',
                'min_amount': Decimal('10.00'),
                'max_amount': Decimal('100000.00'),
                'charge_type': 'percentage',
                'charge_amount': Decimal('0.00'),
                'duration': '1-24 hours',
                'wallet_address': '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb0',
                'is_active': True,
                'order': 3,
            },
            {
                'name': 'Litecoin',
                'type': 'both',
                'min_amount': Decimal('10.00'),
                'max_amount': Decimal('100000.00'),
                'charge_type': 'percentage',
                'charge_amount': Decimal('0.00'),
                'duration': '1-24 hours',
                'wallet_address': 'LdP8Qox1VAhCzLJNqrr74YovaWYyNBUWvL',
                'is_active': True,
                'order': 4,
            },
        ]

        created_count = 0
        updated_count = 0
        for data in payment_methods_data:
            name = data.pop('name')
            payment_method, created = PaymentMethod.objects.update_or_create(
                name=name,
                defaults=data
            )
            data['name'] = name  # Restore for logging
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created payment method: {name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Updated payment method: {name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Payment methods: {created_count} created, {updated_count} updated\n'))

    def seed_investment_plans(self):
        """Create investment plans"""
        self.stdout.write('Creating investment plans...')

        plans_data = [
            {
                'name': 'STARTER PLAN',
                'min_amount': Decimal('100.00'),
                'max_amount': Decimal('999.00'),
                'daily_profit_percentage': Decimal('5.00'),
                'duration_days': 7,
                'total_return_percentage': Decimal('35.00'),
                'is_active': True,
                'description': 'Perfect for beginners - Start your investment journey with our starter plan',
            },
            {
                'name': 'STANDARD PLAN',
                'min_amount': Decimal('1000.00'),
                'max_amount': Decimal('4999.00'),
                'daily_profit_percentage': Decimal('7.50'),
                'duration_days': 14,
                'total_return_percentage': Decimal('105.00'),
                'is_active': True,
                'description': 'Balanced growth plan with competitive daily returns',
            },
            {
                'name': 'PROFESSIONAL PLAN',
                'min_amount': Decimal('5000.00'),
                'max_amount': Decimal('14999.00'),
                'daily_profit_percentage': Decimal('10.00'),
                'duration_days': 21,
                'total_return_percentage': Decimal('210.00'),
                'is_active': True,
                'description': 'For serious investors looking for higher returns',
            },
            {
                'name': 'RETIREMENT PLAN',
                'min_amount': Decimal('15000.00'),
                'max_amount': Decimal('49999.00'),
                'daily_profit_percentage': Decimal('15.00'),
                'duration_days': 30,
                'total_return_percentage': Decimal('450.00'),
                'is_active': True,
                'description': 'Long-term investment plan with maximum returns',
            },
            {
                'name': 'VIP PLAN',
                'min_amount': Decimal('50000.00'),
                'max_amount': Decimal('1000000.00'),
                'daily_profit_percentage': Decimal('20.00'),
                'duration_days': 30,
                'total_return_percentage': Decimal('600.00'),
                'is_active': True,
                'description': 'Exclusive plan for high-net-worth investors',
            },
        ]

        created_count = 0
        for data in plans_data:
            plan, created = InvestmentPlan.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'  ✓ Created plan: {data["name"]} '
                    f'(${data["min_amount"]}-${data["max_amount"]}, '
                    f'{data["daily_profit_percentage"]}% daily, '
                    f'{data["duration_days"]} days)'
                ))
            else:
                self.stdout.write(f'  - Plan already exists: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Investment plans: {created_count} created, {len(plans_data) - created_count} already existed\n'))
