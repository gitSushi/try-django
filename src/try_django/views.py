# Model View Template (MVT)

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost

def home_page(request):
  new_title = "Welcome to Try Django"
  context = {"title": "not authenticated title"}
  if request.user.is_authenticated:
    # context = {"title": new_title, "my_list": ["one", "two", "three"]}
    qs = BlogPost.objects.all()[:5]
    context = {"title": new_title, "my_list": qs}
  return render(request, "home.html", context)

def about_page(request):
  return render(request, "about.html", {"title": "What do you want now ?!"})
  
def contact_page(request):
  title = "DO NOT EVER CONTACT ME, not even if the building is burning down !!!"
  #print(request.POST)
  form = ContactForm(request.POST or None)
  if form.is_valid():
    print(form.cleaned_data)
    # Reafreshes the form
    form = ContactForm()
  context = {
    "title": title,
    "form": form,
  }
  return render(request, "form.html", context)

def example_page(request):
  context       = {"title": "Example"}
  template_name = "hello_world.html"
  template_obj  = get_template(template_name)
  return HttpResponse(template_obj.render(context))