from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.conf import settings

# Create your models here.
class author(models.Model):
    auth_name = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_image = models.FileField()
    auth_details = models.TextField()

    def __str__(self):
        return self.auth_name.username

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True,verbose_name='Adres SEO')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' / '.join(full_path[::-1])


class PublishedManager(models.Manager):
    def get_queryset(self):
       '''select only published posts'''
       return super(PublishedManager, self).get_queryset().filter(status="published")

class Post(models.Model):
    author = models.ForeignKey(author, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    body = RichTextUploadingField()
    image = models.FileField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    posted = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # the default manager
    published_objects = PublishedManager()  # The publish-specific manager.
    tags = TaggableManager()
    class Meta:
        ordering = ['-posted', ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField(max_length=160)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return '{}-{}'.format(self.post.title, self.name)

