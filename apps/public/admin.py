from django.contrib import admin
from .models import OcliconTeamMembers, FrequentlyAskedQuestions

@admin.register(OcliconTeamMembers)
class CliconTeamMembersAdmin(admin.ModelAdmin):
    fields = ("picture", "name", "role")
    list_display = ("picture", "name", "role", 'date_posted')

@admin.register(FrequentlyAskedQuestions)
class FrequentlyAskedQuestionsAdmin(admin.ModelAdmin):
    fields = ('email', 'subject', 'description', 'active_faq')
    list_display = ('email', 'subject', 'description', 'active_faq', 'date_created')
    