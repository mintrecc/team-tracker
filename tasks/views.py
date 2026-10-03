from django.views import generic

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
