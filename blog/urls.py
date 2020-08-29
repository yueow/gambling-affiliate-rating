from django.urls import path
from blog import views

app_name = "blog"


urlpatterns = [
    path('', views.home_view, name='home'),
    path('rating/', views.rating_view, name='rating'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('casino/<slug:casino>/', views.casino_detail_view, name='casino_detail'),

    # AJAX Endpoints
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
]