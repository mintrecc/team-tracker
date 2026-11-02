
from django.urls import path

from tasks.views import (
    IndexView,
    TasksListView,
    TaskTypeListView,
    PositionListView,
    TasksDetailView,
    TaskTypeDetailView,
    PositionDetailView,
    TaskCreateView,
    TaskTypeCreateView,
    PositionCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskTypeUpdateView,
    TaskTypeDeleteView,
    PositionDeleteView,
    PositionUpdateView,
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
        "task-types/<int:pk>/update/",
        TaskTypeUpdateView.as_view(),
        name="task-type-update"
    ),
    path(
        "task-types/<int:pk>/delete/",
        TaskTypeDeleteView.as_view(),
        name="task-type-delete"
    ),
    path(
        "task-types/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="positions-list"
    ),
    path(
        "positions/<int:pk>/",
        PositionDetailView.as_view(),
        name="position-detail"
    ),
    path(
        "positions/<int:pk>/delete",
        PositionDeleteView.as_view(),
        name="position-delete"
    ),
    path(
        "positions/<int:pk>/update",
        PositionUpdateView.as_view(),
        name="position-update"
    ),
    path(

        "positions/create/",
        PositionCreateView.as_view(),
        name="position-create"
    ),
]

app_name = "tasks"
