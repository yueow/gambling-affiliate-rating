from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from autoslug import AutoSlugField
from django.conf import settings


class Post(models.Model):
    STATUS = (
        (0,"Draft"),
        (1,"Publish")
    )

    title = models.CharField(max_length=200, unique=True, verbose_name= "_(Post Title)")
    # slug = models.SlugField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now = True)
    created_on = models.DateTimeField(auto_now_add=True)    
    content = models.TextField()
    time_for_reading = models.CharField(max_length=50, blank=False, \
        null=True, verbose_name="Time for reading('2 минуты')")
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Service(models.Model):
    # location = CharFild() e.g. Футер
    # name = CharFild() e.g. Текст Футера 
    # content = TextFilder() e.g.  sdhgsdgsdgodsigiosdgoi dsgio dsoig dsiog udsoig 
    pass






