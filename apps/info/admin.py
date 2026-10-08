from django.contrib import admin

from .models import Tblinfo


@admin.register(Tblinfo)
class TblinfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title', 'description')
