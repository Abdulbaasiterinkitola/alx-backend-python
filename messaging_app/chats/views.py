from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Conversation, Message, User, Role
from .pagination import MessagePagination
from .filters import MessageFilter
from .permissions import IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import ConversationSerializer, MessageSerializer, RoleSerializer, UserSerializer
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes

class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    permission_classes=[IsAuthenticated]

    queryset = Conversation.objects.all().prefetch_related('participants')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation between users.
        Expected payload:
        {
            "participant_ids": [<user_id_1>, <user_id_2>, ...]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Retrieve all messages in a specific conversation.
        """
        conversation = self.get_object()
        messages = Message.objects.filter(
            sender__in=conversation.participants.all(),
            receiver__in=conversation.participants.all()
        ).order_by('sent_at')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    permission_classes=[IsAuthenticated]
    
    queryset = Message.objects.all().select_related('sender', 'receiver')
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message between users.
        Expected payload:
        {
            "sender_id": "<user_id>",
            "receiver_id": "<user_id>",
            "message_body": "Hello!"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    """Viewset for user management
    """

    queryset = User.objects.all().prefetch_related('conversations')
    serializer_class = UserSerializer

    @permission_classes([AllowAny])
    def create(self, request, *args, **kwargs):
        """ Any user can create a new user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)

    @permission_classes([IsAuthenticated, IsAdminUser])
    def list(self, request, *args, **kwargs):
        """ Admin can list all users"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    @permission_classes([IsAuthenticated, IsAdminUser])
    def user(self, request, *args, **kwargs):
        """ Admin/ user can get a user"""
        user_id = kwargs['pk'] or request.user.user_id
        user = self.get_queryset().get(user_id=user_id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    """Viewset for role management
    """ 
    permission_classes=[IsAuthenticated, IsAdminUser]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return Response(self.get_serializer(role).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if kwargs['pk']:
            queryset = queryset.filter(role_id=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    