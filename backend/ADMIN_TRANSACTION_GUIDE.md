# Admin Transaction Management Guide

## How to Approve/Reject Deposits from the Admin Panel

### Quick Method (Recommended)

1. **Go to the Admin Panel**
   - Navigate to: http://localhost:8000/admin/
   - Login with your superuser credentials

2. **Open Deposits**
   - Click on **Transactions → Deposits**
   - You'll see a list of all deposits with:
     - Username
     - Amount
     - Status (color-coded)
     - Payment Method
     - Proof Uploaded (✓ Yes / ✗ No)
     - Created date

3. **View Payment Proof**
   - Click on any deposit to view details
   - You'll see the **Payment Proof Preview** showing the uploaded image
   - Verify if the payment is legitimate

4. **Approve or Reject**

   **Method A - Using Bulk Actions:**
   - Select deposits using checkboxes
   - From the "Action" dropdown, select:
     - **"Approve selected deposits"** - To approve
     - **"Reject selected deposits"** - To reject
   - Click **"Go"**

   **Method B - From Transaction Detail:**
   - Go to **Transactions → Transactions**
   - Select pending transactions
   - Use actions: **"Approve selected transactions"** or **"Reject selected transactions"**

### What Happens When You Approve a Deposit?

When you approve a deposit, the system automatically:

1. ✅ Updates transaction status to `approved`
2. ✅ Adds the deposit amount to the user's balance
3. ✅ Sets the `processed_at` timestamp
4. ✅ Creates a notification for the user (if implemented)

**Example:**
- User deposits $500
- You approve it
- User's balance increases by $500
- Transaction marked as approved

### What Happens When You Reject a Deposit?

When you reject a deposit:

1. ❌ Updates transaction status to `rejected`
2. ❌ **Does NOT** add money to user's balance
3. ❌ Sets the `processed_at` timestamp
4. ❌ Adds admin note explaining rejection

## Managing Withdrawals

### Withdrawal Approval Process

1. **Go to Withdrawals**
   - Admin → **Transactions → Withdrawals**

2. **Review Details**
   - Check user's account balance
   - Verify withdrawal address
   - Check withdrawal amount

3. **Approve or Reject**
   - Select withdrawals
   - Action: **"Approve selected transactions"** or **"Reject selected transactions"**

### What Happens When You Approve a Withdrawal?

1. ✅ Updates status to `approved`
2. ✅ **Deducts** the amount from user's balance
3. ✅ You must manually send crypto to the withdrawal address
4. ✅ User gets notified

**Important:** The system deducts the balance but doesn't send crypto automatically. You must:
- Copy the withdrawal address from the admin panel
- Send the crypto from your wallet
- Keep records of transaction hashes

### What Happens When You Reject a Withdrawal?

1. ❌ Updates status to `rejected`
2. ❌ **Does NOT** deduct from user's balance
3. ❌ User can request withdrawal again

## Status Color Coding

When viewing transactions, statuses are color-coded:

- 🟠 **PENDING** (Orange) - Waiting for admin approval
- 🔵 **PROCESSING** (Blue) - Being processed
- 🟢 **APPROVED** (Green) - Approved and completed
- 🔴 **REJECTED** (Red) - Rejected by admin
- ⚫ **CANCELLED** (Gray) - Cancelled by user or system

## Direct Links to Admin Sections

After starting the server (`python manage.py runserver`):

- **All Transactions**: http://localhost:8000/admin/transactions/transaction/
- **Deposits Only**: http://localhost:8000/admin/transactions/deposit/
- **Withdrawals Only**: http://localhost:8000/admin/transactions/withdrawal/
- **Transfers**: http://localhost:8000/admin/transactions/transfer/
- **Payment Methods**: http://localhost:8000/admin/investments/paymentmethod/
- **Investment Plans**: http://localhost:8000/admin/investments/investmentplan/
- **Users**: http://localhost:8000/admin/accounts/user/

## Common Admin Tasks

### 1. Approve Multiple Deposits at Once

```
1. Go to: Admin → Transactions → Deposits
2. Filter by Status: "pending"
3. Select all deposits you want to approve (use checkboxes)
4. Action dropdown: "Approve selected deposits"
5. Click "Go"
```

### 2. Find Pending Transactions

```
1. Go to: Admin → Transactions → Transactions
2. Filter sidebar: Status = "pending"
3. Filter sidebar: Type = "deposit" or "withdrawal"
```

### 3. Search for a Specific User's Transactions

```
1. Go to: Admin → Transactions → Transactions
2. Use search box: Enter username or email
3. All transactions for that user will appear
```

### 4. View User's Current Balance

```
1. Go to: Admin → Accounts → Users
2. Search for the user
3. Click on username
4. See "Balance" field
```

### 5. Manually Adjust User Balance

```
1. Go to: Admin → Accounts → Users
2. Find and click the user
3. Edit the "Balance" field directly
4. Click "Save"
```

**Warning:** Only do this for corrections. Normal deposits/withdrawals should use the transaction system.

### 6. Add Admin Notes to Transactions

```
1. Open any transaction
2. Scroll to "Additional Information" section
3. Add your note in "Admin note" field
4. Save
```

This note is only visible to admins, not users.

## Troubleshooting

### ❓ Deposit approved but balance didn't update?

**Check:**
1. Transaction status is actually "approved" (not just "processing")
2. Look at the transaction detail - check `processed_at` field
3. Verify user's balance in Users section
4. Check if the approve() method was called (or if status was just changed manually)

**Fix:** If balance wasn't updated, you can:
- Change status back to "pending"
- Use the "Approve selected transactions" action again
- OR manually adjust user balance in Users section

### ❓ User says they deposited but I don't see it?

**Check:**
1. Transactions → Deposits - filter by username
2. Check if proof image was uploaded
3. Verify payment method matches what they claim

### ❓ Cannot approve transaction - error appears?

**Possible causes:**
1. Transaction already approved/rejected
2. Database connection issue
3. User account issue

**Fix:** Check transaction status first. If stuck, change status to "pending" and try again.

## Best Practices

✅ **DO:**
- Always verify payment proof before approving deposits
- Check user's balance before approving withdrawals
- Add admin notes for rejected transactions
- Filter by "pending" status daily to process new requests
- Keep records of crypto transaction hashes for withdrawals

❌ **DON'T:**
- Don't manually change status without using approve/reject actions
- Don't approve deposits without payment proof
- Don't approve withdrawals if user balance is insufficient
- Don't delete transactions (archive them instead)

## Security Notes

🔒 **Important:**
- Only admin/superuser accounts can access /admin/
- All transaction approvals are logged with timestamps
- User balances are updated atomically (no race conditions)
- Withdrawals require OTP verification from users
- Payment proofs are stored securely in media/deposit_proofs/

## Need Help?

If you encounter issues:
1. Check Django logs for error messages
2. Verify database migrations are up to date: `python manage.py migrate`
3. Ensure you're logged in as superuser
4. Check user permissions if using staff accounts
