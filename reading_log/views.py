from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Main page shows reading list..
def index(request):
    return render(request, "index.html", {})

# Login view (POSTed from the account panel in header)
def login_view(request):
    # Take user submissions..
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"

    # Attempt to login..
    user = authenticate(request, username=username, password=password)
    if user is None:
        # User not found, so show error and redirect..
        messages.error(request, "Invalid username or password.")
        return redirect(next_url)

    # User found, so log them in and redirect..
    login(request, user)
    return redirect(next_url)

# Register form - inline..
def register(request):

    # User tried to create an account, so process the request..
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create user object..
            user = form.save()

            # Log into freshly created user and redirect to home page
            login(request, user)
            return redirect("index")

    # Any other request should just show the form..
    else:
        form = UserCreationForm()

    # Pass form into template for rendering (i didn't bother styling it for this assignment..)
    return render(request, "register.html", {"form": form})