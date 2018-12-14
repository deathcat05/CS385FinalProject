# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from restapi.serializers import *
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

import json

class ContentViewSet(viewsets.ModelViewSet):
    """
    This is only to be used with a multipart/form-data
    Read the README.md for the specs
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def create(self, request, *args, **kwargs):
        # print(request.user.id)
        tags_data = request.data.pop('tag', None)
        content = self.content_serializer(request)
        self.create_tags(tags_data, content)

        return Response({"id": content.id})

    def update(self, request, *args, **kwargs):
        request_data = request.data.copy()
        new_tags_data = request_data.pop('tag', None)
        content = Content.objects.get(pk=kwargs['pk'])
        
        # Updating content
        if content.owner == request.user:
            content_serializer = ContentSerializer(content, data=request.data)
            original_tags_data = ContentTags.objects.filter(content=content)
            original_tags_data.delete() # delete the orig tags
            self.create_tags(new_tags_data, content)
        
            return Response({"id": content.id})
        return Response({"Message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

    def get_permissions(self):
        if ( 
            self.action == 'create' or 
            self.action == 'update' or 
            self.action == 'partial_update' or
            self.action == 'destroy'
          ):
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [AllowAny, ]
        return [permission() for permission in permission_classes]

    def content_serializer(self, request):
        content_serializer = ContentSerializer(data=request.data, context={"owner": request.user})
        content_serializer.is_valid(raise_exception=True)
        return content_serializer.save()

    def create_tags(self, tags_data, content):
        if tags_data is None:
            return
        for tag in tags_data:
            tag = Tag.objects.get_or_create(tag=tag)
            ContentTags.objects.create(content=content, tag=tag[0])

    def destroy(self, request, *args, **kwargs):
        content = Content.objects.get(pk=kwargs['pk'])
        if content.owner == request.user:
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        return Response({"Message": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

class TagsView(generics.ListAPIView):
    """
    This is only used for viewing/debugging purposes.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class SubscriptionsView(viewsets.ModelViewSet):
    """
    {
        "user": {
            "id": 1
        }
    }

     {
        "tag": {
            "id": 1
        }
    }
    """
    queryset = UserExtended.objects.all()
    serializer_class = SubscriptionsSerializer
    permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        subscriptions = UserExtended.objects.filter(user=request.user.id)
        # For debugging
        # subscriptions = UserExtended.objects.all()
        subscription_serializer = SubscriptionsSerializer(subscriptions, many=True)
        return Response(subscription_serializer.data)

    def create(self, request, *args, **kwargs):
        follower = request.user
        following = request.data.get('user')
        if following:
            following = following.get('id')
            follower = UserExtended.objects.get(user=follower.id)
            followed = UserExtended.objects.get(user=follower).follow_user(user_id=following)
            return Response({"followed": followed})

        tag_id = request.data.get('tag').get('id')
        if tag_id:
            tag = Tag.objects.get(pk=tag_id)
            user = UserExtended.objects.get(pk=follower.id)
            user_tag = UserTag.objects.filter(user=user, tag=tag)
            if not user_tag.exists():
                UserTag.objects.create(user=user, tag=tag)
                return Response({"tag": True})
            else:
                return Response({"tag": "Already following"})

    def retrieve(self, request, *args, **kwargs):
        return Response({"Message":"Request not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return Response({"Error": "Unable to follow"})

class SubscribersView(generics.RetrieveAPIView):
    queryset = UserExtended.objects.all()
    serializer_class = SubscribersSerializer

class TagSubscribersView(generics.ListAPIView):
    lookup_field = 'tag'
    queryset = UserTag.objects.filter()
    serializer_class = UserTagSerializer

    def get_queryset(self):
        tag = self.kwargs.get('tag', None)
        users = UserTag.objects.filter(tag=tag) # we have all the users associated with the tag
        return users

class FeedView(generics.ListAPIView):
    queryset = UserExtended.objects.all()
    serializer_class = FeedSerializer

    def list(self, request, *args, **kwargs):
        # Get a list of content
        user = UserExtended.objects.get(user=request.user)
        users_following = user.get_following()

        if users_following is not None:
            content = Content.objects.filter(owner=users_following[0].user)
        for i in users_following:
            content = content | Content.objects.filter(owner=i.user)

        user_tags = user.get_tags()
        if users_following is None and user_tags is not None:
            content = Content.objects.filter(tags=user_tags[0])
        for i in user_tags:
            content = content | Content.objects.filter(tags=i)
        if content:
            content = content.distinct().order_by("-created")
            content_serializer = ContentSerializer(content, many=True)
            return Response({"content": content_serializer.data})
            
        return Response({"content": None})

class SearchView(generics.CreateAPIView):
    """
    {"search": "string"}
    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    def create(self, request, *args, **kwargs):
        search = request.data.pop('search', None)
        content = Content.objects.filter(description__icontains=search) | Content.objects.filter(tags__tag__icontains=search)
        content = content.distinct().order_by("-created")
        if content:
            content_serializer = ContentSerializer(content, many=True)
            return Response({"results": content_serializer.data})
        return Response({"results": None})