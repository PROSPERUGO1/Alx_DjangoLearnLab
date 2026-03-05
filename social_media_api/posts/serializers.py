from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model
    """
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'username', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    author_profile_picture = serializers.ImageField(source='author.profile_picture', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_username', 'author_profile_picture', 
                  'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    author_profile_picture = serializers.ImageField(source='author.profile_picture', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'author_profile_picture', 
                  'title', 'content', 'created_at', 'updated_at', 
                  'comments', 'comments_count', 'likes_count', 'is_liked']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'likes_count']
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating posts
    """
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value
    
    def validate_content(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Content must be at least 5 characters long.")
        return value


class CommentCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating comments
    """
    class Meta:
        model = Comment
        fields = ['content']
    
    def validate_content(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Comment must be at least 2 characters long.")
        return value