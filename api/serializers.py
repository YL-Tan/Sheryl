"""
model serializer - because response object cannot natively handle complex data types such as django model instances
So, we have to serialize the data before we can actually render it out

this class defines to control how instances of your Chat model should be converted into these serializable formats
"""
from rest_framework import serializers
from chatbot.models import Chat

class ChatSerializer(serializers.ModelSerializer):  #inheriting from the ModeSerializer class
    response = serializers.CharField(allow_blank=True, default='') 
    user = serializers.StringRelatedField()
    # session = serializers.StringRelatedField()
    history = serializers.JSONField(default=list)
    
    class Meta:
        model = Chat
        fields = ['user', 'message', 'history', 'response', 'created_at']

#note that this is a read-only configuration. 
# If you want to support writing (i.e., creating or updating Chat instances) 
# through this serializer, you would need to implement create() and update() 
# methods, or use primary key related fields for 'user' and 'session'. 
# In this case, you would handle them as the id of the user and the session, 
# respectively.