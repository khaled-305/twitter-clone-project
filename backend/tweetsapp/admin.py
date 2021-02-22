from django.contrib import admin
from .models import Tweet, TweetLike

admin.site.register(Tweet)
admin.site.register(TweetLike)
