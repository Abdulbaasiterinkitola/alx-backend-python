from rest_framework import serializers
from .models import User, Role, Message, Conversation

class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    
    class Meta:
        model = Role
        fields = ['name', 'description']
    
class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password','phone_number', 'role_id', 'role', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def validate_phone_number(self, value):
        """Custom validation using ValidationError"""
        if not value.startswith('+'):
            raise serializers.ValidationError("Phone number must start with '+'.")
        return value


class MiniUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name().capitalize()

class MessageSerializer(serializers.ModelSerializer):
    sender = MiniUserSerializer(read_only=True)
    receiver = MiniUserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='sender', write_only=True
    )
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='receiver', write_only=True
    )

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender', 'sender_id',
            'receiver', 'receiver_id',
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = MiniUserSerializer(read_only=True)
    receiver = MiniUserSerializer(read_only=True)

    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='sender', write_only=True
    )
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='receiver', write_only=True
    )

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'receiver',
            'receiver_id',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = MiniUserSerializer(many=True, read_only=True)
    participant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, source='participants', write_only=True
    )

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',
            'messages',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        participants = validated_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
    