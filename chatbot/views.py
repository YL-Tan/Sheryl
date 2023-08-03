from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token

from .models import Chat

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def chatbot(request):
    # if not request.session.session_key:
    #     request.session.create()
    
    # context = {'sessionId': request.session.session_key}
    chats = Chat.objects.filter(user=request.user)  # filter to get the chats history for the current logged in user
    token, created = Token.objects.get_or_create(user=request.user)
    
    return render(request, 'chatbot.html', {'chats': chats, 'token': token.key})    # django will go /templates and fetch the specified file; chats (:type list) are from the sqlite database

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {'error_message': error_message})
    else:
        return render(request, 'login.html')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password2)
                user.save()
                return redirect('login')
            except:
                error_message = "Failed to create your account"
                return render(request, "register.html", {'error_message': error_message})
        else:
            error_message = 'Passwords did not match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, "register.html")

def logout(request):
    auth.logout(request)
    return redirect('login')
    
