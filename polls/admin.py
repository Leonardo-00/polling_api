from django.contrib import admin

from .models import Poll, Category, Choice, Vote
# Register your models here.


admin.site.register(Category)
admin.site.register(Choice)
admin.site.register(Vote)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at', 'category', )  # colonne da mostrare
    search_fields = ('question',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)