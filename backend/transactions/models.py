from django.db import models
from django.utils import timezone
from accounts.models import User


class Transaction(models.Model):
    """Model for all user transactions (deposits, withdrawals, transfers)"""

    TYPE_CHOICES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('bonus', 'Bonus'),
        ('referral', 'Referral Bonus'),
        ('profit', 'Profit'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('bitcoin', 'Bitcoin'),
        ('ethereum', 'Ethereum'),
        ('usdt', 'USDT (TRC20)'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('stripe', 'Credit/Debit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

    # Transaction details
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment details
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_reference = models.CharField(max_length=255, blank=True, help_text="Transaction ID or reference")
    payment_address = models.CharField(max_length=255, blank=True, help_text="Wallet address or account number")

    # Additional info
    description = models.TextField(blank=True)
    admin_note = models.TextField(blank=True, help_text="Internal notes for administrators")

    # For transfers
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_transfers')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.type} - ${self.amount} - {self.status}"

    def approve(self):
        """Approve transaction and update user balance"""
        if self.status != 'pending':
            return False

        self.status = 'approved'
        self.processed_at = timezone.now()

        # Update user balance based on transaction type
        if self.type == 'deposit':
            self.user.balance += self.amount
        elif self.type == 'withdrawal':
            if self.user.balance >= self.amount:
                self.user.balance -= self.amount
            else:
                return False  # Insufficient balance
        elif self.type in ['bonus', 'referral', 'profit']:
            self.user.balance += self.amount

        self.user.save()
        self.save()
        return True

    def reject(self, reason=''):
        """Reject transaction"""
        self.status = 'rejected'
        self.admin_note = reason
        self.processed_at = timezone.now()
        self.save()


class Deposit(models.Model):
    """Model for deposit requests (extends Transaction)"""

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='deposit_details')

    # Proof of payment
    proof_image = models.ImageField(upload_to='deposits/', null=True, blank=True)

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'
        ordering = ['-transaction__created_at']

    def __str__(self):
        return f"Deposit - {self.transaction}"


class Withdrawal(models.Model):
    """Model for withdrawal requests (extends Transaction)"""

    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='withdrawal_details')

    # Withdrawal details
    withdrawal_address = models.CharField(max_length=255, help_text="Wallet address or account details")
    withdrawal_method = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Withdrawal'
        verbose_name_plural = 'Withdrawals'
        ordering = ['-transaction__created_at']

    def __str__(self):
        return f"Withdrawal - {self.transaction}"


class Transfer(models.Model):
    """Model for internal fund transfers between users"""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transfers_received')

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True)

    # Fees
    fee_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_deducted = models.DecimalField(max_digits=15, decimal_places=2, help_text="Amount + Fee")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Transfer'
        verbose_name_plural = 'Transfers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username} - ${self.amount}"

    def save(self, *args, **kwargs):
        # Calculate total deducted (amount + fee)
        if not self.total_deducted or self.total_deducted == 0:
            self.total_deducted = self.amount + self.fee_amount
        super().save(*args, **kwargs)

    def complete(self):
        """Complete the transfer - deduct from sender and credit recipient"""
        if self.status != 'pending':
            return False

        # Check if sender has sufficient balance
        if self.sender.balance < self.total_deducted:
            self.status = 'failed'
            self.save()
            return False

        # Deduct from sender
        self.sender.balance -= self.total_deducted
        self.sender.save()

        # Credit recipient
        self.recipient.balance += self.amount
        self.recipient.save()

        # Update status
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

        return True

    def cancel(self):
        """Cancel the transfer"""
        if self.status == 'pending':
            self.status = 'cancelled'
            self.save()
            return True
        return False
