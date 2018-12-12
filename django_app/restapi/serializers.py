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

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'
        read_only_fields = ('thumbnail', 'medium', 'default',)


class ContentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    images = ImagesSerializer()

    def create(self, validated_data):
        # Must pop off the tags data first
        tags_data = validated_data.pop('tags')

        print ("printing context... tags_data")
        print(tags_data)
        # print (self.context)

        # Then we can create the content object
        content = Content.objects.create(**validated_data)
        # # This is iterating over a list of OrderedDicts
        for tag in tags_data:
            print (tag['tag'])
            # print(tag['tag']) # will print the tag string
            # print(tag) # will print the OrderedDict
            # print(tag.tag) # will product err - obj has no attribute tag ...
        
            # Get or create the tag if it does not exist
            # print (tag)
        
            # This made for odd behavior and unexpected results
            # tag = Tag.objects.get_or_create(tag) # (<Tag: Tag object>, False)
        
            # Needed to use the name not about the object
            tag = Tag.objects.get_or_create(tag=tag['tag'])
        
            # tag = Tag.objects.get_or_create(tag)[0] # Tag object
            # print(tag)
            tag = tag[0]
            # tag = Tag.objects.get_or_create(tag)[0].tag # CharField
        
            # Populate the M:N table
            print "creating contenttags..."
            ContentTags.objects.create(content=content, tag=tag)
            print "after contenttags..."


        return content

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
