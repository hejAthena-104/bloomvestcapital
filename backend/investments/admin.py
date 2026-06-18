from django.contrib import admin
from .models import InvestmentPlan, Investment, ProfitHistory, PaymentMethod


@admin.register(InvestmentPlan)
class InvestmentPlanAdmin(admin.ModelAdmin):
    """Admin interface for Investment Plans"""
    list_display = (
        'name',
        'min_amount',
        'max_amount',
        'daily_profit_percentage',
        'duration_days',
        'total_return_percentage',
        'is_active',
        'is_featured',
        'order'
    )
    list_filter = ('is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_active', 'is_featured', 'order')
    ordering = ('order', 'min_amount')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'order')
        }),
        ('Investment Terms', {
            'fields': (
                'min_amount',
                'max_amount',
                'duration_days',
                'daily_profit_percentage',
                'total_return_percentage'
            )
        }),
        ('Features', {
            'fields': ('referral_bonus_percentage', 'is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    """Admin interface for Investments"""
    list_display = (
        'user',
        'plan',
        'amount',
        'profit_earned',
        'status',
        'start_date',
        'end_date',
        'display_progress'
    )
    list_filter = ('status', 'plan', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email', 'plan__name')

    def get_readonly_fields(self, request, obj=None):
        base = ['start_date', 'created_at', 'updated_at']
        if obj:
            base += ['display_progress', 'display_days_remaining', 'display_daily_profit']
        return base

    def get_fieldsets(self, request, obj=None):
        base_fieldsets = [
            ('Investment Details', {
                'fields': ('user', 'plan', 'amount', 'status')
            }),
        ]
        if obj:
            base_fieldsets.append(
                ('Financial Information', {
                    'fields': ('profit_earned', 'total_return', 'display_daily_profit')
                })
            )
            base_fieldsets.append(
                ('Timeline', {
                    'fields': (
                        'start_date',
                        'end_date',
                        'last_profit_date',
                        'completed_date',
                        'display_days_remaining',
                        'display_progress'
                    )
                })
            )
        else:
            base_fieldsets.append(
                ('Financial Information', {
                    'fields': ('profit_earned', 'total_return')
                })
            )
            base_fieldsets.append(
                ('Timeline', {
                    'fields': ('end_date', 'last_profit_date', 'completed_date')
                })
            )
        base_fieldsets.append(
            ('Timestamps', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',)
            })
        )
        return base_fieldsets

    def display_progress(self, obj):
        if not obj or not obj.pk:
            return "N/A"
        return f"{obj.progress_percentage:.1f}%"
    display_progress.short_description = 'Progress'

    def display_days_remaining(self, obj):
        if not obj or not obj.pk:
            return "N/A"
        return obj.days_remaining
    display_days_remaining.short_description = 'Days Remaining'

    def display_daily_profit(self, obj):
        if not obj or not obj.pk:
            return "N/A"
        return f"${obj.expected_daily_profit:.2f}"
    display_daily_profit.short_description = 'Expected Daily Profit'

    actions = ['mark_active', 'mark_completed', 'mark_cancelled']

    def mark_active(self, request, queryset):
        count = queryset.filter(status='pending').update(status='active')
        self.message_user(request, f'{count} investment(s) marked as active.')
    mark_active.short_description = 'Mark selected as Active (pending only)'

    def mark_completed(self, request, queryset):
        from django.utils import timezone
        count = queryset.filter(status='active').update(status='completed', completed_date=timezone.now())
        self.message_user(request, f'{count} investment(s) marked as completed.')
    mark_completed.short_description = 'Mark selected as Completed (active only)'

    def mark_cancelled(self, request, queryset):
        count = queryset.exclude(status='completed').update(status='cancelled')
        self.message_user(request, f'{count} investment(s) marked as cancelled.')
    mark_cancelled.short_description = 'Mark selected as Cancelled (except completed)'


@admin.register(ProfitHistory)
class ProfitHistoryAdmin(admin.ModelAdmin):
    """Admin interface for Profit History"""
    list_display = ('user', 'investment', 'amount', 'description', 'date')
    list_filter = ('date',)
    search_fields = ('user__username', 'user__email', 'investment__plan__name')
    readonly_fields = ('date',)

    def has_add_permission(self, request):
        return True  # Allow adding profit manually


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Admin interface for Payment Methods"""
    list_display = ('name', 'type', 'min_amount', 'max_amount', 'charge_type', 'charge_amount', 'is_active', 'order')
    list_filter = ('type', 'is_active', 'charge_type')
    search_fields = ('name', 'wallet_address')
    list_editable = ('is_active', 'order')
    ordering = ('order', 'name')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type', 'icon', 'order')
        }),
        ('Limits', {
            'fields': ('min_amount', 'max_amount')
        }),
        ('Charges', {
            'fields': ('charge_type', 'charge_amount')
        }),
        ('Processing', {
            'fields': ('duration',)
        }),
        ('Crypto Details', {
            'fields': ('wallet_address', 'qr_code'),
            'description': 'For cryptocurrency payment methods'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
