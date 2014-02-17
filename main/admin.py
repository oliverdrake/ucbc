from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from main.models import UserRole, BrewtoadAccount


class UCBCUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined',
                    'is_staff', 'is_active', 'is_superuser', 'get_groups')

    def get_groups(self, user):
        return ", ".join([str(group.name) for group in user.groups.all()])
    get_groups.short_description = "Groups"


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


class BrewtoadAccountAdmin(admin.ModelAdmin):
    list_display = ('brewtoad_user_id', 'user')

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UCBCUserAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(BrewtoadAccount, BrewtoadAccountAdmin)
