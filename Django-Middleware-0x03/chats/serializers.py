from rest_framework import serializers
from .models import User, Conversation, Message


# User Serializer

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # Example of SerializerMethodField

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'role', 'created_at'
        ]
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# Message Serializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # Explicit CharField

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'message_body', 'sent_at'
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty")
        return value


# Conversation Serializer

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    conversation_id_str = serializers.SerializerMethodField()  # Another SerializerMethodField

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'conversation_id_str', 'participants', 'messages', 'created_at'
        ]
    
    def get_conversation_id_str(self, obj):
        return str(obj.conversation_id)

