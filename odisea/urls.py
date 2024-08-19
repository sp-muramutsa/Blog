from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"),
    # # path("register/", views.register, name="register"),
    # # path("login/", views.login_view, name="login"),
    # # path("logout/", views.logout_view, name="logout"),
    # # path("about/", views.about, name="about"),
    # path("<str:author_username>/", views.author, name="author"),
    # path("article/<str:article_id>", views.article, name="article")
    path("articles/", views.articles, name="articles"),
    path("articles/<slug:slug>", views.article_detail, name="article-detail"),
    path("articles-search/", views.articles_search, name="articles-search")
]

# endpoints:
# GET_ALL_NOTES_and_CREATE_NEW_NOTE = "127.0.0.1:8000/notes/"
# GET_SPECIFIC_NOTE = "127.0.0.1:8000/notes/note-slug"