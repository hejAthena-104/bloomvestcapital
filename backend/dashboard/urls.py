from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard_index, name='index'),

    # Investments
    path('my-plans/', views.my_plans, name='my_plans'),
    path('myplans/All/', views.my_plans, name='my_plans_all'),  # Alternative URL
    path('buy-plan/', views.buy_plan, name='buy_plan'),

    # Deposits
    path('deposits/', views.deposits, name='deposits'),
    path('newdeposit/', views.new_deposit, name='new_deposit'),
    path('payment/<int:transaction_id>/', views.payment, name='payment'),

    # Withdrawals
    path('withdrawals/', views.withdrawals, name='withdrawals'),
    path('enter-amount/', views.select_withdrawal_method, name='select_withdrawal_method'),
    path('withdraw-funds/', views.withdraw_funds, name='withdraw_funds'),
    path('getotp/', views.request_otp, name='request_otp'),

    # History
    path('profit-history/', views.profit_history, name='profit_history'),
    path('account-history/', views.account_history, name='account_history'),
    path('accounthistory/', views.account_history, name='accounthistory'),  # Alternative URL
    path('withdrawal-history/', views.withdrawal_history, name='withdrawal_history'),
    path('other-history/', views.other_history, name='other_history'),

    # Referrals
    path('refer/', views.refer_user, name='refer_user'),
    path('referuser/', views.refer_user, name='referuser'),  # Alternative URL

    # Settings
    path('account-settings/', views.account_settings, name='account_settings'),
    path('manage-account-security/', views.manage_account_security, name='manage_account_security'),

    # Support
    path('support/', views.support, name='support'),

    # Transfer
    path('transfer-funds/', views.transfer_funds, name='transfer_funds'),

    # Admin Email Management
    path('send-email/', views.send_email, name='send_email'),
]
