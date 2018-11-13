# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from restapi.serializers import *
from rest_framework import viewsets
from rest_framework.response import Response

from django.shortcuts import render

# Create your views here.
class contentViewSet(viewsets.ModelViewSet):

    queryset = content.objects.all()
    serializer_class = contentSerializer
