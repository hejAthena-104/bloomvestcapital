from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationToken, PasswordResetToken, LoginHistory, Notification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model"""

    # Fields to display in the user list
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'balance',
        'total_profit',
        'referral_code',
        'is_verified',
        'is_staff',
        'is_active',
        'created_at'
    )

    # Fields to filter by
    list_filter = (
        'is_staff',
        'is_active',
        'is_verified',
        'created_at',
        'date_joined'
    )

    # Fields to search
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
        'referral_code'
    )

    # Read-only fields
    readonly_fields = (
        'referral_code',
        'created_at',
        'updated_at',
        'date_joined',
        'last_login'
    )

    # Fieldsets for the user detail page
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Financial Information', {
            'fields': (
                'balance',
                'total_profit',
                'total_bonus',
                'referral_bonus'
            )
        }),
        ('Referral Information', {
            'fields': ('referral_code', 'referred_by')
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_verified',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')
        }),
    )

    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'phone',
                'is_staff',
                'is_active'
            ),
        }),
    )

    # Order by newest first
    ordering = ('-created_at',)


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    """Admin interface for Email Verification Tokens"""
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')
    ordering = ('-created_at',)


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin interface for Password Reset Tokens"""
    list_display = ('user', 'token', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at', 'expires_at')
    ordering = ('-created_at',)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    """Admin interface for Login History"""
    list_display = ('user', 'ip_address', 'login_time', 'success')
    list_filter = ('success', 'login_time')
    search_fields = ('user__username', 'user__email', 'ip_address')
    readonly_fields = ('user', 'ip_address', 'user_agent', 'location', 'login_time', 'success')
    ordering = ('-login_time',)

    def has_add_permission(self, request):
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notifications"""
    list_display = ('user', 'title', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} notification(s) marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f"{queryset.count()} notification(s) marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"
