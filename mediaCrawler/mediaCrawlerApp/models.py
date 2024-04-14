from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class TikTokUser(models.Model):
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()
    mutable_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.mutable_id:
            # Generate a unique ID
            self.mutable_id = str(uuid.uuid4())
        super(TikTokUser, self).save(*args, **kwargs)

class LiveStreamVideo(models.Model):
    tiktok_user = models.ForeignKey(TikTokUser, on_delete=models.CASCADE, related_name='live_stream_videos')
    url = models.URLField(max_length=255)
    tag = models.CharField(max_length=255)

    def __str__(self):
        return self.url

class SimilarUser(models.Model):
    tiktok_user = models.ForeignKey(TikTokUser, on_delete=models.CASCADE, related_name='similar_users')
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    ip = models.GenericIPAddressField()
    user_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name
