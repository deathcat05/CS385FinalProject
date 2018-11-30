# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# For creating a UserExtended after the User model
# is created.
from django.db.models.signals import post_save
# Create your models here.

class Tag(models.Model):
    # id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    # CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
    # trim_whitespace - trims leading and trailing whitespace
    tag = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return "%s" % (self.tag)

class Content(models.Model):
    """
        This  endpoint  also  allows  including  comments  and  tags.
    """
    created = models.DateTimeField(auto_now_add=True)
    # ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)

    # Not sure how to handle a picture for this
    # class ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, **options)
    image = models.ImageField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag, through='ContentTags', related_name='to_contents_tags')

    # change the default value
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

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



class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField('self', related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', related_name='user_following', symmetrical=False)
    tags = models.ManyToManyField(Tag, through='UserTag')

    def is_following(self, user_id):
        return self.followers.all().filter(user__id=user_id).exists()

    def follow_user(self, user_id):
        other = UserExtended.objects.get(user__id=user_id)
        if not self.is_following(user_id):
            self.following.add(other)
            self.save()
            other.followers.add(self)
            other.save()
            return True

        return False

# Create a UserExtended instance for every User instance created
def create_user_extended(sender, instance, created, *args, **kargs):
    if created:
        user_extended = UserExtended(user=instance)
        user_extended.save()
post_save.connect(create_user_extended, sender=User)

class UserTag(models.Model):
    user = models.ForeignKey(UserExtended, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)