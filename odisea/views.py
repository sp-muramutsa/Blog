from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, permission_required
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *

# Create your views here.
def index(request):
    return render(request, "odisea/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "odisea/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "odisea/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "odisea/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new reader
        try:
            user = Reader.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "odisea/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "odisea/register.html")
    

def about(request):
    return render(request, "odisea/about.html")


@login_required(login_url="login")
@permission_required("odisea.new", raise_exception=True)
def new(request):
    return render(request, "odisea/new.html")
# neymar, neymar@brasil.com, neymarjunior11
# sandrinmuramutsa, sandrinmuramutsa@gmail.com, pacodisea