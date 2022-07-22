from django.contrib import admin

from .models import Organisation, User, Lead, Agent


admin.site.register(User)
admin.site.register(Organisation)
admin.site.register(Lead)
admin.site.register(Agent)