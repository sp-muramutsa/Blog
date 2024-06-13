from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import IntegrityError
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ArticleForm

from .models import *

# Create your views here.
def index(request):
    articles = Article.objects.all()
    return render(request, "odisea/index.html", {
        "articles": articles
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        print(username, password)
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

def is_author(user):
    return user.username.startswith("odiseade")

@login_required(login_url="login")
@user_passes_test(is_author, login_url="index")
def new(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = Author.objects.get(username=request.user.username)
            article.save()
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, "odisea/new.html", {"form": form})


def author(request, author_username):
    author = Author.objects.filter(username=author_username).first()
    articles = author.get_articles()
    user_is_author = is_author(request.user)
    return render(request, "odisea/author.html", {
        "author": author,
        "user_is_author": user_is_author,
        "articles": articles
    })


def article(request, article_id):
    article = Article.objects.filter(id=article_id)
    return render(request, "odisea/article.html", {
        "article": article
    })

# neymar, neymar@brasil.com, neymarjunior11
# sandrinmuramutsa, sandrinmuramutsa@gmail.com, pacodisea