# Quick Start - Seed Test Data

## TL;DR - 3 Commands to Test Everything

```bash
# 1. Seed payment methods and investment plans
python manage.py seed_data

# 2. Seed test data for your user (replace 'admin' with your username)
python manage.py seed_user_data admin

# 3. Start server and test
python manage.py runserver
```

Then visit:
- **Deposits**: http://127.0.0.1:8000/dashboard/deposits/
- **Account History**: http://127.0.0.1:8000/dashboard/account-history/
- **Profit History**: http://127.0.0.1:8000/dashboard/profit-history/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## What Gets Created

### From `seed_data`:
- 4 Payment Methods (USDT, Bitcoin, Ethereum, Litecoin)
- 5 Investment Plans (Starter → VIP)

### From `seed_user_data <username>`:
- 4 Deposits ($4,750 total)
  - 3 Approved: $1,000 + $2,500 + $500
  - 1 Pending: $750
- 3 Withdrawals ($650 total)
  - 2 Approved: $300 + $150
  - 1 Pending: $200
- 3 Investments
  - 1 Completed (STARTER, 7 days profit)
  - 2 Active (STANDARD + STARTER)
- 19 Profit Records ($2,500+ total)

**Your Balance**: ~$3,850

## Quick Tests

### ✅ Test Deposit
```
1. Go to: /dashboard/deposits/
2. Select USDT (not Solana!)
3. Enter $100
4. Click Proceed
5. Upload proof image
6. Admin → Approve deposit
7. Balance increases ✓
```

### ✅ Test Payment Page
```
1. After creating deposit, you'll see:
   - Network Type: USDT Network ✓ (not Solana)
   - Wallet Address: (from database) ✓
```

### ✅ Test Account History
```
1. Go to: /dashboard/account-history/
2. Should see all 7+ transactions ✓
```

### ✅ Test Profit History
```
1. Go to: /dashboard/profit-history/
2. Should see 19+ profit entries ✓
3. Daily amounts: $25, $150, $15
```

## Fixed Issues

1. ✅ Payment page now shows selected method (not hardcoded Solana)
2. ✅ Wallet address comes from database
3. ✅ Account history shows all transactions
4. ✅ Profit history displays profit records
5. ✅ Withdrawal links stay on your site (no external redirects)

## If Something Doesn't Work

See **TESTING_GUIDE.md** for detailed troubleshooting.
