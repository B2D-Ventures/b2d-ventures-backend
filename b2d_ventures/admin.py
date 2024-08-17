from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from b2d_ventures.app.models import Admin, Investor, Startup


# Custom Admin classes
class AdminUserAdmin(UserAdmin):
    model = Admin
    list_display = ('email', 'username', 'is_staff', 'is_superuser')


class InvestorUserAdmin(UserAdmin):
    model = Investor
    list_display = ('email', 'username', 'available_funds', 'total_invested')


class StartupUserAdmin(UserAdmin):
    model = Startup
    list_display = (
    'email', 'username', 'name', 'fundraising_goal', 'total_raised')


admin.site.register(Admin, AdminUserAdmin)
admin.site.register(Investor, InvestorUserAdmin)
admin.site.register(Startup, StartupUserAdmin)
