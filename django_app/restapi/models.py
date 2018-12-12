# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from sorl.thumbnail import ImageField, get_thumbnail


class Tag(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(max_length=255)

    class Meta:
        db_table = 'tag'

    def __str__(self):
        return "%s" % (self.tag)

class Images(models.Model):
    original_image = models.ImageField(blank=False)
    thumbnail = models.ImageField()
    medium = models.ImageField()
    default = models.ImageField()


    def save(self, *args, **kwargs):
        if self.original_image:
            self.default = get_thumbnail(self.original_image, '1080x1080', quality=99, format='JPEG').name
            self.medium = get_thumbnail(self.original_image, '612x612', quality=99, format='JPEG').name
            self.thumbnail = get_thumbnail(self.original_image, '161x161', quality=99, format='JPEG').name
        super(Images, self).save(*args, **kwargs)

class Content(models.Model):
    """
        This  endpoint  also  allows  including  comments  and  tags.
    """
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through='ContentTags', related_name='to_contents_tags', blank=True)

    # change the default value
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=255, null=True)
    images = models.OneToOneField(Images)


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