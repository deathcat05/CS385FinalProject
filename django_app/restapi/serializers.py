from rest_framework import serializers
from restapi.models import *
from django.contrib.auth.models import User


class UsernameUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag',)


class ContentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    def create(self, validated_data):
        return Content.objects.create(owner=self.context.get('owner'), **validated_data)

    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ('thumbnail', 'medium', 'default', 'owner')

class UsernameUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username',)

class UsernameUserIdSerializerUserExtended(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserExtended
        fields = ('id', 'username',)

class SubscriptionsSerializer(serializers.ModelSerializer):
    user = UsernameUserIdSerializer(read_only=True)
    followers = UsernameUserIdSerializerUserExtended(many=True, read_only=True)
    following = UsernameUserIdSerializerUserExtended(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = UserExtended
        fields = '__all__'
        read_only_fields = ('user', 'followers',)
