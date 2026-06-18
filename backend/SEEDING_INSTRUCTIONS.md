# Database Seeding Instructions

## How to Seed Your Database with Dummy Data

### Step 1: Navigate to Backend Directory
```bash
cd /mnt/c/Users/DELL/Desktop/work/client_work/dynamicsdigitalasset/backend
```

### Step 2: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
source venv/bin/activate
```

### Step 3: Run Migrations (if not already done)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Seed the Database
```bash
python manage.py seed_data
```

This command will create:

## ✅ What Gets Created:

### 1. **Payment Methods** (4 methods)
- **USDT** - TRC20 Network ($10 - $100,000)
- **Bitcoin** - BTC Network ($10 - $100,000)
- **Ethereum** - ERC20 Network ($10 - $100,000)
- **Litecoin** - LTC Network ($10 - $100,000)

All with 0% fees and dummy wallet addresses.

### 2. **Investment Plans** (5 plans)
- **STARTER PLAN**: $100-$999, 5% daily, 7 days (35% total return)
- **STANDARD PLAN**: $1,000-$4,999, 7.5% daily, 14 days (105% total return)
- **PROFESSIONAL PLAN**: $5,000-$14,999, 10% daily, 21 days (210% total return)
- **RETIREMENT PLAN**: $15,000-$49,999, 15% daily, 30 days (450% total return)
- **VIP PLAN**: $50,000-$1,000,000, 20% daily, 30 days (600% total return)

## 📝 Next Steps:

1. **Update Wallet Addresses**: Go to `/admin/investments/paymentmethod/` and update with your real wallet addresses

2. **Adjust Investment Plans**: Go to `/admin/investments/investmentplan/` to modify profit percentages, durations, or amounts

3. **Create Superuser** (if you haven't already):
   ```bash
   python manage.py createsuperuser
   ```

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

5. **Test the Deposit Flow**:
   - Go to http://localhost:8000/dashboard/deposits/
   - Select a payment method (USDT, Bitcoin, or Ethereum)
   - Enter an amount or click a preset amount
   - Click "Proceed" - it should now work!

## 🔄 Re-seeding

The seeding command is **idempotent** - it won't create duplicates if you run it multiple times. It will skip items that already exist.

If you want to start fresh:
```bash
# Delete database (SQLite only - be careful!)
rm db.sqlite3

# Re-create database
python manage.py migrate

# Re-seed
python manage.py seed_data

# Re-create superuser
python manage.py createsuperuser
```

## 🛠️ Customizing Wallet Addresses

After seeding, you **MUST** update the wallet addresses in the admin panel:

1. Go to: http://localhost:8000/admin/investments/paymentmethod/
2. Click on each payment method
3. Update the "Wallet address" field with your actual crypto wallet addresses
4. Save

**Important**: The dummy addresses in the seed data are just placeholders!
