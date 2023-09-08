from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import uuid
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Transactions, User


@login_required
def default(request):
    return render(request, 'banque/index.html')


@csrf_exempt
@login_required
def getState(request):
    operation = Transactions.objects.filter(user_to_id=request.user.id, is_validated=False, is_deleted=False).last()
    operations = Transactions.objects.filter(user_from_id=request.user.id, is_validated=True, is_deleted=False)
    retraits = Transactions.objects.filter(user_to_id=request.user.id, is_validated=True, is_deleted=False)
    
    operations = [op.serialise() for op in operations] + [op.serialise() for op in retraits]
    
    if operation:
        operation = operation.serialise()
    else:
        operation = False
    
    context = {
        'balance': request.user.balance,
        'operation': operation,
        'operations': operations,
    }
    
    return JsonResponse(context)

@csrf_exempt
@login_required
def createUser(request):
    data = json.loads(request.body.decode('utf-8'))
    firstname = data.get('first_name')
    lastname = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('password2')
    
    if password and email and firstname and lastname:

        if password == confirm_password:
            try:
                account_num = uuid.uuid4()
                account_num = str(account_num).upper()[:8]
                account_num = f"G8-{account_num}"
                    
                user = User.objects.create_user(
                        first_name=firstname,
                        last_name=lastname,
                        email=email,
                        is_staff=True,
                        balance=5000,
                        password=password,
                        account_num=account_num,
                    )
                return JsonResponse({'success': 'Créaction du compte éffectuer avec succès, bonne journée !'})
            except:
                error = "Un utilisateur existe déjà avec le même email"
        else:
            error = "Vos deux mots de passe ne sont pas identiques"            
    else:
        error = "Veuillez remplir tout les champs"
        
    return JsonResponse({'error': error}, status=400)

@csrf_exempt
@login_required
def depot(request):
    data = json.loads(request.body.decode('utf-8'))
    account_num = data.get('account_num')
    balance = data.get('balance')
    password = data.get('user_password')
    ref = data.get('ref')
    
    if account_num and (balance > 0) and password:
        if request.user.check_password(password):
            user = User.objects.filter(account_num=account_num).first()            
            if user:
                if request.user.can_send(balance):
                    Transactions.objects.create(
                        operation='Dépot',
                        ref=ref,
                        user_from=request.user,
                        user_to=user,
                        balance=balance,
                    )
                    if not request.user.is_superuser:
                        request.user.balance -= balance
                        request.user.save()

                    user.balance += balance
                    user.save()
                    
                    return JsonResponse({'success': 'Transfert éffectuer avec succès, bonne journée !'})
                else:
                    error = "Votre solde est insuffisant pour cette operation"
            else:
                error = "Le numéro de compte du destinataire est invalide, verifiez encore"
        else:
            error = "Votre mot de passe est incorrect"
    else:
        error = "Veuillez remplir tout vos champs de saisir"
    
    return JsonResponse({'error': error}, status=400)

@csrf_exempt
@login_required
def retrait(request):
    data = json.loads(request.body.decode('utf-8'))
    account_num = data.get('account_num')
    balance = data.get('balance')
    password = data.get('user_password')
    
    if account_num and (balance > 0) and password:
        if request.user.check_password(password):
            user = User.objects.filter(account_num=account_num).first()            
            if user:
                if user.can_send(balance):
                    Transactions.objects.create(
                        operation='Rétrait',
                        user_from=request.user,
                        user_to=user,
                        balance=balance,
                        is_validated=False,
                    )
                    return JsonResponse({'success': 'Transfert en attente de validation, vous serez notifier une fois confirmer !'})
                else:
                    error = "Le solde du compte correspondant est insuffisant pour cette operation"
            else:
                error = "Le numéro de compte du destinataire est invalide, verifiez encore"
        else:
            error = "Votre mot de passe est incorrect"
    else:
        error = "Veuillez remplir tout vos champs de saisir"
    
    return JsonResponse({'error': error}, status=400)

@csrf_exempt
@login_required
def confirm_retrait(request):
    data = json.loads(request.body.decode('utf-8'))
    tras_id = data.get('id')
    user_id = data.get('user_from')
    balance = data.get('balance')
    
    if request.user.can_send(balance):
        
        user_from = User.objects.get(id=user_id['id'])
        user_from.balance += balance
        user_from.save()
        
        transaction = Transactions.objects.get(id=tras_id)
        transaction.is_validated = True
        transaction.save()
        
        request.user.balance -= balance
        request.user.save()
        
        return JsonResponse({'success': "La transaction a bien été validé"}) 
    else:
        error = "Votre solde est insuffisant pour cette operation"
    
    return JsonResponse({'error': error}, status=400)

@csrf_exempt
@login_required
def cancel_retrait(request):
    data = json.loads(request.body.decode('utf-8'))
    tras_id = data.get('id')
    
    transaction = Transactions.objects.get(id=tras_id)
    transaction.is_deleted = True
    transaction.save()
    
    return JsonResponse({'success': "La transaction a bien été réfusé"})