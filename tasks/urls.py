
from django.urls import path

from tasks.views import IndexView, TasksListView, TaskTypeListView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks-list"),
    path("task-types/", TaskTypeListView.as_view(), name="task-types-list")
]

app_name = "tasks"
