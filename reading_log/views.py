from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import BookReadForm
from .models import BookRead

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

# Adding a book requires login
@login_required
def add_book(request):

    # User tried to submit a book read..
    if request.method == "POST":
        form = BookReadForm(request.POST)
        if form.is_valid():

            # Build class, attach user, save to db
            BookRead = form.save(commit=False)
            BookRead.user = request.user
            BookRead.save()

            # Send back to main index..
            return redirect("index")

        else:
            # Invalid form..
            messages.error(request, "Invalid form fill..")

    # Create empty form if not..
    else:
        form = BookReadForm()

    # Load page again regardless..
    return render(request, "add_book.html", {"form": form})