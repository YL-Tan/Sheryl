from django.shortcuts import render, redirect
from django.http import JsonResponse
import openai
import json
from django.contrib import auth
from django.contrib.auth.models import User
from .models import Chat

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

from django.utils import timezone

def ask_openai(message):
    with open('api.json', 'r') as file_to_read:
        json_data = json.load(file_to_read)
        openai.api_key = json_data["openai_api_key"]
        
    # response = openai.Completion.create(
    #     model = "text-curie-001",
    #     prompt = message,
    #     max_tokens = 150,
    #     n = 1,
    #     stop = None,
    #     temperature = 0.7,
    # )
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]     
    )
    answer = response.choices[0].message.content.strip()
    print("\n" + answer + "\n")
    formatter = HtmlFormatter()
    code_html = highlight(answer, PythonLexer(), formatter)
    return code_html
    
# Create your views here.
def chatbot(request):
    chats = Chat.objects.filter(user=request.user)  # filter to get the current logged in user
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
    
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html', {'chats': chats})

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
                auth.login(request, user)
                return redirect('chatbot')
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
    
