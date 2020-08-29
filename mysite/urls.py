from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403, handler400

from blog import views

admin.site.site_header = 'Awesome Inc. Administration'
admin.site.site_title = 'Awesome Inc. Administration'


handler400 = 'blog.views.error400'
handler403 = 'blog.views.error403'
handler404 = 'blog.views.error404'
handler500 = 'blog.views.error500'


urlpatterns = [
    path('secret/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)