from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'completed')
    
    search_fields = ('title', 'description', 'user__username')

    list_filter = ('priority', 'completed', 'due_date')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user', 'due_date', 'priority', 'completed')
        }),
    )

    ordering = ('due_date',)

admin.site.register(Task, TaskAdmin)
