from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from notifications.models import Notification
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer, PostCreateUpdateSerializer,
    CommentSerializer, CommentCreateUpdateSerializer,
    LikeSerializer
)

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post CRUD operations
    """
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content']
    filterset_fields = ['author']
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific post
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a post and create notification
        """
        post = self.get_object()
        serializer = CommentCreateUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                content=serializer.validated_data['content']
            )
            
            # Create notification for post author (if not self-comment)
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb='comment',
                    target=post
                )
            
            return Response(
                CommentSerializer(comment, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='like')
    def like_post(self, request, pk=None):
        """
        Like a post and create notification
        """
        # Use get_object_or_404 from django.shortcuts (not generics)
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Use get_or_create as required by ALX
        like, created = Like.objects.get_or_create(user=user, post=post)
        
        if created:
            # Create notification for post author (if not self-like)
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='like',
                    target=post
                )
            
            return Response({
                'message': 'Post liked successfully',
                'likes_count': post.likes.count()
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'You already liked this post'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='unlike')
    def unlike_post(self, request, pk=None):
        """
        Unlike a post
        """
        # Use get_object_or_404 from django.shortcuts
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        like = Like.objects.get_or_create(user=request.user, post=post)
        like.delete()
        
        return Response({
            'message': 'Post unliked successfully',
            'likes_count': post.likes.count()
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def likes(self, request, pk=None):
        """
        Get all users who liked this post
        """
        post = self.get_object()
        likes = post.likes.all()
        serializer = LikeSerializer(likes, many=True, context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment CRUD operations
    """
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateUpdateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    def get_queryset(self):
        queryset = Comment.objects.all()
        post_id = self.request.query_params.get('post', None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset


class FeedView(generics.ListAPIView):
    """
    Feed view - shows posts from users that the current user follows
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Get all users that the current user follows
        following_users = user.following.all()
        # Return posts from followed users, ordered by most recent
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context