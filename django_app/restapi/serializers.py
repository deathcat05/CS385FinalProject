from rest_framework import serializers
from restapi.models import *

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'tag',)


class ContentSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    def create(self, validated_data):
        # Must pop off the tags data first
        tags_data = validated_data.pop('tags')

        # Then we can create the content object
        content = Content.objects.create(**validated_data)

        # This is iterating over a list of OrderedDicts
        for tag in tags_data:
            # print(tag['tag']) # will print the tag string
            # print(tag) # will print the OrderedDict
            # print(tag.tag) # will product err - obj has no attribute tag ...

            # Get or create the tag if it does not exist
            print (tag)

            # This made for odd behavior and unexpected results
            # tag = Tag.objects.get_or_create(tag) # (<Tag: Tag object>, False)

            # Needed to use the name not about the object
            tag = Tag.objects.get_or_create(tag=tag['tag'])

            # tag = Tag.objects.get_or_create(tag)[0] # Tag object
            print(tag)
            tag = tag[0]
            # tag = Tag.objects.get_or_create(tag)[0].tag # CharField

            # Populate the M:N table
            ContentTags.objects.create(content=content, tag=tag)


        return content

    class Meta:
        model = Content
        fields = '__all__'

