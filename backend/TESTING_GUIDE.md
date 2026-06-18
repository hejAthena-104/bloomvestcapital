# Complete End-to-End Testing Guide

## Step 1: Seed Payment Methods and Investment Plans

First, create the base data (payment methods and investment plans):

```bash
python manage.py seed_data
```

**Expected Output:**
```
🌱 Starting database seeding...

Creating payment methods...
  ✓ Created payment method: USDT
  ✓ Created payment method: Bitcoin
  ✓ Created payment method: Ethereum
  ✓ Created payment method: Litecoin

✓ Payment methods: 4 created

Creating investment plans...
  ✓ Created plan: STARTER PLAN ($100-$999, 5% daily, 7 days)
  ✓ Created plan: STANDARD PLAN ($1,000-$4,999, 7.5% daily, 14 days)
  ✓ Created plan: PROFESSIONAL PLAN ($5,000-$14,999, 10% daily, 21 days)
  ✓ Created plan: RETIREMENT PLAN ($15,000-$49,999, 15% daily, 30 days)
  ✓ Created plan: VIP PLAN ($50,000-$1,000,000, 20% daily, 30 days)

✓ Investment plans: 5 created

✅ Database seeding completed successfully!
```

## Step 2: Seed Test Data for Your Admin User

Replace `yourusername` with your actual admin username:

```bash
python manage.py seed_user_data yourusername
```

**If you don't know your username**, first list users:
```bash
python manage.py shell -c "from accounts.models import User; [print(f'{u.username} - {u.email}') for u in User.objects.all()]"
```

**Expected Output:**
```
🌱 Seeding test data for user: yourusername

Creating test deposits...
  ✓ Created deposit: $1000.00 (USDT) - approved
  ✓ Created deposit: $2500.00 (Bitcoin) - approved
  ✓ Created deposit: $500.00 (USDT) - approved
  ✓ Created deposit: $750.00 (Bitcoin) - pending
✓ 4 deposits created

Creating test withdrawals...
  ✓ Created withdrawal: $300.00 (Bitcoin) - approved
  ✓ Created withdrawal: $150.00 (USDT) - approved
  ✓ Created withdrawal: $200.00 (Bitcoin) - pending
✓ 3 withdrawals created

Creating test investments...
  ✓ Created investment: $500.00 (STARTER PLAN) - completed
    → Generated 7 days of profit ($25.00/day)
  ✓ Created investment: $2000.00 (STANDARD PLAN) - active
    → Generated 15 days of profit ($150.00/day)
  ✓ Created investment: $300.00 (STARTER PLAN) - active
    → Generated 5 days of profit ($15.00/day)
✓ 3 investments created
✓ 19 profit records created

Calculating user balance...
  Approved deposits: $4000.00
  Approved withdrawals: $450.00
  Active investments: $2300.00
  Total profit: $2600.00
  Final balance: $3850.00

✅ Test data seeding completed for yourusername!
User balance: $3850.00
Total profit: $2600.00
```

## Step 3: Verify Everything Works

### 3.1 Test Deposit Flow

1. **Go to Deposits Page:**
   ```
   http://127.0.0.1:8000/dashboard/deposits/
   ```

2. **Verify:**
   - ✅ You see USDT, Bitcoin, Ethereum, Litecoin cards (not Solana)
   - ✅ Payment methods come from database
   - ✅ Your deposit history shows at the bottom

3. **Create a New Deposit:**
   - Select a payment method (e.g., USDT)
   - Enter amount: `100`
   - Click "Proceed"

4. **On Payment Page:**
   ```
   http://127.0.0.1:8000/dashboard/payment/X/
   ```
   - ✅ Network Type shows "USDT Network" (not Solana)
   - ✅ Wallet address matches the USDT address from database
   - ✅ Upload a screenshot/image as payment proof
   - ✅ Click "Mark as Completed"

5. **Approve in Admin:**
   ```
   http://127.0.0.1:8000/admin/transactions/deposit/
   ```
   - ✅ See your deposit in the list
   - ✅ Click it, view the uploaded proof image
   - ✅ Select it, Action → "Approve selected deposits" → Go
   - ✅ Check user balance increased by $100

### 3.2 Test Account History

1. **Go to Account History:**
   ```
   http://127.0.0.1:8000/dashboard/account-history/
   ```

2. **Verify You See:**
   - ✅ All deposits (4 seeded + 1 new = 5 total)
   - ✅ All withdrawals (3 seeded)
   - ✅ Transaction types, amounts, statuses
   - ✅ Dates are correct

**If you see nothing:**
- Check URL is exactly: `/dashboard/account-history/` (with hyphen)
- Check browser console for errors
- Verify you're logged in as the correct user

### 3.3 Test Profit History

1. **Go to Profit History:**
   ```
   http://127.0.0.1:8000/dashboard/profit-history/
   ```

2. **Verify You See:**
   - ✅ 19 profit entries (from seeded investments)
   - ✅ Daily profit amounts ($25, $150, $15)
   - ✅ Investment plan names
   - ✅ Dates spanning last 25 days

**Expected Profit Breakdown:**
- STARTER PLAN (completed): 7 days × $25/day = $175
- STANDARD PLAN (active): 15 days × $150/day = $2,250
- STARTER PLAN (active): 5 days × $15/day = $75
- **Total: $2,500 in profits**

### 3.4 Test Withdrawal Flow

1. **Go to Withdrawals:**
   ```
   http://127.0.0.1:8000/dashboard/withdrawals/
   ```

2. **Verify:**
   - ✅ Shows your withdrawal history (3 pending/approved)
   - ✅ Select payment method (USDT/Bitcoin)
   - ✅ Does NOT redirect to external site
   - ✅ Stays on your domain

3. **Request OTP:**
   - Click "Request OTP"
   - Check terminal/console for OTP (if email not configured)
   - ✅ OTP is generated

4. **Submit Withdrawal:**
   - Enter amount: `50`
   - Enter the OTP code
   - Submit
   - ✅ Withdrawal created with status "pending"

5. **Approve in Admin:**
   ```
   http://127.0.0.1:8000/admin/transactions/withdrawal/
   ```
   - Select the withdrawal
   - Action → "Approve selected transactions" → Go
   - ✅ User balance decreased by $50

### 3.5 Test Investment Flow

1. **Go to Buy Plan:**
   ```
   http://127.0.0.1:8000/dashboard/buy-plan/
   ```

2. **Verify:**
   - ✅ You see 5 investment plans (Starter, Standard, Professional, Retirement, VIP)
   - ✅ Plans show correct percentages and durations
   - ✅ Select a plan

3. **Purchase Investment:**
   - Select "STARTER PLAN"
   - Enter amount: `200`
   - Click "Confirm & Invest"
   - ✅ Investment created
   - ✅ Balance decreased by $200

4. **View My Plans:**
   ```
   http://127.0.0.1:8000/dashboard/my-plans/
   ```
   - ✅ See active investments (3 seeded + 1 new = 4)
   - ✅ See completed investment (1)
   - ✅ Progress bars show correctly
   - ✅ Expected profit calculated

## Step 4: Admin Panel Verification

### 4.1 Check All Transactions

```
http://127.0.0.1:8000/admin/transactions/transaction/
```

**Verify:**
- ✅ Color-coded status badges (Orange, Green, Red)
- ✅ Can filter by Type, Status, Payment Method
- ✅ Can search by username
- ✅ Bulk actions work (Approve/Reject)

### 4.2 Check Deposits

```
http://127.0.0.1:8000/admin/transactions/deposit/
```

**Verify:**
- ✅ Shows "Proof Uploaded" column (✓ Yes / ✗ No)
- ✅ Click deposit to see full payment proof image
- ✅ Can approve/reject from here

### 4.3 Check Investments

```
http://127.0.0.1:8000/admin/investments/investment/
```

**Verify:**
- ✅ Shows all investments (active and completed)
- ✅ Can filter by status, plan, user
- ✅ Progress and profit calculated correctly

### 4.4 Check Profit History

```
http://127.0.0.1:8000/admin/investments/profithistory/
```

**Verify:**
- ✅ 19+ profit records exist
- ✅ Daily profits recorded correctly
- ✅ Linked to correct investments

## Step 5: Balance Verification

### Check User Balance Calculation

Your final balance should be:

```
Approved Deposits: $4,000 (+ any new deposits you made)
- Approved Withdrawals: $450 (+ any you made)
- Active Investments: $2,300 (+ any you made)
+ Total Profits: $2,500
= Expected Balance: ~$3,750
```

**Verify in Admin:**
```
http://127.0.0.1:8000/admin/accounts/user/
```
- Find your user
- Check "Balance" field matches calculation

## Troubleshooting

### Issue: Account History shows nothing

**Solution:**
1. Check you're accessing: `/dashboard/account-history/` (with hyphen)
2. Run in terminal:
   ```bash
   python manage.py shell
   ```
   ```python
   from accounts.models import User
   from transactions.models import Transaction
   user = User.objects.get(username='yourusername')
   print(Transaction.objects.filter(user=user).count())
   # Should show 7+
   ```

### Issue: Profit History shows nothing

**Solution:**
1. Run in terminal:
   ```bash
   python manage.py shell
   ```
   ```python
   from accounts.models import User
   from investments.models import ProfitHistory
   user = User.objects.get(username='yourusername')
   print(ProfitHistory.objects.filter(user=user).count())
   # Should show 19+
   ```

### Issue: Payment page still shows "Solana"

**Solution:**
1. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Restart Django server

### Issue: Wallet address not showing

**Solution:**
1. Check payment method has wallet_address:
   ```
   http://127.0.0.1:8000/admin/investments/paymentmethod/
   ```
2. Click USDT, ensure "Wallet address" field is filled
3. If empty, add your wallet address and save

## Summary Checklist

After following this guide, you should have:

- ✅ 4 Payment methods (USDT, Bitcoin, Ethereum, Litecoin)
- ✅ 5 Investment plans (Starter through VIP)
- ✅ 4+ Deposits (3 approved, 1 pending, + any new)
- ✅ 3+ Withdrawals (2 approved, 1 pending, + any new)
- ✅ 3+ Investments (1 completed, 2 active, + any new)
- ✅ 19+ Profit history records
- ✅ User balance correctly calculated
- ✅ Payment page shows correct network (not Solana)
- ✅ All pages show data correctly
- ✅ No external links redirect outside

If all checkboxes are ✅, your system is working end-to-end!
