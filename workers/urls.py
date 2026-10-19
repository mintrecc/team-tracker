from django.urls import path

from workers.views import (
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerDeleteView
)

app_name = "workers"

urlpatterns = [
    path(
        "",
        WorkerListView.as_view(),
        name="workers-list"
    ),
    path(
        "<int:pk>/",
        WorkerDetailView.as_view(),
        name="workers-detail"
    ),
    path(
        "create/",
        WorkerCreateView.as_view(),
        name="workers-create"
    ),
    path(
        "<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="workers-delete"
    ),
]
