from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import CATEGORY_CHOICES
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class AbstractUserBase(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Reader(AbstractUserBase):
    following = models.ManyToManyField("Author", related_name="followers", blank=True)

    class Meta:
        verbose_name = "Reader"
        verbose_name_plural = "Readers"
    
    def get_following(self):
        return self.following.all()


class Author(Reader):
    bio = models.TextField()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        permissions = [
            ("new", "Can view the new page and create blogs there."),
        ]

    def get_articles(self):
        return self.articles.all()

    def get_followers(self):
        return self.followers.all()


class Article(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="articles", default=3)
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=150, choices=CATEGORY_CHOICES, default="Personal")
    likes = models.ManyToManyField("Reader", related_name="liked_posts", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate initial slug
            slug = slugify(self.title)
            # Check if the slug is unique and modify it if necessary
            if Article.objects.filter(slug=slug).exists():
                slug = f'{slug}-{get_random_string(5)}'
            self.slug = slug
        super(Article, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_likes(self):
        return self.likes.all()
    
    def get_comments(self):
        return self.comments.all()
    

class Comment(models.Model):
    article = models.ForeignKey("Article", on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey("Reader", on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField("Reader", related_name="liked_comments", blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.commenter} on {self.article}"
    
    def likes_count(self):
        return self.likes.count()
    
    def replies_count(self):
        return self.replies.count()
