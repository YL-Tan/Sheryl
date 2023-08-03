import openai
import os
from datetime import datetime

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_chatbot_response(history: str, message: str) -> str:
    if not history:
        history.append({'role': 'system', 'message': 'You are a helpful assistant.', 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    # Add the new message to the end of history
    history.append({'role': 'user', 'message': message, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    # Convert each item in history to the format expected by the ChatCompletion.create() method
    messages = [{'role': item['role'], 'content': item['message']} for item in history]
    
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    # )
    # answer = response.choices[0].message.content.strip()
    answer = "I'm sorry, you're not connected to openai API"
    return answer