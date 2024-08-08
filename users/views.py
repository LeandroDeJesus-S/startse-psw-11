from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signup(request: HttpRequest):
    """the view which have the function of to register new users"""
    SIGNUP_URL = redirect('signup')

    if request.method == 'GET':
        return render(request, 'signup.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('senha')
        password_confirm = request.POST.get('confirmar_senha')
        
        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return SIGNUP_URL
        
        elif len(password) < 8:
            messages.error(request, 'Senha precisa ter no mínimo 8 dígitos')
            return SIGNUP_URL

        elif password != password_confirm:
            messages.error(request, 'Senhas não são iguais.')
            return SIGNUP_URL
        
        User.objects.create(username=username, password=password)
        return redirect('signin')


def signin(request: HttpRequest):
    """the view which have the function to authenticate an user"""
    if request.method == "GET":
        return render(request, 'signin.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('senha')

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, 'Credenciais inválidas')
            return redirect('signin')

        login(request, user)
        return redirect('signup_company')
