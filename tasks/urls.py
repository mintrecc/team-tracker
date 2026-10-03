
from django.urls import path

from tasks.views import IndexView, TasksListView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tasks/", TasksListView.as_view(), name="tasks-list")
]

app_name = "tasks"
