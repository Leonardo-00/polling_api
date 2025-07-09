from itertools import count
from django.contrib import admin
from django.db.models import Count

from .models import Poll, Category, Choice, Vote
# Register your models here.


admin.site.register(Category)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'votes_count')
    search_fields = ('text',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Annotiamo il queryset con il conteggio delle choices
        qs = qs.annotate(_votes_count=Count('votes'))
        return qs

    def votes_count(self, obj):
        # Nota: qui usiamo l'annotazione definita nel get_queryset
        return obj._votes_count
    votes_count.short_description = "# Votes"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'voted_by')
    

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at', 'category', 'choices_count')  # colonne da mostrare
    search_fields = ('question',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Annotiamo il queryset con il conteggio delle choices
        qs = qs.annotate(_choices_count=Count('choices'))
        return qs

    def choices_count(self, obj):
        # Nota: qui usiamo l'annotazione definita nel get_queryset
        return obj._choices_count
    choices_count.short_description = "# Choices"