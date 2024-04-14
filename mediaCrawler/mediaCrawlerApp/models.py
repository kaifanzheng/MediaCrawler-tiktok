from django.db import models

class TikTokUser(models.Model):
    name = models.CharField(max_length=255)
    ip = models.GenericIPAddressField()

class LiveStreamVideo(models.Model):
    tiktok_user = models.ForeignKey(TikTokUser, on_delete=models.CASCADE, related_name='live_stream_videos')
    url = models.URLField(max_length=255)
    tag = models.CharField(max_length=255)

class SimilarUser(models.Model):
    tiktok_user = models.ForeignKey(TikTokUser, on_delete=models.CASCADE, related_name='similar_users')
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    ip = models.GenericIPAddressField()
