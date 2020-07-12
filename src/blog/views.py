from django.shortcuts import render , get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.utils import timezone

# Create your views here.
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm

'''
CRUD

GET -> Read/Retrieve
POST -> Create Update Delete

Retrieve will be separated in two :
  all query : list
  single query: details
'''

# list_view is a version of the retrieve_view
def blog_post_list_view(request):
  # list out objects
  # queryset ->list of objects  
  # now = timezone.now()
  # qs = BlogPost.objects.all()
  # qs = BlogPost.objects.filter(publish_date__lte=now)
  ''' Both work due to models.BlogPostManager and models.BlogPostQuerySet '''
  ''' if not logged in shows only published posts '''
  qs = BlogPost.objects.published()
  # qs = BlogPost.objects.all().published()
  ''' Showing both un/published posts '''
  if request.user.is_authenticated:
    my_qs = BlogPost.objects.filter(user=request.user)
    # avoids duplicates
    qs = (qs | my_qs).distinct()
  # could be a search field
  '''
  qs = BlogPost.objects.filter(title__icontains='title')
  '''
  template_name = 'blog/list.html'
  context = {"object_list": qs}
  return render(request, template_name, context)

# (login_url="/login") as argument or change in settings
# @login_required
@staff_member_required
def blog_post_create_view(request):
  # create objects
  '''
  form = BlogPostForm(request.POST or None)
  if form.is_valid():
    #print(form.cleaned_data)
    # ** is python way of destructuring object or unpacking
    obj = BlogPost.objects.create(**form.cleaned_data)
    form = BlogPostForm()
  '''
  form = BlogPostModelForm(request.POST or None, request.FILES or None)
  if form.is_valid():
    #form.save()
    obj = form.save(commit=False)
    # can make some direct changes to the form data
    # obj.title = form.cleaned_data.get("title") + "007"

    # because of decorator access to user in request. post associated to logged in user
    obj.user = request.user
    obj.save()
    form = BlogPostModelForm()
  template_name = 'blog/form.html'
  context = {"form": form}
  return render(request, template_name, context)

def blog_post_detail_view(request, slug):
  # 1 object -> detail view
  obj = get_object_or_404(BlogPost, slug=slug)
  template_name = 'blog/detail.html'
  context = {"object": obj}
  return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request, slug):
  obj = get_object_or_404(BlogPost, slug=slug)
  form = BlogPostModelForm(request.POST or None, instance=obj)
  if form.is_valid():
    form.save()
  template_name = 'blog/form.html'
  context = {"title": f"Update {obj.title}", "form": form}
  return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request, slug):
  obj = get_object_or_404(BlogPost, slug=slug)
  template_name = 'blog/delete.html'
  if request.method == "POST":
    obj.delete()
    return redirect("/blog")
  context = {"object": obj}
  return render(request, template_name, context)


  '''
  #######
  previous lessons code
  #######

  # def blog_post_detail_page(request, post_id):
def blog_post_detail_page(request, slug):
  print("DJANGO SAYS : ", request.user)
  # NOT THE BEST WAY
  '''
  '''
  try:
    # query -> database -> data -> django renders it
    obj = BlogPost.objects.get(id=post_id)
  except BlogPost.DoesNotExist:
    raise Http404
  except ValueError:
    raise Http404
  '''
  '''
  # SO MUCH BETTER
  # SINGLE QUERY
  
  obj = get_object_or_404(BlogPost, slug=slug)
  
  # MULTIPLE QUERY
  '''
  '''
  queryset = BlogPost.objects.filter(slug=slug)
  '''
  '''
  template_name = 'blog_post_detail.html'
  context = {"object": obj}
  return render(request, template_name, context)

  '''

