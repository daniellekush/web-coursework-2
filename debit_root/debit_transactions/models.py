from django.db import models

class UUID(models.Model):
    unique_ID = models.TextField('UUID', blank=True, unique=True)

class TransactionLog(models.Model):
    issueBankAccID = models.TextField('IssueBankAccID', blank=True)
    acqBankAccID = models.TextField('AcqBankAccID', blank=True)
    amount = models.FloatField()
    currencyCode = models.PositiveIntegerField()
    UUID = models.ForeignKey(UUID, on_delete=models.CASCADE)
    
class Bank(models.Model):
    accountNumber = models.IntegerField(unique=True)
    sortCode = models.TextField('SortCode', blank=True)
    nameOnAccount = models.TextField('Name on Account', blank=True)

