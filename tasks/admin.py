from django.contrib import admin
from tasks.models import Task, Position, TaskType


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
    )


admin.site.register(TaskType)
admin.site.register(Position)
