from django.db import models
from django.conf import settings
from django.utils import timezone

# clicon team members model create
class OcliconTeamMembers(models.Model):
    picture = models.ImageField(upload_to='team/%Y/%m/%d/', blank=False, null=False)
    name = models.CharField(max_length=30, null=False, blank=False)
    role = models.CharField(max_length=40)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Faqs model --
class FrequentlyAskedQuestions(models.Model):
    email = models.EmailField(max_length=50, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(max_length=500, blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    active_faq = models.BooleanField(default=False)

    def __str__(self):
        return self.email

# blog post model create
class BlogPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
    category = models.ForeignKey('products.Category', on_delete=models.CASCADE, related_name='stack')
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} by {self.author.username}'

# blog post image
class BlogPostImage(models.Model):
    post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='blog_post_images')
    image = models.ImageField(upload_to='blogpost/blog-img/%Y/%m/%d/')

    def __str__(self):
        return self.post.title

# blog post links
class BlogPostLink(models.Model):
    post = models.OneToOneField(BlogPost, on_delete=models.CASCADE, related_name='blog_post_links')
    whatsapp_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()
    pinterest_link = models.URLField()
    link = models.URLField()

    def __str__(self):
        return self.post.title

# comment for blog post
class BlogPostComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='blog_post_comment')
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

# news letter model
class NewsLetterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
