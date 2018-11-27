# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from restapi.serializers import *
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import render

# Create your views here.
class ContentViewSet(viewsets.ModelViewSet):
    """
    This is the format to follow for post:
    {
    "tags": [
        {"tag": "some_hashtag"},
        {"tag": "another_hashtag"}
    ],
    "description": "Description"
    }

    """
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    # permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        # we are going to create the Content first
        # print("TEST....\n\n\n")
        # print(request.data)
        content_serializer = ContentSerializer(data=request.data)
        content_serializer.is_valid(raise_exception=True)
        content_serializer.save()

        return Response(content_serializer.data)

class TagsView(generics.ListAPIView):
    """
    This is only used for viewing purposes.
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

        return Response({"Error": "Unable to follow"})