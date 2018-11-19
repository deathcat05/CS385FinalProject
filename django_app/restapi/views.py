# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from restapi.serializers import *
from rest_framework import viewsets, generics
from rest_framework.response import Response

from django.shortcuts import render

# Create your views here.
class ContentViewSet(viewsets.ModelViewSet):
    """
    This is the format to follow fpor post:
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

    def create(self, request, *args, **kwargs):
        # data = request.data
        # content_data = data.pop('description')
        # tags_data = request.data.pop('tags')
        # print(content_data)

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
