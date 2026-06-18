import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from transactions.models import Transfer

transfers = Transfer.objects.all()
print(f"Total transfers: {transfers.count()}")

for t in transfers:
    print(f"Transfer #{t.id}: {t.sender.username} -> {t.recipient.username} ${t.amount} [{t.status}]")
