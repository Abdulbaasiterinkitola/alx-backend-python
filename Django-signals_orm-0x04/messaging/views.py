from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    """
    Allow a logged-in user to delete their account.
    All related data (messages, notifications, history)
    will be cleaned automatically by post_delete signal.
    """
    user = request.user

    if request.method == "POST":
        username = user.username
        user.delete()
        logout(request)
        messages.success(request, f"Account '{username}' and all related data deleted successfully.")
        return redirect("login")  # Redirect to login page or homepage

    return redirect("profile")  # Default redirect if GET request
