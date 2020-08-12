from django.shortcuts import render, get_object_or_404
from blog.models import Post
from casinos.models import Casino
from django.core.paginator import Paginator
from django.db.models import Q
from casinos import filters



# ! Вынести это в отдельный файл с конфигами
DEFAULT_TITLE_CONST = "Лучшие онлайн казино в 2019 году. Онлайн казино играть. "

# Create your views here.

def aboutView(request):

    context = {


    }



    return render(request, 'about.html', context)





def casinoRating(request):

# Dummy GET search
    if 'q' in request.GET:
        query_text = request.GET["q"]

        query_raw = Q(title__icontains = query_text)|\
                    Q(slug__icontains = query_text)|\
                    Q(ca_license__icontains = query_text)
        
       
        casinos = Casino.objects.filter(query_raw)
    else:
        casinos = Casino.objects.all()


# Sorting&filtering by buttons
    if 'filter' in request.GET:
        filter_value = request.GET["filter"]
        if filters.FILTERS[filter_value]:
            casinos = filters.FILTERS[filter_value]()
        print(filter_value)





# Title below is changeable 
    title = "Рейтинг онлайн казино 2019. Найти лучшее казино"

    context = {
        'title': title,
        'casinos': casinos,

    }
    return render(request, 'rating.html', context)






def casinoDetail(request, casino):

    casino_object = get_object_or_404(Casino, slug=casino)
    rating_iterator = [
        range(int(casino_object.rate)),
        range(int(casino_object.rate_soft))
        ]

# Title below is changeable 
    title = "Рейтинг онлайн казино 2019. Найти лучшее казино"

    context = {
        'title': title,
        'casino':casino_object,
        'rating_iterator':rating_iterator,

    }


    
    return render(request, 'casino.html', context)








def postList(request):
    postQuery = Post.objects.filter(status = 1).order_by('-created_on')
    casinosTop10 = Casino.objects.order_by('-rate')[:10]

# Paginator block
    paginator = Paginator(postQuery, 3)
    page = request.GET.get('page') 

    postQuery = paginator.get_page(page) # < New in 2.0!
#   


    title = DEFAULT_TITLE_CONST


    context = {
        'postQuery': postQuery,
        'title' : title,
        'casinos': casinosTop10,


    }

    return render(request, 'index.html', context)
    


def postDetail(request, slug):
    model = get_object_or_404(Post, slug=slug)


    title = model.title
    context = {
        'post':model,
        'title':title,
    }

    return render(request, 'post_detail.html', context)



def handler404(request):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)