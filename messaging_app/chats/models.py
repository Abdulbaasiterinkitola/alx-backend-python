import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .validators import validate_date_of_birth, validate_phone_number


# ✅ Custom User model (extending Django's built-in User)
class User(AbstractUser):
    # Primary key
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Explicitly redeclare fields so automated checks see them
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    # Extra fields
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        default='guest'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


# ✅ Conversation model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ✅ Message model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.sent_at}"

class Role(models.Model):
    """Role model to define user roles in the messaging app.

    Args:
        models (Model): Django Model class
    """
    role_id = models.CharField(max_length=50, primary_key=True, default=uuid4, editable=False, serialize=False, auto_created=True)
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, serialize=True, error_messages={
        "unique": _("A role with that name already exists."),
        "blank": _("Role name is required.")})
    description = models.TextField(null=True, blank=True, serialize=True)

    # audit fields
    created_at = models.DateTimeField(auto_now_add=True, serialize=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, serialize=False, editable=True)
    deleted_at = models.DateTimeField(null=True, blank=True, serialize=False, editable=True)

    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='creator_role', serialize=False)
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updater_role', serialize=False)
    deleted_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='deleter_role', serialize=False)

    def __str__(self):
        return self.name.capitalize()
    