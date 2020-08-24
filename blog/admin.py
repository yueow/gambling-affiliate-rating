from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin

from blog.models import Post

class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')

    summernote_fields = ('content',)

    list_filter = ("status",)
    search_fields = ('title', 'content')


admin.site.register(Post, PostAdmin)
