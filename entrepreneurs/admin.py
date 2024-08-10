from django.contrib import admin
from .models import Company, Document, Metric


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'name', 'area', 'stage', 'time_of_existence', 'valuation'
    ]
    list_display_links = list_display


admin.site.register(Company, CompanyAdmin)
admin.site.register(Document)
admin.site.register(Metric)
