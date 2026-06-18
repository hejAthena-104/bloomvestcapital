from django.db import models
from django.utils import timezone
from accounts.models import User
from decimal import Decimal


class InvestmentPlan(models.Model):
    """Model for investment plans"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    daily_profit_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Daily profit percentage")
    duration_days = models.IntegerField(help_text="Duration in days")
    total_return_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    # Features
    referral_bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Display order
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Investment Plan'
        verbose_name_plural = 'Investment Plans'
        ordering = ['order', 'min_amount']

    def __str__(self):
        return f"{self.name} - {self.daily_profit_percentage}% daily"

    @property
    def profit_range(self):
        """Calculate profit range based on min and max amount"""
        min_profit = (self.min_amount * self.total_return_percentage) / 100
        if self.max_amount:
            max_profit = (self.max_amount * self.total_return_percentage) / 100
            return f"${min_profit} - ${max_profit}"
        return f"${min_profit}+"


class Investment(models.Model):
    """Model for user investments"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    plan = models.ForeignKey(InvestmentPlan, on_delete=models.PROTECT, related_name='investments')

    # Investment details
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    profit_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_return = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    # Status and dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    last_profit_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - ${self.amount}"

    def save(self, *args, **kwargs):
        # Calculate end date on first save
        if not self.pk and not self.end_date:
            from datetime import timedelta
            self.end_date = timezone.now() + timedelta(days=self.plan.duration_days)

        # Calculate total expected return
        if not self.total_return or self.total_return == 0:
            self.total_return = (self.amount * self.plan.total_return_percentage) / 100

        super().save(*args, **kwargs)

    @property
    def days_remaining(self):
        """Calculate days remaining until investment completes"""
        if self.status == 'completed':
            return 0
        if not self.end_date:
            return 0
        delta = self.end_date - timezone.now()
        return max(0, delta.days)

    @property
    def progress_percentage(self):
        """Calculate investment progress percentage"""
        if self.status == 'completed':
            return 100
        if not self.plan_id or not self.start_date:
            return 0

        total_days = self.plan.duration_days
        elapsed_days = (timezone.now() - self.start_date).days
        return min(100, (elapsed_days / total_days) * 100 if total_days > 0 else 0)

    @property
    def expected_daily_profit(self):
        """Calculate expected daily profit"""
        if not self.plan_id:
            return Decimal('0.00')
        return (self.amount * self.plan.daily_profit_percentage) / 100

    def is_active(self):
        """Check if investment is still active"""
        return self.status == 'active' and self.end_date and timezone.now() < self.end_date


class ProfitHistory(models.Model):
    """Model for tracking profit payments"""

    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, related_name='profit_history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profit_history')

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, default="Daily profit")

    class Meta:
        verbose_name = 'Profit History'
        verbose_name_plural = 'Profit History'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.date.strftime('%Y-%m-%d')}"


class PaymentMethod(models.Model):
    """Model for payment methods (deposit & withdrawal)"""

    TYPE_CHOICES = [
        ('deposit', 'Deposit Only'),
        ('withdrawal', 'Withdrawal Only'),
        ('both', 'Both'),
    ]

    CHARGE_TYPE_CHOICES = [
        ('fixed', 'Fixed Amount'),
        ('percentage', 'Percentage'),
    ]

    # Basic info
    name = models.CharField(max_length=50, unique=True, help_text="e.g., USDT, Bitcoin, Ethereum")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='both')
    icon = models.ImageField(upload_to='payment_methods/', blank=True, null=True)

    # Limits
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, default=10.00)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Leave blank for no limit")

    # Charges/Fees
    charge_type = models.CharField(max_length=20, choices=CHARGE_TYPE_CHOICES, default='percentage')
    charge_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Amount or percentage based on charge type")

    # Processing
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '1-24 hours', 'Instant'")

    # For crypto deposits - the platform's wallet address
    wallet_address = models.CharField(max_length=200, blank=True, help_text="Platform wallet address for receiving payments")
    qr_code = models.ImageField(upload_to='payment_qr_codes/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)

    # Display order
    order = models.IntegerField(default=0, help_text="Display order")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment Method'
        verbose_name_plural = 'Payment Methods'
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def calculate_charge(self, amount):
        """Calculate charge for a given amount"""
        if self.charge_type == 'fixed':
            return self.charge_amount
        else:  # percentage
            return (amount * self.charge_amount) / 100

    def get_total_amount(self, base_amount):
        """Calculate total amount including charges"""
        return base_amount + self.calculate_charge(base_amount)
