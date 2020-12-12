from django.db import models

from django.contrib.auth.models import User

class Chirp(models.Model):
    body = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='chirps', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

class Like(models.Model):
    chirp = models.ForeignKey(Chirp, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)