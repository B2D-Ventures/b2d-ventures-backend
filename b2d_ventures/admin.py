from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from b2d_ventures.app.models import Admin, Investor, Startup, Deal, User, \
    DataRoom, DealInvestor, Investment, Meeting, MeetingParticipant


class DealAdmin(admin.ModelAdmin):
    model = Deal
    list_display = (
        'name', 'startup', 'allocation', 'price_per_unit',
        'minimum_investment',
        'raised', 'start_date', 'end_date', 'investor_count', 'status')
    list_filter = ('startup', 'type', 'status', 'start_date', 'end_date')
    search_fields = ('name', 'startup__name', 'content')
    fieldsets = (
        (None, {
            'fields': ('startup', 'name', 'content', 'type', 'status')
        }),
        ('Images', {
            'fields': (
                'image_background_url', 'image_logo_url', 'image_content_url')
        }),
        ('Financial Details', {
            'fields': (
                'allocation', 'price_per_unit', 'minimum_investment', 'raised')
        }),
        ('Timing', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('investor_count',)
        }),
    )


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'is_staff', 'is_superuser')


class DealInvestorAdmin(admin.ModelAdmin):
    model = DealInvestor
    list_display = ('deal', 'investor', 'investment_amount', 'investment_date')
    list_filter = ('deal', 'investor', 'investment_date')
    search_fields = ('deal__name', 'investor__username', 'investor__email')


class InvestmentAdmin(admin.ModelAdmin):
    model = Investment
    list_display = ('investor', 'deal', 'amount', 'date')
    list_filter = ('investor', 'deal', 'date')
    search_fields = ('investor__username', 'investor__email', 'deal__name')


class MeetingAdmin(admin.ModelAdmin):
    model = Meeting
    list_display = ('date', 'status')
    list_filter = ('status', 'date')


class MeetingParticipantAdmin(admin.ModelAdmin):
    model = MeetingParticipant
    list_display = ('meeting', 'investor', 'startup')
    list_filter = ('meeting', 'investor', 'startup')
    search_fields = ('investor__username', 'investor__email', 'startup__name')


admin.site.register(Deal, DealAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(DealInvestor, DealInvestorAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingParticipant, MeetingParticipantAdmin)
