from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of a conversation can send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Require authentication
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Explicitly check for GET, POST, PUT, PATCH, DELETE methods.
        Only participants are allowed.
        """
        if hasattr(obj, "participants"):  # Conversation
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, "conversation"):  # Message
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        # Allow read-only access (GET, HEAD, OPTIONS) if participant
        if request.method in permissions.SAFE_METHODS:
            return is_participant

        # Explicit checks for modification methods
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return is_participant

        return False

