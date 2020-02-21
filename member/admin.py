from django.contrib import admin

from .models import *
admin.site.register(Category)
admin.site.register(Type)

@admin.register(Complaint_Model)
class ComplaintModelAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'respondent_first_name', 'respondent_last_name', 'respondent_address', 'category', 'type',
                       'subject', 'complain', 'created_date', 'created_time')
    fields = ('user', 'respondent_first_name', 'respondent_last_name', 'respondent_address', 'category', 'type',
                       'subject', 'complain', 'created_date', 'created_time', 'resolution', 'comments')