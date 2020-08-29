import json
import logging

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db.models import Q
from casinos.models import Casino, CasinoRating, TopCasino, UserExists, IpExists

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

    # ! Implement using filter-box
    # Filtering and Sorting 
    if 'filter' in request.GET:
        filter_value = request.GET["filter"]
        if filters.FILTERS[filter_value]:
            casinos = filters.FILTERS[filter_value]()
        logger.debug(filter_value)

    context = {
        'casinos': casinos,
    }

    logger.debug(f'Context data: {context}')
    return render(request, 'rating.html', context)


# Casino Page
def casino_detail_view(request, casino):
    casino_object = get_object_or_404(Casino, slug=casino)
    
    # Handles rating data
    if request.method == "POST":
        logger.debug(request.POST)

        rate = request.POST.get('main_star', 0)
        rate_safe = request.POST.get('safe_star', 0)
        rate_faith = request.POST.get('faith_star', 0)
        rate_design = request.POST.get('design_star', 0)
        rate_soft = request.POST.get('software_star', 0)
        # logger.warning(rate)
        # logger.warning(rate_safe)
        # logger.warning(rate_debug)
        # logger.warning(rate_faith)
        # logger.warning(rate_soft)
        ip = request.META['REMOTE_ADDR']
        user = None if request.user.is_anonymous else request.user

        try:
            new = CasinoRating.objects.create(
                casino=casino_object,
                user=user,
                rate=rate,
                rate_safe=rate_safe,
                rate_faith=rate_faith,
                rate_design=rate_design,
                rate_soft=rate_soft,
                ip=ip)
            logger.debug(f'{casino} rated!')
            logger.debug(new)        
        except UserExists as err:
            messages.error(request, err)
            logger.warning(err)
            logger.warning(f'{casino}, {user} - {ip}')
        except IpExists as err:
            messages.error(request, err)
            logger.warning(err)
            logger.warning(f'{casino}, {user} - {ip}')

    context = {
        'casino': casino_object,
    }

    logger.debug(f'Context data: {context}')
    return render(request, 'casino.html', context)


# Home/Index Page
def home_view(request):
    posts = Post.objects.filter(status=1).order_by('-created')
    
    # ! Implement using TopCasino model
    casinos_10 = Casino.objects.all()

    # Pagination
    paginator = Paginator(posts, 5)
    page = request.GET.get('page') 
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'casinos': casinos_10,
    }

    logger.debug(f'Context data: {context}')
    return render(request, 'index.html', context)
    

# Post Page
def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    context = {
        'post' : post,
    }

    logger.debug(f'Context data: {context}')
    return render(request, 'post_detail.html', context)


# Post Like/Dislike Endpoint
@csrf_exempt
@require_POST
def post_like(request, slug):
    obj = get_object_or_404(Post, slug=slug)

    liked = obj.like(request)
    like_count = obj.like_count

    data = {
        "liked": liked,
        "like_count": like_count,
    }
    logger.debug(f'Post like status: {data["liked"]}, Post like count = {data["like_count"]}')
    return JsonResponse(data)


# Handles response codes
def error400(request, exception=None):
    return render(request, '404.html', status=400)

def error403(request, exception=None):
    return render(request, '404.html', status=403)

def error404(request, exception=None):
    return render(request, '404.html', status=404)

def error500(request, exception=None):
    return render(request, '500.html', status=500)