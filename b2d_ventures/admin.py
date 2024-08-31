from django.contrib import admin

from b2d_ventures.app.models import Deal, User, DealInvestor, Investment, Meeting, MeetingParticipant

admin.site.register(Deal)
admin.site.register(User)
admin.site.register(DealInvestor)
admin.site.register(Investment)
admin.site.register(Meeting)
admin.site.register(MeetingParticipant)
