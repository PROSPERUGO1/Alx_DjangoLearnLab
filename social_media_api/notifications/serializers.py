from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from posts.models import Post, Comment
from accounts.models import CustomUser

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model
    """
    actor_username = serializers.ReadOnlyField(source='actor.username')
    actor_profile_picture = serializers.ImageField(source='actor.profile_picture', read_only=True)
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'actor_username', 'actor_profile_picture',
                  'verb', 'target_type', 'target_id', 'read', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'timestamp']
    
    def get_target_type(self, obj):
        if obj.target:
            return obj.target.__class__.__name__.lower()
        return None
    
    def get_target_id(self, obj):
        if obj.target:
            return obj.target.id
        return None