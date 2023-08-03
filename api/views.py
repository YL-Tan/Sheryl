from rest_framework import viewsets
from rest_framework.response import Response # Response will take in any python data or already serialized data that we pass into it and rendered it out as json data
from rest_framework.permissions import IsAuthenticated
from .serializers import ChatSerializer
from chatbot.models import Chat
from .openai_services import get_chatbot_response
from datetime import datetime


class ChatViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    def create(self, request):
        serializer = ChatSerializer(data=request.data)
        
        if serializer.is_valid():
            message = serializer.validated_data.get('message')
            history = serializer.validated_data.get('history', [])
            chatbot_response = get_chatbot_response(history, message)
            
            updated_history = history.copy()
            updated_history.append({'role': 'assistant', 'message': chatbot_response, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
                
            # save the response in a new Chat object        
            chat = Chat.objects.create(user=request.user, message=message, response=chatbot_response, history=updated_history)
            
            return  Response({'id': chat.id, 'message': message, 'response': chatbot_response, 'history': updated_history}, status=201)
        return Response(serializer.errors, status=400)