from rest_framework import serializers
from .models import Article, Reader, Author, Comment

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "author", "title", "content", "category", "likes", "created_at", "updated_at"]

class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ["id", "username", "first_name", "last_name", "following", "created_at", "updated_at"]

class AuthorSerializer(serializers.ModelSerializer):
    followers = ReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "username", "first_name", "last_name", "following", "created_at", "updated_at", "bio", "followers"]

class CommentSerializer(serializers.ModelSerializer):
    likes = ReaderSerializer(many=True, read_only=True)
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "article", "commenter", "content", "likes", "parent", "replies", "created_at", "updated_at"]


