from django.contrib import admin

from .models import Poll, Category, Choice, Vote
# Register your models here.


admin.site.register(Category)
admin.site.register(Choice)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_by', 'created_at')  # colonne da mostrare
    search_fields = ('question',)
    list_filter = ('created_at',)