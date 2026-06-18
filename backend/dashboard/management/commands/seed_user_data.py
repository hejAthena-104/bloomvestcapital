"""
Django management command to seed test data for a specific user.
Usage: python manage.py seed_user_data <username>
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta

from accounts.models import User, Notification
from investments.models import PaymentMethod, InvestmentPlan, Investment, ProfitHistory
from transactions.models import Transaction, Deposit, Withdrawal


class Command(BaseCommand):
    help = 'Seeds test data for a specific user (deposits, withdrawals, investments, profits)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to seed data for')

    def handle(self, *args, **options):
        username = options['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User "{username}" not found!'))
            self.stdout.write('\nAvailable users:')
            for u in User.objects.all()[:10]:
                self.stdout.write(f'  - {u.username} ({u.email})')
            return

        self.stdout.write(self.style.SUCCESS(f'\n🌱 Seeding test data for user: {user.username}\n'))

        # Seed deposits
        self.seed_deposits(user)

        # Seed withdrawals
        self.seed_withdrawals(user)

        # Seed investments and profits
        self.seed_investments(user)

        # Update user balance
        self.update_balance(user)

        self.stdout.write(self.style.SUCCESS(f'\n✅ Test data seeding completed for {user.username}!\n'))
        self.stdout.write(f'User balance: ${user.balance}')
        self.stdout.write(f'Total profit: ${user.total_profit}')

    def seed_deposits(self, user):
        """Create test deposits"""
        self.stdout.write('Creating test deposits...')

        # Get or create payment methods
        try:
            usdt = PaymentMethod.objects.get(name='USDT')
            bitcoin = PaymentMethod.objects.get(name='Bitcoin')
        except PaymentMethod.DoesNotExist:
            self.stdout.write(self.style.WARNING('  ⚠ Payment methods not found. Run: python manage.py seed_data'))
            return

        deposits_data = [
            {
                'amount': Decimal('1000.00'),
                'payment_method': usdt.name,
                'status': 'approved',
                'days_ago': 30,
            },
            {
                'amount': Decimal('2500.00'),
                'payment_method': bitcoin.name,
                'status': 'approved',
                'days_ago': 20,
            },
            {
                'amount': Decimal('500.00'),
                'payment_method': usdt.name,
                'status': 'approved',
                'days_ago': 10,
            },
            {
                'amount': Decimal('750.00'),
                'payment_method': bitcoin.name,
                'status': 'pending',
                'days_ago': 1,
            },
        ]

        count = 0
        for data in deposits_data:
            created_at = timezone.now() - timedelta(days=data['days_ago'])

            transaction = Transaction.objects.create(
                user=user,
                type='deposit',
                amount=data['amount'],
                payment_method=data['payment_method'],
                status=data['status'],
                description=f'Deposit via {data["payment_method"]}',
            )
            transaction.created_at = created_at
            if data['status'] == 'approved':
                transaction.processed_at = created_at + timedelta(hours=2)
            transaction.save()

            Deposit.objects.create(transaction=transaction)

            # Create notification
            Notification.objects.create(
                user=user,
                title=f'Deposit {data["status"].title()}',
                message=f'Your deposit of ${data["amount"]} via {data["payment_method"]} is {data["status"]}.',
                type='deposit',
                created_at=created_at,
            )

            count += 1
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ Created deposit: ${data["amount"]} ({data["payment_method"]}) - {data["status"]}'
            ))

        self.stdout.write(self.style.SUCCESS(f'✓ {count} deposits created\n'))

    def seed_withdrawals(self, user):
        """Create test withdrawals"""
        self.stdout.write('Creating test withdrawals...')

        # Set user withdrawal addresses first
        if not user.btc_address:
            user.btc_address = 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
        if not user.usdt_address:
            user.usdt_address = 'TXYZa1b2c3d4e5f6g7h8i9j0k1l2m3n4o5'
        user.save()

        withdrawals_data = [
            {
                'amount': Decimal('300.00'),
                'method': 'Bitcoin',
                'address': user.btc_address,
                'status': 'approved',
                'days_ago': 15,
            },
            {
                'amount': Decimal('150.00'),
                'method': 'USDT',
                'address': user.usdt_address,
                'status': 'approved',
                'days_ago': 5,
            },
            {
                'amount': Decimal('200.00'),
                'method': 'Bitcoin',
                'address': user.btc_address,
                'status': 'pending',
                'days_ago': 0,
            },
        ]

        count = 0
        for data in withdrawals_data:
            created_at = timezone.now() - timedelta(days=data['days_ago'])

            transaction = Transaction.objects.create(
                user=user,
                type='withdrawal',
                amount=data['amount'],
                payment_method=data['method'],
                status=data['status'],
                description=f'Withdrawal via {data["method"]}',
            )
            transaction.created_at = created_at
            if data['status'] == 'approved':
                transaction.processed_at = created_at + timedelta(hours=4)
            transaction.save()

            Withdrawal.objects.create(
                transaction=transaction,
                withdrawal_method=data['method'],
                withdrawal_address=data['address'],
            )

            # Create notification
            Notification.objects.create(
                user=user,
                title=f'Withdrawal {data["status"].title()}',
                message=f'Your withdrawal of ${data["amount"]} to {data["method"]} is {data["status"]}.',
                type='withdrawal',
                created_at=created_at,
            )

            count += 1
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ Created withdrawal: ${data["amount"]} ({data["method"]}) - {data["status"]}'
            ))

        self.stdout.write(self.style.SUCCESS(f'✓ {count} withdrawals created\n'))

    def seed_investments(self, user):
        """Create test investments and profits"""
        self.stdout.write('Creating test investments...')

        # Get investment plans
        try:
            starter_plan = InvestmentPlan.objects.get(name='STARTER PLAN')
            standard_plan = InvestmentPlan.objects.get(name='STANDARD PLAN')
        except InvestmentPlan.DoesNotExist:
            self.stdout.write(self.style.WARNING('  ⚠ Investment plans not found. Run: python manage.py seed_data'))
            return

        investments_data = [
            {
                'plan': starter_plan,
                'amount': Decimal('500.00'),
                'days_ago': 25,
                'status': 'completed',
            },
            {
                'plan': standard_plan,
                'amount': Decimal('2000.00'),
                'days_ago': 15,
                'status': 'active',
            },
            {
                'plan': starter_plan,
                'amount': Decimal('300.00'),
                'days_ago': 5,
                'status': 'active',
            },
        ]

        investment_count = 0
        profit_count = 0

        for data in investments_data:
            start_date = timezone.now() - timedelta(days=data['days_ago'])
            end_date = start_date + timedelta(days=data['plan'].duration_days)

            investment = Investment.objects.create(
                user=user,
                plan=data['plan'],
                amount=data['amount'],
                status=data['status'],
                start_date=start_date,
                end_date=end_date,
            )

            if data['status'] == 'completed':
                investment.completed_date = end_date
                investment.save()

            # Create profit history
            daily_profit = (data['amount'] * data['plan'].daily_profit_percentage) / 100

            # Determine how many days of profit to create
            if data['status'] == 'completed':
                profit_days = data['plan'].duration_days
            else:
                # For active investments, create profits for days passed
                profit_days = min(data['days_ago'], data['plan'].duration_days)

            for day in range(profit_days):
                profit_date = start_date + timedelta(days=day)

                ProfitHistory.objects.create(
                    user=user,
                    investment=investment,
                    amount=daily_profit,
                    date=profit_date,
                    description=f'Daily profit from {data["plan"].name}',
                )
                profit_count += 1

            # Update investment profit_earned
            investment.profit_earned = daily_profit * profit_days
            investment.save()

            investment_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'  ✓ Created investment: ${data["amount"]} ({data["plan"].name}) - {data["status"]}'
            ))
            self.stdout.write(f'    → Generated {profit_days} days of profit (${daily_profit}/day)')

        self.stdout.write(self.style.SUCCESS(f'✓ {investment_count} investments created'))
        self.stdout.write(self.style.SUCCESS(f'✓ {profit_count} profit records created\n'))

    def update_balance(self, user):
        """Calculate and update user balance"""
        self.stdout.write('Calculating user balance...')

        # Calculate approved deposits
        approved_deposits = Transaction.objects.filter(
            user=user,
            type='deposit',
            status='approved'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        # Calculate approved withdrawals
        approved_withdrawals = Transaction.objects.filter(
            user=user,
            type='withdrawal',
            status='approved'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        # Calculate active investments
        active_investments = Investment.objects.filter(
            user=user,
            status='active'
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        # Calculate total profit
        total_profit = ProfitHistory.objects.filter(
            user=user
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

        # Update user
        user.balance = approved_deposits - approved_withdrawals - active_investments + total_profit
        user.total_profit = total_profit
        user.save()

        self.stdout.write(f'  Approved deposits: ${approved_deposits}')
        self.stdout.write(f'  Approved withdrawals: ${approved_withdrawals}')
        self.stdout.write(f'  Active investments: ${active_investments}')
        self.stdout.write(f'  Total profit: ${total_profit}')
        self.stdout.write(self.style.SUCCESS(f'  Final balance: ${user.balance}\n'))


# Import models for aggregation
from django.db import models
