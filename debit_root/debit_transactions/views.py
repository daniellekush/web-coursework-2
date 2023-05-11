from django.shortcuts import render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError
from .models import TransactionLog, Bank, UUID
import uuid

def InitiateTransactionDebit(request):
    random_id = uuid.uuid4()
    if request.method == 'POST':
        # Error 100
        if len(request.POST) == 0:
            return JsonResponse({"StatusCode":100, "UUID": random_id, "Comment": "Request body empty."})
        # Error 101
        try:
            issueBankAccID = request.POST["issueBankAccID"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find issueBankAccID field."})
        try:
            acqBankAccID = request.POST["acqBankAccID"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find acqBankAccID field."})
        try:
            amount = request.POST["amount"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find amount field."})
        try:
            currencyCode = request.POST["currencyCode"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find currencyCode field."})
        try:
            request_uuid = request.POST["AuthUUID"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find currencyCode field."})
        # Error 102
        if request.POST["amount"] == '0':
            return JsonResponse({"StatusCode":102, "UUID": random_id, "Comment": "Transaction amount had amount 0."})
        # Error 401
        try:
            unique_id = UUID(unique_ID=random_id)
            record = TransactionLog(issueBankAccID=int(request.POST["issueBankAccID"]), 		  acqBankAccID=int(request.POST["acqBankAccID"]), amount=float(request.POST["amount"]), currencyCode=int(request.POST["currencyCode"]), UUID=unique_id)
        except (ObjectDoesNotExist, FieldDoesNotExist):
            return JsonResponse({"StatusCode":401, "UUID": random_id, "Comment": "Could not access database."})
        
        # Do application stuff here
        try:
            test_id = UUID.objects.filter(unique_ID=request.POST["AuthUUID"])

            # Error 404
            if len(test_id) == 0:
                return JsonResponse({"StatusCode":404, "UUID": random_id, "Comment": "Transaction could not be authorised."})
            unique_id = UUID.objects.filter(unique_ID=request.POST["AuthUUID"])
            record = TransactionLog(issueBankAccID=int(request.POST["issueBankAccID"]), 		  acqBankAccID=int(request.POST["acqBankAccID"]), amount=float(request.POST["amount"]), currencyCode=int(request.POST["currencyCode"]), UUID=unique_id[0])
            record.save()
            save_id = UUID(unique_ID=random_id)
            save_id.save()
        except:
            return JsonResponse({"StatusCode":403, "UUID": random_id, "Comment": "Transaction request failed."})

        # If it reached here, it succeeded
        return JsonResponse({"StatusCode":200, "UUID": random_id, "Comment": "Success."})
    # Error 104
    return JsonResponse({"StatusCode":104, "UUID": random_id, "Comment": "Request type is not POST."})

    
def InitiateAuthDebit(request):
    random_id = uuid.uuid4()
    if request.method == "POST":
        # Error 100
        if len(request.POST) == 0:
            return JsonResponse({"StatusCode":100, "UUID": random_id, "Comment": "Request body empty."})
        # Error 101
        try:
            issueBankAccID = request.POST["issueBankAccID"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find issueBankAccID field."})
        try:
            acqBankAccID = request.POST["acqBankAccID"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find acqBankAccID field."})
        try:
            amount = request.POST["amount"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find amount field."})
        try:
            currencyCode = request.POST["currencyCode"]
        except MultiValueDictKeyError:
            return JsonResponse({"StatusCode":101, "UUID": random_id, "Comment": "Could not find currencyCode field."})
        # Error 102
        if request.POST["amount"] == '0':
            return JsonResponse({"StatusCode":102, "UUID": random_id, "Comment": "Transaction amount had amount 0."})
        # Error 103
        if float(request.POST["amount"]) > 25000:
            return JsonResponse({"StatusCode":103, "UUID": random_id, "Comment": "Transaction amount exceeded the limit of 25000."})
        # Error 401
        try:
            # Error 402
            if Bank.objects.filter(accountNumber=request.POST["issueBankAccID"]) == 0:
                return JsonResponse({"StatusCode":402, "UUID": random_id, "Comment": "Bank with number {} could not be located.".format(request.POST["issueBankAccID"])})
            if Bank.objects.filter(accountNumber=request.POST["acqBankAccID"]) == 0:
                return JsonResponse({"StatusCode":402, "UUID": random_id, "Comment": "Bank with number {} could not be located.".format(request.POST["cqBankAccID"])})
        except (ObjectDoesNotExist, FieldDoesNotExist):
            return JsonResponse({"StatusCode":401, "UUID": random_id, "Comment": "Could not access database."})
        # Error 404
        try:
            bank1 = Bank.objects.filter(accountNumber=request.POST["issueBankAccID"])
            bank2 = Bank.objects.filter(accountNumber=request.POST["acqBankAccID"])
                
            unique_id = UUID(unique_ID=random_id)
            unique_id.save()
        except:
            return JsonResponse({"StatusCode":404, "UUID": random_id, "Comment": "Transaction could not be authorised."})
        # If it reached here, it succeeded
        return JsonResponse({"StatusCode":200, "UUID": random_id, "Comment": "Success."})
    # Error 104
    return JsonResponse({"StatusCode":104, "UUID": random_id, "Comment": "Request type is not POST."})
