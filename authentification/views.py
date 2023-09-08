from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from .models import MyUser as User
import uuid


def login(request):
    if request.user.is_authenticated:
        return redirect('default')
    error = []

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if password and email:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                user_login(request, user)
                return redirect('default')
            error = "Mot de passe ou numero email invalide"
        else:
            error = "Veuillez remplir tout les champs"

    context = {
        'error': error
    }

    return render(request, 'authentification/login.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('default')
    
    error = ''

    if request.method == 'POST':

        email = request.POST.get('email')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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
                            password=password,
                            account_num=account_num,
                        )
                    user = authenticate(request, username=email, password=password)
                    if user is not None:
                        user_login(request, user)
                        return redirect('default')
                    else:
                        error = "Mot de passe ou numero matricule invalide"
                except:
                    error = "Un utilisateur existe déjà avec le même email"
            else:
                error = "Vos deux mots de passe ne sont pas identiques"            
        else:
            error = "Veuillez remplir tout les champs"

    context = {
        'error': error
    }

    return render(request, 'authentification/register.html', context)

def new_password(request):

    context = {}

    return render(request, 'authentification/forgot-password.html', context)

def logout(request):
    user_logout(request)
    return redirect('login')