"""
Management command to populate database with demo data for demonstration purposes
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random

from accounts.models import User
from investments.models import InvestmentPlan, Investment, ProfitHistory
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Populate database with demo data for demonstration purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing demo data before populating',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting demo data population...')

        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Investment.objects.all().delete()
            InvestmentPlan.objects.all().delete()
            Transaction.objects.exclude(user__is_superuser=True).delete()
            User.objects.filter(is_superuser=False).exclude(username='admin').delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        # Create investment plans
        self.create_investment_plans()

        # Create demo users with investments and transactions
        self.create_demo_users()

        self.stdout.write(self.style.SUCCESS('Demo data populated successfully!'))

    def create_investment_plans(self):
        """Create investment plans"""
        plans = [
            {
                'name': 'Starter Plan',
                'description': 'Perfect for beginners looking to start their investment journey',
                'min_amount': Decimal('100.00'),
                'max_amount': Decimal('999.00'),
                'daily_profit_percentage': Decimal('2.5'),
                'duration_days': 30,
                'total_return_percentage': Decimal('75.00'),
                'referral_bonus_percentage': Decimal('5.00'),
                'is_active': True,
                'is_featured': False,
                'order': 1
            },
            {
                'name': 'Silver Plan',
                'description': 'Enhanced returns for intermediate investors',
                'min_amount': Decimal('1000.00'),
                'max_amount': Decimal('4999.00'),
                'daily_profit_percentage': Decimal('3.5'),
                'duration_days': 45,
                'total_return_percentage': Decimal('157.50'),
                'referral_bonus_percentage': Decimal('7.00'),
                'is_active': True,
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Gold Plan',
                'description': 'Premium plan with accelerated growth',
                'min_amount': Decimal('5000.00'),
                'max_amount': Decimal('9999.00'),
                'daily_profit_percentage': Decimal('4.5'),
                'duration_days': 60,
                'total_return_percentage': Decimal('270.00'),
                'referral_bonus_percentage': Decimal('10.00'),
                'is_active': True,
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Platinum Plan',
                'description': 'Exclusive plan for serious investors',
                'min_amount': Decimal('10000.00'),
                'max_amount': Decimal('49999.00'),
                'daily_profit_percentage': Decimal('5.5'),
                'duration_days': 90,
                'total_return_percentage': Decimal('495.00'),
                'referral_bonus_percentage': Decimal('12.00'),
                'is_active': True,
                'is_featured': True,
                'order': 4
            },
            {
                'name': 'Diamond Plan',
                'description': 'Ultimate plan with maximum returns',
                'min_amount': Decimal('50000.00'),
                'max_amount': None,
                'daily_profit_percentage': Decimal('7.0'),
                'duration_days': 120,
                'total_return_percentage': Decimal('840.00'),
                'referral_bonus_percentage': Decimal('15.00'),
                'is_active': True,
                'is_featured': True,
                'order': 5
            },
        ]

        for plan_data in plans:
            plan, created = InvestmentPlan.objects.get_or_create(
                name=plan_data['name'],
                defaults=plan_data
            )
            if created:
                self.stdout.write(f'Created plan: {plan.name}')

    def create_demo_users(self):
        """Create demo users with sample data"""
        # Get or create the admin user who registered
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.create_superuser(
                'admin',
                'admin@dynamicsdigitalasset.com',
                'admin123456'
            )

        # Update admin user with demo data
        admin_user.balance = Decimal('15000.00')
        admin_user.total_profit = Decimal('5000.00')
        admin_user.total_bonus = Decimal('500.00')
        admin_user.referral_bonus = Decimal('250.00')
        admin_user.is_verified = True
        admin_user.save()

        # Create some investments for admin
        plans = InvestmentPlan.objects.all()

        # Active investment
        active_plan = plans.filter(name='Gold Plan').first()
        if active_plan:
            investment = Investment.objects.create(
                user=admin_user,
                plan=active_plan,
                amount=Decimal('7500.00'),
                profit_earned=Decimal('2250.00'),
                status='active',
                start_date=timezone.now() - timedelta(days=30),
                last_profit_date=timezone.now()
            )

            # Add some profit history
            for i in range(15):
                ProfitHistory.objects.create(
                    investment=investment,
                    user=admin_user,
                    amount=Decimal('150.00'),
                    description=f"Daily profit - Day {i+1}"
                )

        # Completed investment
        completed_plan = plans.filter(name='Silver Plan').first()
        if completed_plan:
            Investment.objects.create(
                user=admin_user,
                plan=completed_plan,
                amount=Decimal('3000.00'),
                profit_earned=Decimal('4725.00'),
                total_return=Decimal('4725.00'),
                status='completed',
                start_date=timezone.now() - timedelta(days=90),
                end_date=timezone.now() - timedelta(days=45),
                completed_date=timezone.now() - timedelta(days=45)
            )

        # Create transactions
        transactions_data = [
            {
                'type': 'deposit',
                'amount': Decimal('10000.00'),
                'status': 'approved',
                'payment_method': 'bitcoin',
                'description': 'Initial deposit via Bitcoin',
                'created_at': timezone.now() - timedelta(days=100),
                'processed_at': timezone.now() - timedelta(days=100)
            },
            {
                'type': 'deposit',
                'amount': Decimal('5000.00'),
                'status': 'approved',
                'payment_method': 'ethereum',
                'description': 'Second deposit via Ethereum',
                'created_at': timezone.now() - timedelta(days=60),
                'processed_at': timezone.now() - timedelta(days=60)
            },
            {
                'type': 'withdrawal',
                'amount': Decimal('2500.00'),
                'status': 'approved',
                'payment_method': 'bitcoin',
                'description': 'Partial profit withdrawal',
                'created_at': timezone.now() - timedelta(days=20),
                'processed_at': timezone.now() - timedelta(days=19)
            },
            {
                'type': 'bonus',
                'amount': Decimal('500.00'),
                'status': 'approved',
                'description': 'Welcome bonus',
                'created_at': timezone.now() - timedelta(days=95),
                'processed_at': timezone.now() - timedelta(days=95)
            },
            {
                'type': 'referral',
                'amount': Decimal('250.00'),
                'status': 'approved',
                'description': 'Referral bonus from user signup',
                'created_at': timezone.now() - timedelta(days=40),
                'processed_at': timezone.now() - timedelta(days=40)
            },
        ]

        for trans_data in transactions_data:
            Transaction.objects.create(user=admin_user, **trans_data)

        self.stdout.write(self.style.SUCCESS(f'Created demo data for user: {admin_user.username}'))