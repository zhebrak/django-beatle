from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['path', 'frequency', 'is_enabled']
    list_editable = ['is_enabled']
    list_filter = ['is_enabled']

    readonly_fields = ['path', 'frequency']


admin.site.register(Task, TaskAdmin)
