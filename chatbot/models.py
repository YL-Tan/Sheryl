"""
models.py file is for defining your database schema and the relationship 
between different models
"""
from django.db import models
from django.contrib.auth.models import User

"""
Each Chat instance is associated with a single ChatSession, and each ChatSession 
can have multiple Chat instances (messages). 
When the user starts a new chat, a new ChatSession instance is created.
"""
# class ChatSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')  # linking each ChatSession to a Django User
#     session_id = models.CharField(max_length=255, unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self) -> str:
#         formatted_date = self.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         return f'Session {self.id}: {self.user.username} at {formatted_date}'

    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(null=True, blank=True)
    history = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    # session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.username}: {self.message}'

""" FIXME:
However, this means that all existing rows that have NULL for session will have to be handled manually, for example with a RunPython or RunSQL operation. This might involve writing a data migration script or manually updating the rows in the database.

It's generally a good idea to plan your database schema carefully to avoid these kind of issues. But when you have to make changes to existing data, Django provides tools like data migrations to help you do it in a safe and controlled manner.

Once you have resolved this issue, you can enforce that session should always be present for all future Chat objects
"""