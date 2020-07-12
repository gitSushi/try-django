from django import forms

from .models import BlogPost

class BlogPostForm(forms.Form):
  title = forms.CharField()
  slug = forms.SlugField()
  content = forms.CharField(widget=forms.Textarea)

class BlogPostModelForm(forms.ModelForm):
  class Meta:
    model = BlogPost
    fields = ['title', 'slug', 'content', 'publish_date', 'image']

  # allows unique titles
  def clean_title(self, *args, **kwargs):
    # debugging helper
    # print(dir(self))
    instance = self.instance
    # create post will have instance -> none
    # print(instance)
    title = self.cleaned_data.get('title')
    # Checks if chosen title already on the database
    # title__iexact -> not case sensitive
    qs = BlogPost.objects.filter(title__iexact=title)
    # update -> allows an instance to be the same
    if instance is not None:
      qs = qs.exclude(pk=instance.pk)
    if qs.exists():
      raise forms.ValidationError("This title is taken. You lost, now PISS OFF !")
    return title