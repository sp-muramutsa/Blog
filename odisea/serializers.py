from rest_framework import serializers
from .models import Article, Reader, Author, Comment

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {
            'author': {'required': False}
        }
    
# class ReaderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reader
#         fields = '__all__'

# class AuthorSerializer(serializers.ModelSerializer):
#     followers = ReaderSerializer(many=True, read_only=True)

#     class Meta:
#         model = Author
#         fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#     likes = ReaderSerializer(many=True, read_only=True)
#     replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

#     class Meta:
#         model = Comment
#         fields = '__all__'


