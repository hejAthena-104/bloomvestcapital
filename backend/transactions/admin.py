from django.contrib import admin
from django.utils.html import format_html
from .models import Transaction, Deposit, Withdrawal, Transfer


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transactions"""
    list_display = (
        'id',
        'user',
        'type',
        'amount',
        'status_badge',
        'payment_method',
        'created_at',
        'processed_at'
    )
    list_filter = ('type', 'status', 'payment_method', 'created_at', 'processed_at')
    search_fields = (
        'user__username',
        'user__email',
        'payment_reference',
        'description'
    )
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50

    def status_badge(self, obj):
        """Display colored status badge"""
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'approved': 'green',
            'rejected': 'red',
            'cancelled': 'gray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )

    status_badge.short_description = 'Status'

    fieldsets = (
        ('Transaction Details', {
            'fields': ('user', 'type', 'amount', 'status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_reference', 'payment_address')
        }),
        ('Additional Information', {
            'fields': ('description', 'admin_note', 'recipient')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at')
        }),
    )

    actions = ['approve_transactions', 'reject_transactions']

    def approve_transactions(self, request, queryset):
        """Bulk approve transactions"""
        approved_count = 0
        for transaction in queryset.filter(status='pending'):
            if transaction.approve():
                approved_count += 1
        self.message_user(request, f'{approved_count} transaction(s) approved successfully.')

    approve_transactions.short_description = 'Approve selected transactions'

    def reject_transactions(self, request, queryset):
        """Bulk reject transactions"""
        rejected_count = 0
        for transaction in queryset.filter(status='pending'):
            transaction.reject()
            rejected_count += 1
        self.message_user(request, f'{rejected_count} transaction(s) rejected.')

    reject_transactions.short_description = 'Reject selected transactions'


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    """Admin interface for Deposits"""
    list_display = (
        'transaction',
        'get_user',
        'get_amount',
        'get_status',
        'get_payment_method',
        'has_proof',
        'get_created_at'
    )
    list_filter = (
        'transaction__status',
        'transaction__payment_method',
        'transaction__created_at'
    )
    search_fields = (
        'transaction__user__username',
        'transaction__user__email',
        'transaction__payment_reference'
    )
    readonly_fields = ('proof_preview',)

    fieldsets = (
        ('Transaction Info', {
            'fields': ('transaction',)
        }),
        ('Payment Proof', {
            'fields': ('proof_image', 'proof_preview')
        }),
    )

    actions = ['approve_deposits', 'reject_deposits']

    def proof_preview(self, obj):
        """Display proof image preview"""
        if obj.proof_image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 500px;" />',
                obj.proof_image.url
            )
        return 'No proof uploaded'
    proof_preview.short_description = 'Payment Proof Preview'

    def has_proof(self, obj):
        """Check if proof is uploaded"""
        if obj.proof_image:
            return '✓ Yes'
        return '✗ No'
    has_proof.short_description = 'Proof Uploaded'

    def approve_deposits(self, request, queryset):
        """Approve selected deposits"""
        count = 0
        for deposit in queryset:
            if deposit.transaction.status == 'pending':
                deposit.transaction.approve()
                count += 1
        self.message_user(request, f'{count} deposit(s) approved successfully.')
    approve_deposits.short_description = 'Approve selected deposits'

    def reject_deposits(self, request, queryset):
        """Reject selected deposits"""
        count = 0
        for deposit in queryset:
            if deposit.transaction.status == 'pending':
                deposit.transaction.reject(reason='Rejected by admin')
                count += 1
        self.message_user(request, f'{count} deposit(s) rejected.')
    reject_deposits.short_description = 'Reject selected deposits'

    def get_user(self, obj):
        return obj.transaction.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'transaction__user__username'

    def get_amount(self, obj):
        return f"${obj.transaction.amount}"
    get_amount.short_description = 'Amount'
    get_amount.admin_order_field = 'transaction__amount'

    def get_status(self, obj):
        return obj.transaction.status
    get_status.short_description = 'Status'
    get_status.admin_order_field = 'transaction__status'

    def get_payment_method(self, obj):
        return obj.transaction.payment_method
    get_payment_method.short_description = 'Payment Method'

    def get_created_at(self, obj):
        return obj.transaction.created_at
    get_created_at.short_description = 'Created'
    get_created_at.admin_order_field = 'transaction__created_at'


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    """Admin interface for Withdrawals"""
    list_display = (
        'transaction',
        'get_user',
        'get_amount',
        'withdrawal_method',
        'get_status',
        'get_created_at'
    )
    list_filter = (
        'transaction__status',
        'withdrawal_method',
        'transaction__created_at'
    )
    search_fields = (
        'transaction__user__username',
        'transaction__user__email',
        'withdrawal_address'
    )

    def get_user(self, obj):
        return obj.transaction.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'transaction__user__username'

    def get_amount(self, obj):
        return f"${obj.transaction.amount}"
    get_amount.short_description = 'Amount'
    get_amount.admin_order_field = 'transaction__amount'

    def get_status(self, obj):
        return obj.transaction.status
    get_status.short_description = 'Status'
    get_status.admin_order_field = 'transaction__status'

    def get_created_at(self, obj):
        return obj.transaction.created_at
    get_created_at.short_description = 'Created'
    get_created_at.admin_order_field = 'transaction__created_at'


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    """Admin interface for Fund Transfers"""
    list_display = ('sender', 'recipient', 'amount', 'fee_amount', 'total_deducted', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('sender__username', 'sender__email', 'recipient__username', 'recipient__email')
    readonly_fields = ('total_deducted', 'created_at', 'completed_at')

    fieldsets = (
        ('Transfer Details', {
            'fields': ('sender', 'recipient', 'amount', 'description')
        }),
        ('Fees & Total', {
            'fields': ('fee_amount', 'total_deducted')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )

    actions = ['complete_transfers', 'cancel_transfers']

    def complete_transfers(self, request, queryset):
        """Bulk complete transfers"""
        completed_count = 0
        for transfer in queryset.filter(status='pending'):
            if transfer.complete():
                completed_count += 1
        self.message_user(request, f'{completed_count} transfer(s) completed successfully.')
    complete_transfers.short_description = 'Complete selected transfers'

    def cancel_transfers(self, request, queryset):
        """Bulk cancel transfers"""
        cancelled_count = 0
        for transfer in queryset.filter(status='pending'):
            if transfer.cancel():
                cancelled_count += 1
        self.message_user(request, f'{cancelled_count} transfer(s) cancelled.')
    cancel_transfers.short_description = 'Cancel selected transfers'
