# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Bloomvest Capital** - Investment platform with static frontend and Django backend.

- **Frontend**: Static HTML/CSS/JS landing pages deployed to Netlify
- **Backend**: Django 4.2.7 application deployed to Railway/Render
- **Database**: SQLite (dev), PostgreSQL (production)

## Development Commands

```bash
# Setup (from backend directory)
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver  # http://localhost:8000

# Testing
python manage.py test                    # All tests
python manage.py test accounts           # Single app
python manage.py test accounts.tests.TestUserModel  # Single test class

# Database
python manage.py makemigrations && python manage.py migrate
python manage.py shell_plus              # Enhanced shell (django-extensions)

# Seed test data (see QUICKSTART.md for details)
python manage.py seed_data               # Create payment methods & investment plans
python manage.py seed_user_data <username>  # Create test transactions for user
```

## Architecture

### Django Apps Structure

The backend is organized into 5 Django apps with clear separation of concerns:

1. **accounts** - User authentication and profile management
   - Custom User model extending AbstractUser
   - Email/username authentication via custom backend
   - Email verification tokens (24-hour expiry)
   - Password reset tokens (1-hour expiry)
   - Login history tracking
   - User notifications system

2. **investments** - Investment plans and user investments
   - InvestmentPlan: Define investment products with min/max amounts, daily profit %, duration
   - Investment: Track user investments with status (active/completed/cancelled)
   - ProfitHistory: Record daily profit payments
   - PaymentMethod: Configure deposit/withdrawal methods with fees

3. **transactions** - Financial transactions
   - Transaction: Unified model for deposits, withdrawals, transfers, bonuses, profits
   - Deposit: Extended details with proof of payment
   - Withdrawal: Extended details with withdrawal addresses
   - Transfer: Internal fund transfers between users

4. **support** - Customer support system
   - SupportTicket: Auto-generated ticket numbers (TKT-XXXXXXXX)
   - Status workflow: open → in_progress → waiting_reply → resolved → closed
   - Priority levels and categorization

5. **dashboard** - User dashboard views and business logic

### Custom User Model

Located in `accounts/models.py`:

```python
AUTH_USER_MODEL = 'accounts.User'
```

**Key fields:**
- Financial: `balance`, `total_profit`, `total_bonus`, `referral_bonus`
- Referral: `referral_code` (auto-generated 8-char), `referred_by` (self-referential FK)
- Verification: `is_verified` (email verification status)
- Banking: `bank_name`, `account_name`, `account_number`, `swift_code`
- Crypto: `btc_address`, `eth_address`, `ltc_address`, `usdt_address`
- Preferences: `email_on_withdrawal`, `email_on_roi`, `email_on_expiration`

**Properties:**
- `total_deposited`: Sum of approved deposits
- `total_withdrawn`: Sum of approved withdrawals
- `referral_count`: Number of referred users

### Authentication Backend

Custom authentication allows login with either username or email:

```python
# accounts/views.py:281
class EmailOrUsernameModelBackend
```

Configured in `config/settings.py:151`:
```python
AUTHENTICATION_BACKENDS = [
    'accounts.views.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

### Key Model Methods

**Transaction approval (`transactions/models.py:67`):**
```python
transaction.approve()  # Updates user balance, sets status to approved
transaction.reject(reason='...')  # Rejects with admin note
```

**Investment lifecycle:**
```python
investment.days_remaining  # Calculate days until completion
investment.progress_percentage  # Calculate % complete
investment.expected_daily_profit  # Daily profit amount
investment.is_active()  # Check if still active
```

**Transfer operations (`transactions/models.py:172`):**
```python
transfer.complete()  # Deduct from sender, credit recipient
transfer.cancel()  # Cancel pending transfer
```

### URL Structure

```
/admin/                    - Django admin panel
/auth/login/              - Login page
/auth/register/           - Registration page
/auth/logout/             - Logout
/auth/forgot-password/    - Password reset request
/dashboard/               - User dashboard (requires authentication)
```

### Settings Configuration

**Key settings (`config/settings.py`):**
- `AUTH_USER_MODEL = 'accounts.User'` (line 148)
- `LOGIN_URL = '/auth/login/'` (line 157)
- `LOGIN_REDIRECT_URL = '/dashboard/'` (line 158)
- `FRONTEND_URL` from environment for CORS/redirects (line 162)
- WhiteNoise for static file serving in production (line 140)
- Logging configured for console output (line 165)

### Template Organization

```
backend/templates/
├── auth/
│   ├── login.html
│   ├── register.html
│   └── forgot-password.html
└── dashboard/
    ├── index.html
    ├── deposits.html
    ├── withdrawals.html
    ├── buy-plan.html
    ├── account-settings.html
    └── [11 more dashboard pages]
```

### Static Files

- **Development**: Files served from `backend/static/`
- **Production**: Collected to `staticfiles/` via `python manage.py collectstatic`
- **Theme**: Dashly admin theme in `static/themes/dashly/`

## Important Implementation Details

### Referral System
- Referral codes auto-generate on user creation (8 alphanumeric characters)
- Set via `referred_by` ForeignKey on User model
- Referral bonuses tracked in `User.referral_bonus` field

### Token-Based Verification
- Email verification: 24-hour validity (`accounts/models.py:165`)
- Password reset: 1-hour validity (`accounts/models.py:197`)
- Both use UUID tokens with `is_valid()` and `mark_as_used()` methods

### Transaction Status Flow
```
Deposit/Withdrawal: pending → processing → approved/rejected
Investment: active → completed/cancelled
Transfer: pending → completed/failed/cancelled
```

### Investment Profit Calculation
- Daily profit: `(amount * plan.daily_profit_percentage) / 100`
- Total return: `(amount * plan.total_return_percentage) / 100`
- End date auto-calculated on Investment creation based on `plan.duration_days`

### Payment Method Fees
```python
payment_method.calculate_charge(amount)  # Returns fee amount
payment_method.get_total_amount(base_amount)  # Base + fee
```

## Deployment

### Environment Variables

Required in production:
```bash
SECRET_KEY=<generate-secure-key>
DEBUG=False
ALLOWED_HOSTS=.railway.app,.render.com,yourdomain.com
DATABASE_URL=postgresql://...  # Auto-provided by Railway/Render
FRONTEND_URL=https://your-frontend.netlify.app
```

### Deployment Commands

```bash
# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Start with gunicorn (production)
gunicorn config.wsgi --log-file -
```

### Database Migration Path

Development → Production:
1. Test migrations locally with SQLite
2. Apply to production PostgreSQL via `python manage.py migrate`
3. Always backup production database before migrations

## Code Patterns

### View Decorators
Use `@login_required` for authenticated views:
```python
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    # View logic
```

### Message Framework
Use Django messages for user feedback:
```python
from django.contrib import messages

messages.success(request, 'Action completed successfully!')
messages.error(request, 'Something went wrong.')
messages.warning(request, 'Please be careful.')
messages.info(request, 'FYI: Something happened.')
```

### Model Property Usage
Properties are computed, not stored in database:
```python
user.total_deposited  # Property - computed from transactions
user.balance  # Field - stored in database
```

### Related Name Conventions
- Always use descriptive `related_name` on ForeignKey fields
- Example: `referred_by` has `related_name='referrals'`
- Access via: `user.referrals.all()` gets all users they referred

## Related Documentation

- **QUICKSTART.md** - Fast setup with 3 commands to seed test data
- **TESTING_GUIDE.md** - Complete end-to-end testing walkthrough
- **SEEDING_INSTRUCTIONS.md** - Database seeding details

## Email Service

Email functionality via `accounts/email_utils.py` using Resend service. Configure via environment variables (see `.env.example`).
