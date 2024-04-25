from rest_framework import serializers
from .models import *

class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=50)
    content = serializers.CharField()
    recipient = serializers.EmailField()
    message = serializers.CharField()


    class Meta:
        model=Email
        fields = ['id', 'html_content', 'sender_username', 'created_at']