from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

from tasks.forms import WorkerCreationForm, TaskForm
from tasks.models import (
    Position,
    Task,
    TaskType,
    Worker,
)


class IndexView(generic.TemplateView):
    template_name = "tasks/index.html"

    def get(self, request, *args, **kwargs):
        request.session["num_visits"] = request.session.get(
            "num_visits",
            0,
        ) + 1
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        num_tasks = Task.objects.count()
        num_types = TaskType.objects.count()
        num_workers = Worker.objects.count()
        num_positions = Position.objects.count()
        num_visits = self.request.session.get("num_visits", 1)

        context.update({
            "num_tasks": num_tasks,
            "num_types": num_types,
            "num_workers": num_workers,
            "num_positions": num_positions,
            "num_visits": num_visits,
        })

        return context


class TasksListView(generic.ListView):
    model = Task
    queryset = (Task.objects.select_related("task_type")
                .prefetch_related("assignees"))
    template_name = "tasks/tasks_list.html"


class TasksDetailView(generic.DetailView):
    model = Task


class TaskCreateView(generic.CreateView):
    model = Task
    success_url = reverse_lazy("tasks:tasks-list")
    fields = "__all__"


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks-list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:tasks-list")


class TaskTypeListView(generic.ListView):
    model = TaskType
    context_object_name = "task_types_list"
    template_name = "tasks/task_types_list.html"


class TaskTypeCreateView(generic.CreateView):
    model = TaskType
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/task_types_form.html"
    fields = "__all__"


class TaskTypeUpdateView(generic.UpdateView):
    model = TaskType
    template_name = "tasks/task_types_form.html"
    success_url = reverse_lazy("tasks:tasks-list")
    fields = "__all__"


class TaskTypeDeleteView(generic.DeleteView):
    model = TaskType
    template_name = "tasks/task_type_confirm_delete.html"
    success_url = reverse_lazy("tasks:tasks-list")


class TaskTypeDetailView(generic.DetailView):
    model = TaskType
    context_object_name = "task_type_detail"
    template_name = "tasks/task_type_detail.html"


class WorkerListView(generic.ListView):
    model = get_user_model()


class WorkerDetailView(generic.DetailView):
    model = get_user_model()


class WorkerCreateView(generic.CreateView):
    model = get_user_model()
    form_class = WorkerCreationForm
    success_url = reverse_lazy("tasks:workers-list")


class WorkerDeleteView(generic.DeleteView):
    model = get_user_model()
    success_url = reverse_lazy("tasks:workers-list")


class PositionListView(generic.ListView):
    model = Position
    template_name = "tasks/positions_list.html"


class PositionDetailView(generic.DetailView):
    model = Position
    template_name = "tasks/position_detail.html"


class PositionCreateView(generic.CreateView):
    model = Position
    success_url = reverse_lazy("tasks:positions-list")
    fields = "__all__"


class PositionUpdateView(generic.UpdateView):
    model = Position
    success_url = reverse_lazy("tasks:positions-list")
    fields = "__all__"


class PositionDeleteView(generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:positions-list")
