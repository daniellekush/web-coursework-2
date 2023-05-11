from django.test import TestCase
from .models import TransactionLog, Bank, UUID
from django.test.client import RequestFactory
from .views import InitiateTransactionDebit, InitiateAuthDebit
import json

# Create your tests here.

class AppTests(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.factory = RequestFactory()

    # Error 104
    def test_transaction_get(self):
        request = self.factory.get('/initiatetransactiondebit/')
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 104)

    def test_auth_get(self):
        request = self.factory.get('/initiateauthdebit/')
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 104)
        
    # Error 100
    def test_transaction_empty_post(self):
        data = {}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 100)

    def test_auth_empty_post(self):
        data = {}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 100)

    # Error 101
    def test_transaction_empty_issue(self):
        data = {"acqBankAccID": 123, "amount": 2, "currencyCode": 826, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_transaction_empty_acq(self):
        data = {"issueBankAccID": 123, "amount": 2, "currencyCode": 826, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_transaction_empty_amount(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "currencyCode": 826, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_transaction_empty_code(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 2, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)

    def test_transaction_empty_uuid(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 2, "currencyCode": 826}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_auth_empty_issue(self):
        data = {"acqBankAccID": 123, "amount": 2, "currencyCode": 826}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_auth_empty_acq(self):
        data = {"issueBankAccID": 123, "amount": 2, "currencyCode": 826}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_auth_empty_amount(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "currencyCode": 826}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    def test_auth_empty_code(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 2}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 101)
        
    # Error 102
    def test_transaction_zero_amount(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 0, "currencyCode": 826, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 102)
    
    def test_auth_zero_amount(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 0, "currencyCode": 826}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 102)
        
    # Error 404
    def test_transaction_bad_uuid(self):
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 20, "currencyCode": 826, "AuthUUID": "ff5sac19-ffa0-4673-1854-41436f94391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 404)
        
    # Good
    def test_transaction_good(self):
        bank = Bank(accountNumber=321, sortCode="33-22-11", nameOnAccount="test")
        bank.save()
        bank = Bank(accountNumber=123, sortCode="11-22-33", nameOnAccount="test2")
        bank.save()
        uuid = UUID(unique_ID="ff56ac19-ffa0-4673-8854-41436094391b")
        uuid.save()
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 20, "currencyCode": 826, "AuthUUID": "ff56ac19-ffa0-4673-8854-41436094391b"}
        request = self.factory.post('/initiatetransactiondebit/', data)
        response = InitiateTransactionDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 200)
        
    def test_auth_good(self):
        bank = Bank(accountNumber=321, sortCode="33-22-11", nameOnAccount="test")
        bank.save()
        bank = Bank(accountNumber=123, sortCode="11-22-33", nameOnAccount="test2")
        bank.save()
        data = {"issueBankAccID": 321, "acqBankAccID": 123, "amount": 20, "currencyCode": 826}
        request = self.factory.post('/initiateauthdebit/', data)
        response = InitiateAuthDebit(request)
        status_code = json.loads(response.content)['StatusCode']
        self.assertEqual(status_code, 200)
