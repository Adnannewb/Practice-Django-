from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post

# Create your views here.

def post_list(request):
    posts=Post.objects.all().order_by('id')
    paginator=Paginator(posts,4)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'post_list.html',{'page_obj':page_obj})