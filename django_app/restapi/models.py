# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tag(models.Model):
    # id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    # CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    # trim_whitespace - trims leading and trailing whitespace
    tag = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

class Content(models.Model):
    """
        This  endpoint  also  allows  including  comments  and  tags.
    """
    created = models.DateTimeField(auto_now_add=True)
    # ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)

    # Not sure how to handle a picture for this
    # image = models.ImageField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag, through='ContentTags', related_name='to_contents_tags')
    owner = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'content'

class ContentTags(models.Model):
    # Intermediate table for M:N
    # Content can have many tags
    # and a specific tag can be
    # associated with multiple
    # content.

    # on_delete:
    #   - Just an image is removed we dont want to remove the tag because
    #       other images can be using it
    #   - Because this table is a lookup table connecting the tag and content
    #       if something is deleted from this table it's most likely a tag
    #       and we always want to keep tags intact.
    tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING, related_name="content_tag")
    content = models.ForeignKey(Content, on_delete=models.DO_NOTHING, related_name="content")

    class Meta:
        db_table = 'content_tags___'
