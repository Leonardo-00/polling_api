from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    model = Account

    fieldsets = UserAdmin.fieldsets + (
        ("Categorie preferite", {
            "fields": ("favorite_categories",),
        }),
    )

    filter_horizontal = ("favorite_categories",)  # abilita il selettore con doppia lista

admin.site.register(Account, AccountAdmin)
