from django.contrib import admin
from .models import TransactionLog, Bank, UUID

admin.site.register(TransactionLog)
admin.site.register(Bank)
admin.site.register(UUID)
