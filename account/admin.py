from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Profile


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', )
    readonly_fields = ("id", "date_joined", "last_login")
    # list_editable = ('administration_status',)

    filter_horizontal = ()
    # list_filter = ('status', 'administration_status')
    fieldsets = ()
    ordering = ('-date_joined',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Profile)
