
from django.urls import path

from tasks.views import (
    IndexView,
    TasksListView,
    TaskTypeListView, WorkerListView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks-list"),
    path("task-types/", TaskTypeListView.as_view(), name="task-types-list"),
    path("workers/", WorkerListView.as_view(), name="workers-list")
]

app_name = "tasks"
