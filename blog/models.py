from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

from autoslug import AutoSlugField


class Post(models.Model):

    STATUS = (
        (0,"Draft"),
        (1,"Publish")
    )

    title = models.CharField(max_length=200, unique=True, verbose_name=_("Post Title"))
    slug = AutoSlugField(populate_from='title')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)    
    content = models.TextField(max_length=10000)
    reading_time = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name=_('Time for reading'))
    status = models.IntegerField(choices=STATUS, default=0)

    liked = models.ManyToManyField(settings.AUTH_USER_MODEL)
    like_count = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'slug':self.slug})

    @property
    def get_like_count(self):
        return self.likeds
        
    # Post Like/Dislike method
    def like(self, request):
        # For Anonymous Users
        # Post Liking works through Request Sessions
        session_liked_posts = request.session.get('posts_liked', [])
        status = None

        if request.user.is_anonymous:
            print(session_liked_posts)
            if self.id in session_liked_posts:
                session_liked_posts.remove(self.id)
                self.like_count -= 1
                self.save()
                status = False
            else:
                session_liked_posts.append(self.id)
                self.like_count += 1
                self.save()
                status = True
            
        # For Logged In Users
        # Post Liking works through ManyToMany, User Model + Request Sessions(for secure purposes)
        else:
            if request.user in self.liked.all():
                self.liked.remove(request.user)
                try:
                    session_liked_posts.remove(self.id)
                except:
                    pass

                # print('Username In')
                self.like_count -= 1
                self.save()
                status = False

            else:
                session_liked_posts.append(self.id)
                # print('Username Not In')
                self.liked.add(request.user)
                self.like_count += 1
                self.save()
                # print('Added')
                status = True

        request.session['posts_liked'] = session_liked_posts
        # print("Checking Request Session")
        # print(request.session['posts_liked'])
        
        return status