from django.shortcuts import render
from django.http import JsonResponse
import openai
import json

def ask_openai(message):
    with open('apikeys.json', 'r') as file_to_read:
        json_data = json.load(file_to_read)
        openai.api_key = json_data["openai_api_key"]
        
    response = openai.Completion.create(
        model = "text-curie-001",
        prompt = message,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.7,
    )

    answer = response.choices[0].text.strip()
    return answer
    
# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')