from django.contrib import admin
from .models import (
    OcliconTeamMembers, FrequentlyAskedQuestions, 
    BlogPost, BlogPostImage, 
    BlogPostLink, NewsLetterSubscriber
)

@admin.register(OcliconTeamMembers)
class CliconTeamMembersAdmin(admin.ModelAdmin):
    fields = ("picture", "name", "role")
    list_display = ("picture", "name", "role", 'date_posted')

@admin.register(FrequentlyAskedQuestions)
class FrequentlyAskedQuestionsAdmin(admin.ModelAdmin):
    fields = ('email', 'subject', 'description', 'active_faq')
    list_display = ('email', 'subject', 'description', 'active_faq', 'date_created')

class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    fields = ['image']

class BlogPostLinkInline(admin.TabularInline):
    model = BlogPostLink
    fields = ('whatsapp_link', 'twitter_link', 'linkedin_link', 'pinterest_link', 'link')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    fields = ('author', 'category', 'title', 'content', 'date_posted')
    list_display = ('author', 'category', 'title', 'date_posted')
    list_filter = ('author', 'category', 'title', 'date_posted')
    readonly_fields = ('id', 'date_posted')
    inlines = [BlogPostImageInline, BlogPostLinkInline]

@admin.register(NewsLetterSubscriber)
class NewsLetterSubscriber(admin.ModelAdmin):
    fields = ['email']
    list_display = ('email', 'is_active', 'date_subscribed')
    list_filter = ('email', 'is_active', 'date_subscribed')
    search_fields = ['email']
