"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from blog import views

admin.site.site_header = 'Awesome Inc. Administration'
admin.site.site_title = 'Awesome Inc. Administration'


#404 and 500 error handlers
# ! TO FINISH THE CODE BELOW
# # handler404 = views.handler404
# handler500 = views.handler500

urlpatterns = [
    path('secret/', admin.site.urls),
    path('', include('blog.urls')),
    path('summernote/', include('django_summernote.urls')),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)