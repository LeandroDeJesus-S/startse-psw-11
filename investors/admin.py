from django.contrib import admin
from .models import ProposalInvestment


class ProposalInvestmentAdmin(admin.ModelAdmin):
    list_display = ['percent', 'value', 'company', 'investor', 'status']

admin.site.register(ProposalInvestment, ProposalInvestmentAdmin)
