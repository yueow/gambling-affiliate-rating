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
    path('', include('blog.urls', namespace='blog')),
    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)