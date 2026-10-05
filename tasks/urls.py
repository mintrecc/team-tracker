
from django.urls import path

from tasks.views import (
    IndexView,
    TasksListView,
    TaskTypeListView,
    WorkerListView,
    PositionListView,
    TasksDetailView,
    TaskTypeDetailView,
    WorkerDetailView,
    PositionDetailView,
    TaskCreateView,
    TaskTypeCreateView,
    WorkerCreateView,
    PositionCreateView,
    TaskUpdateView,
    TaskDeleteView,
)


urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index"
    ),
    path(
        "tasks/",
        TasksListView.as_view(),
        name="tasks-list"
    ),
    path(
        "tasks/<int:pk>/",
        TasksDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "task-types/",
        TaskTypeListView.as_view(),
        name="task-types-list"
    ),
    path(
        "task-types/<int:pk>/",
        TaskTypeDetailView.as_view(),
        name="task-type-detail"
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="workers-list"),
    path(
        "workers/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "workers/create/",
        WorkerCreateView.as_view(),
        name="worker-create"),
    path(
        "positions/",
        PositionListView.as_view(),
        name="positions-list"),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(

        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
]

app_name = "tasks"
