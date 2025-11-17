from django.db import models
from django.contrib.auth.models import User
import datetime

# Extended User Profile for Subscription
# In core/models.py

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, default='0798828381')
    is_paid_registration = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)
    
    # --- NEW FIELD ---
    favorites = models.ManyToManyField('Content', blank=True, related_name='favorited_by')

    def is_premium(self):
        if self.subscription_expiry:
            return self.subscription_expiry > datetime.datetime.now(datetime.timezone.utc)
        return False

    def __str__(self):
        return self.user.username

class Content(models.Model):
    CONTENT_TYPES = (('music', 'Music'), ('podcast', 'Podcast'))
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='covers/')
    audio_file = models.FileField(upload_to='songs/')
    content_type = models.CharField(choices=CONTENT_TYPES, max_length=10, default='music')
    
    def __str__(self):
        return self.title
