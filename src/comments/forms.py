from django import forms

from .models import CommentPost

class CommentPostForm(forms.Form):
  content = forms.CharField()
  commentId = forms.IntegerField()

class CommentPostModelForm(forms.ModelForm):
  class Meta:
    model = CommentPost
    fields = ['content']