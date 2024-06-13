from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from .choices import CATEGORY_CHOICES

class Article(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=60)
    content = models.TextField()
    category = models.CharField(max_length=150, choices=CATEGORY_CHOICES)
    likes =  models.ManyToManyField("Reader", related_name="liked_posts", blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def likes(self):
        return self.likes
    
    def comments(self):
        return self.comments 
    

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey("Reader", on_delete=models.CASCADE)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)
    likes =  models.ManyToManyField("Reader", related_name="liked_comments", blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
    
    def like_count(self):
        return self.likes.count()
    
    def reply_count(self):
        return self.replies.count()


class Reader(AbstractUser):
    following = models.ManyToManyField("Author", symmetrical=False, related_name="followers", blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"

    def str(self):
        return f"{self.first_name} {self.last_name}"
    
    def following(self):
        return self.following

class Author(Reader):
    bio = models.TextField()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        permissions = [
            ("new", "Can view the new page and create blogs there."),
        ]

    def articles(self):
        return self.articles

    def followers(self):
        return self.followers
