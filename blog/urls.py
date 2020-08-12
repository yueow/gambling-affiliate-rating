from django.urls import path
from . import views



urlpatterns = [
    path('', views.postList, name='home'),
    path('post/<slug:slug>/', views.postDetail, name='post_detail'),

    path('about/', views.aboutView, name='about'),

    # casinos
    path('rating/', views.casinoRating, name='rating'),
    path('casino/<slug:casino>/', views.casinoDetail, name='casino_detail'),




]


