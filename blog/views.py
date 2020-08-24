import json
import logging

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from casinos.models import Casino
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db.models import Q

from casinos import filters
from blog.models import Post

logger = logging.getLogger(__name__)

# Rating Page
def rating_view(request):
    # !Implement using Haystack
    # Searching
    if 'q' in request.GET:
        query_text = request.GET["q"]

        query_raw = Q(title__icontains = query_text)|\
                    Q(slug__icontains = query_text)|\
                    Q(ca_license__icontains = query_text)
        casinos = Casino.objects.filter(query_raw)
    else:
        casinos = Casino.objects.all()

    # ! Implement usign filter-box
    # Filtering and Sorting 
    if 'filter' in request.GET:
        filter_value = request.GET["filter"]
        if filters.FILTERS[filter_value]:
            casinos = filters.FILTERS[filter_value]()
        # print(filter_value)

    context = {
        'casinos': casinos,
    }
    return render(request, 'rating.html', context)


# Casino Page View
def casino_detail_view(request, casino):
    casino_object = get_object_or_404(Casino, slug=casino)
    
    rating_iterator = [
        range(int(casino_object.rate)),
        range(int(casino_object.rate_soft))
        ]

    context = {
        'casino':casino_object,
        'rating_iterator':rating_iterator,
    }

    return render(request, 'casino.html', context)


# Home/Index Page
def home_view(request):
    posts = Post.objects.filter(status = 1).order_by('-created_on')
    casinos_10 = Casino.objects.order_by('-rate')[:10]

    paginator = Paginator(posts, 5)
    page = request.GET.get('page') 

    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'casinos': casinos_10,
    }

    return render(request, 'index.html', context)
    

# Post Page
def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post' : post,
    }

    return render(request, 'post_detail.html', context)


#
def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


# Post Like/Dislike Endpoint
@csrf_exempt
@require_POST
def post_like(request, slug):
    obj = Post.objects.get(slug=slug)
    
    liked = obj.like(request)
    like_count = obj.like_count

    data = {
        "liked": liked,
        "like_count": like_count,
    }
    logger.info(f'Post like status: {data["liked"]}, Post like count = {data["like_count"]}')
    return JsonResponse(data)

# Check if Post liked
# @csrf_exempt
# @require_POST
# def post_liked(request, slug):
#     obj = Post.objects.get(slug=slug)
#     return JsonResponse({"liked":obj.check_liked})