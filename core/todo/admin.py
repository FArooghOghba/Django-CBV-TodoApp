from django.contrib import admin
from .models import Task


# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'complete', 'created_date')
    actions = ('tasks_cancellation',)

    @admin.action(description='tasks_cancellation')
    def tasks_cancellation(self, request, queryset):
        updated_count = queryset.update(complete=False)
        self.message_user(
            request,
            f'{updated_count} tasks were successfully updated.'
        )
