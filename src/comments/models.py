from django.db import models
from django.conf import settings

from blog.models import BlogPost

User = settings.AUTH_USER_MODEL

class CommentPost(models.Model):
  user = models.ForeignKey(User,  blank=True, null=True, on_delete=models.SET_NULL)
  content = models.CharField(max_length=250, null=True, blank=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  ''' associate comment to post '''
  # commentId = models.IntegerField()
  commentId = models.ForeignKey(BlogPost, null=True, on_delete=models.SET_NULL)
