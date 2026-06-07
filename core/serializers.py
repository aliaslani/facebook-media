from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from core.models import Post


class PostSerializer(ModelSerializer):
    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at',  'username', 'subject']
        read_only_fields = ['id', 'created_at', 'username']



    def validate(self, attrs):
        user = self.context['request'].user
        if user.is_authenticated:
            attrs['user'] = user
        else:
            raise serializers.ValidationError({'user': 'User must be authenticated'})
        return attrs